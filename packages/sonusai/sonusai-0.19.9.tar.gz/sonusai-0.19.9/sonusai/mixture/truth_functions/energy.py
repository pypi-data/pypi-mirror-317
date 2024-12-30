import numpy as np

from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Truth
from sonusai.utils import load_object


def _core(
    mixdb: MixtureDatabase,
    m_id: int,
    target_index: int,
    config: dict,
    parameters: int,
    mapped: bool,
    snr: bool,
) -> Truth:
    from os.path import join

    import torch
    from pyaaware import ForwardTransform
    from pyaaware import feature_forward_transform_config

    from sonusai.utils import compute_energy_f

    target_audio = mixdb.mixture_targets(m_id)[target_index]
    ft = ForwardTransform(**feature_forward_transform_config(mixdb.feature))

    frames = ft.frames(torch.from_numpy(target_audio))

    if mixdb.mixture(m_id).target_gain(target_index) == 0:
        return np.zeros((frames, parameters), dtype=np.float32)

    noise_audio = mixdb.mixture_noise(m_id)

    target_energy = compute_energy_f(time_domain=target_audio, transform=ft)
    noise_energy = None
    if snr:
        noise_energy = compute_energy_f(time_domain=noise_audio, transform=ft)

    frames = len(target_energy)
    truth = np.empty((frames, ft.bins), dtype=np.float32)
    for frame in range(frames):
        tmp = target_energy[frame]

        if noise_energy is not None:
            old_err = np.seterr(divide="ignore", invalid="ignore")
            tmp /= noise_energy[frame]
            np.seterr(**old_err)

        tmp = np.nan_to_num(tmp, nan=-np.inf, posinf=np.inf, neginf=-np.inf)

        if mapped:
            snr_db_mean = load_object(join(mixdb.location, config["snr_db_mean"]))
            snr_db_std = load_object(join(mixdb.location, config["snr_db_std"]))
            tmp = _calculate_mapped_snr_f(tmp, snr_db_mean, snr_db_std)

        truth[frame] = tmp

    return truth


def _calculate_mapped_snr_f(truth_f: np.ndarray, snr_db_mean: np.ndarray, snr_db_std: np.ndarray) -> np.ndarray:
    """Calculate mapped SNR from standard SNR energy per bin/class."""
    import scipy.special as sc

    old_err = np.seterr(divide="ignore", invalid="ignore")
    num = 10 * np.log10(np.double(truth_f)) - np.double(snr_db_mean)
    den = np.double(snr_db_std) * np.sqrt(2)
    q = num / den
    q = np.nan_to_num(q, nan=-np.inf, posinf=np.inf, neginf=-np.inf)
    result = 0.5 * (1 + sc.erf(q))
    np.seterr(**old_err)

    return result.astype(np.float32)


def energy_f_validate(_config: dict) -> None:
    pass


def energy_f_parameters(feature: str, _num_classes: int, _config: dict) -> int:
    from pyaaware import ForwardTransform
    from pyaaware import feature_forward_transform_config

    return ForwardTransform(**feature_forward_transform_config(feature)).bins


def energy_f(mixdb: MixtureDatabase, m_id: int, target_index: int, config: dict) -> Truth:
    """Frequency domain energy truth generation function

    Calculates the true energy per bin:

    Ti^2 + Tr^2

    where T is the target STFT bin values.

    Output shape: [:, bins]
    """
    return _core(
        mixdb=mixdb,
        m_id=m_id,
        target_index=target_index,
        config=config,
        parameters=energy_f_parameters(mixdb.feature, mixdb.num_classes, config),
        mapped=False,
        snr=False,
    )


def snr_f_validate(_config: dict) -> None:
    pass


def snr_f_parameters(feature: str, _num_classes: int, _config: dict) -> int:
    from pyaaware import ForwardTransform
    from pyaaware import feature_forward_transform_config

    return ForwardTransform(**feature_forward_transform_config(feature)).bins


def snr_f(mixdb: MixtureDatabase, m_id: int, target_index: int, config: dict) -> Truth:
    """Frequency domain SNR truth function documentation

    Calculates the true SNR per bin:

    (Ti^2 + Tr^2) / (Ni^2 + Nr^2)

    where T is the target and N is the noise STFT bin values.

    Output shape: [:, bins]
    """
    return _core(
        mixdb=mixdb,
        m_id=m_id,
        target_index=target_index,
        config=config,
        parameters=snr_f_parameters(mixdb.feature, mixdb.num_classes, config),
        mapped=False,
        snr=True,
    )


def mapped_snr_f_validate(config: dict) -> None:
    if len(config) == 0:
        raise AttributeError("mapped_snr_f truth function is missing config")

    for parameter in ("snr_db_mean", "snr_db_std"):
        if parameter not in config:
            raise AttributeError(f"mapped_snr_f truth function is missing required '{parameter}'")


def mapped_snr_f_parameters(feature: str, _num_classes: int, _config: dict) -> int:
    from pyaaware import ForwardTransform
    from pyaaware import feature_forward_transform_config

    return ForwardTransform(**feature_forward_transform_config(feature)).bins


def mapped_snr_f(mixdb: MixtureDatabase, m_id: int, target_index: int, config: dict) -> Truth:
    """Frequency domain mapped SNR truth function documentation

    Output shape: [:, bins]
    """
    return _core(
        mixdb=mixdb,
        m_id=m_id,
        target_index=target_index,
        config=config,
        parameters=mapped_snr_f_parameters(mixdb.feature, mixdb.num_classes, config),
        mapped=True,
        snr=True,
    )


def energy_t_validate(_config: dict) -> None:
    pass


def energy_t_parameters(_feature: str, _num_classes: int, _config: dict) -> int:
    return 1


def energy_t(mixdb: MixtureDatabase, m_id: int, target_index: int, _config: dict) -> Truth:
    """Time domain energy truth function documentation

    Calculates the true time domain energy of each frame:

    For OLS:
        sum(x[0:N-1]^2) / N

    For OLA:
        sum(x[0:R-1]^2) / R

    where x is the target time domain data,
    N is the size of the transform, and
    R is the number of new samples in the frame.

    Output shape: [:, 1]

    Note: feature transforms can be defined to use a subset of all bins,
    i.e., subset of 0:128 for N=256 could be 0:127 or 1:128. energy_t
    will reflect the total energy over all bins regardless of the feature
    transform config.
    """
    import torch
    from pyaaware import ForwardTransform
    from pyaaware import feature_forward_transform_config

    target_audio = torch.from_numpy(mixdb.mixture_targets(m_id)[target_index])

    ft = ForwardTransform(**feature_forward_transform_config(mixdb.feature))

    frames = ft.frames(target_audio)
    parameters = energy_f_parameters(mixdb.feature, mixdb.num_classes, _config)
    if mixdb.mixture(m_id).target_gain(target_index) == 0:
        return np.zeros((frames, parameters), dtype=np.float32)

    return ft.execute_all(target_audio)[1].numpy()

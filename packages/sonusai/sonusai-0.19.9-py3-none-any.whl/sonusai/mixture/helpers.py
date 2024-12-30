from pyaaware import ForwardTransform
from pyaaware import InverseTransform

from sonusai.mixture.datatypes import AudioF
from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import Augmentation
from sonusai.mixture.datatypes import AugmentationRule
from sonusai.mixture.datatypes import EnergyT
from sonusai.mixture.datatypes import FeatureGeneratorConfig
from sonusai.mixture.datatypes import FeatureGeneratorInfo
from sonusai.mixture.datatypes import GeneralizedIDs
from sonusai.mixture.datatypes import Mixture
from sonusai.mixture.datatypes import NoiseFile
from sonusai.mixture.datatypes import SpeechMetadata
from sonusai.mixture.datatypes import Target
from sonusai.mixture.datatypes import TargetFile
from sonusai.mixture.datatypes import TransformConfig
from sonusai.mixture.db_datatypes import MixtureRecord
from sonusai.mixture.db_datatypes import TargetRecord
from sonusai.mixture.mixdb import MixtureDatabase


def generic_ids_to_list(num_ids: int, ids: GeneralizedIDs = "*") -> list[int]:
    """Resolve generalized IDs to a list of integers

    :param num_ids: Total number of indices
    :param ids: Generalized IDs
    :return: List of ID integers
    """
    all_ids = list(range(num_ids))

    if isinstance(ids, str):
        if ids == "*":
            return all_ids

        try:
            result = eval(f"{all_ids}[{ids}]")  # noqa: S307
            if isinstance(result, list):
                return result
            else:
                return [result]
        except NameError as e:
            raise ValueError(f"Empty ids {ids}: {e}") from e

    if isinstance(ids, range):
        result = list(ids)
    elif isinstance(ids, int):
        result = [ids]
    else:
        result = ids

    if not all(isinstance(x, int) and 0 <= x < num_ids for x in result):
        raise ValueError(f"Invalid entries in ids of {ids}")

    if not result:
        raise ValueError(f"Empty ids {ids}")

    return result


def get_feature_generator_info(
    fg_config: FeatureGeneratorConfig,
) -> FeatureGeneratorInfo:
    from dataclasses import asdict

    from pyaaware import FeatureGenerator

    from .datatypes import FeatureGeneratorInfo
    from .datatypes import TransformConfig

    fg = FeatureGenerator(**asdict(fg_config))

    return FeatureGeneratorInfo(
        decimation=fg.decimation,
        stride=fg.stride,
        step=fg.step,
        feature_parameters=fg.feature_parameters,
        ft_config=TransformConfig(
            length=fg.ftransform_length,
            overlap=fg.ftransform_overlap,
            bin_start=fg.bin_start,
            bin_end=fg.bin_end,
            ttype=fg.ftransform_ttype,
        ),
        eft_config=TransformConfig(
            length=fg.eftransform_length,
            overlap=fg.eftransform_overlap,
            bin_start=fg.bin_start,
            bin_end=fg.bin_end,
            ttype=fg.eftransform_ttype,
        ),
        it_config=TransformConfig(
            length=fg.itransform_length,
            overlap=fg.itransform_overlap,
            bin_start=fg.bin_start,
            bin_end=fg.bin_end,
            ttype=fg.itransform_ttype,
        ),
    )


def mixture_all_speech_metadata(mixdb: MixtureDatabase, mixture: Mixture) -> list[dict[str, SpeechMetadata]]:
    """Get a list of all speech metadata for the given mixture"""
    from praatio.utilities.constants import Interval

    from .datatypes import SpeechMetadata

    results: list[dict[str, SpeechMetadata]] = []
    for target in mixture.targets:
        data: dict[str, SpeechMetadata] = {}
        for tier in mixdb.speaker_metadata_tiers:
            data[tier] = mixdb.speaker(mixdb.target_file(target.file_id).speaker_id, tier)

        for tier in mixdb.textgrid_metadata_tiers:
            item = get_textgrid_tier_from_target_file(mixdb.target_file(target.file_id).name, tier)
            if isinstance(item, list):
                # Check for tempo augmentation and adjust Interval start and end data as needed
                entries = []
                for entry in item:
                    if target.augmentation.tempo is not None:
                        entries.append(
                            Interval(
                                entry.start / target.augmentation.tempo,
                                entry.end / target.augmentation.tempo,
                                entry.label,
                            )
                        )
                    else:
                        entries.append(entry)
                data[tier] = entries
            else:
                data[tier] = item
        results.append(data)

    return results


def mixture_metadata(mixdb: MixtureDatabase, m_id: int) -> str:
    """Create a string of metadata for a Mixture

    :param mixdb: Mixture database
    :param m_id: Mixture ID
    :return: String of metadata
    """
    mixture = mixdb.mixture(m_id)
    metadata = ""
    speech_metadata = mixture_all_speech_metadata(mixdb, mixture)
    for mi, target in enumerate(mixture.targets):
        target_file = mixdb.target_file(target.file_id)
        target_augmentation = target.augmentation
        metadata += f"target {mi} name: {target_file.name}\n"
        metadata += f"target {mi} augmentation: {target.augmentation.to_dict()}\n"
        metadata += f"target {mi} ir: {mixdb.impulse_response_file(target_augmentation.ir)}\n"
        metadata += f"target {mi} target_gain: {target.gain if not mixture.is_noise_only else 0}\n"
        metadata += f"target {mi} class indices: {target_file.class_indices}\n"
        for key in target_file.truth_configs:
            metadata += f"target {mi} truth '{key}' function: {target_file.truth_configs[key].function}\n"
            metadata += f"target {mi} truth '{key}' config:   {target_file.truth_configs[key].config}\n"
        for key in speech_metadata[mi]:
            metadata += f"target {mi} speech {key}: {speech_metadata[mi][key]}\n"
    noise = mixdb.noise_file(mixture.noise.file_id)
    noise_augmentation = mixture.noise.augmentation
    metadata += f"noise name: {noise.name}\n"
    metadata += f"noise augmentation: {noise_augmentation.to_dict()}\n"
    metadata += f"noise ir: {mixdb.impulse_response_file(noise_augmentation.ir)}\n"
    metadata += f"noise offset: {mixture.noise_offset}\n"
    metadata += f"snr: {mixture.snr}\n"
    metadata += f"random_snr: {mixture.snr.is_random}\n"
    metadata += f"samples: {mixture.samples}\n"
    metadata += f"target_snr_gain: {float(mixture.target_snr_gain)}\n"
    metadata += f"noise_snr_gain: {float(mixture.noise_snr_gain)}\n"

    return metadata


def write_mixture_metadata(mixdb: MixtureDatabase, m_id: int) -> None:
    """Write mixture metadata to a text file

    :param mixdb: Mixture database
    :param m_id: Mixture ID
    """
    from os.path import join

    name = join(mixdb.location, "mixture", mixdb.mixture(m_id).name, "metadata.txt")
    with open(file=name, mode="w") as f:
        f.write(mixture_metadata(mixdb, m_id))


def from_mixture(
    mixture: Mixture,
) -> tuple[str, int, str, int, float, bool, float, int, int, int, float]:
    return (
        mixture.name,
        mixture.noise.file_id,
        mixture.noise.augmentation.to_json(),
        mixture.noise_offset,
        mixture.noise_snr_gain,
        mixture.snr.is_random,
        mixture.snr,
        mixture.samples,
        mixture.spectral_mask_id,
        mixture.spectral_mask_seed,
        mixture.target_snr_gain,
    )


def to_mixture(entry: MixtureRecord, targets: list[Target]) -> Mixture:
    import json

    from sonusai.utils import dataclass_from_dict

    from .datatypes import Noise
    from .datatypes import UniversalSNR

    return Mixture(
        targets=targets,
        name=entry.name,
        noise=Noise(
            file_id=entry.noise_file_id,
            augmentation=dataclass_from_dict(Augmentation, json.loads(entry.noise_augmentation)),  # pyright: ignore [reportArgumentType]
        ),
        noise_offset=entry.noise_offset,
        noise_snr_gain=entry.noise_snr_gain,
        snr=UniversalSNR(is_random=entry.random_snr, value=entry.snr),
        samples=entry.samples,
        spectral_mask_id=entry.spectral_mask_id,
        spectral_mask_seed=entry.spectral_mask_seed,
        target_snr_gain=entry.target_snr_gain,
    )


def from_target(target: Target) -> tuple[int, str]:
    return target.file_id, target.augmentation.to_json()


def to_target(entry: TargetRecord) -> Target:
    import json

    from sonusai.utils import dataclass_from_dict

    from .datatypes import Augmentation

    return Target(
        file_id=entry.file_id,
        augmentation=dataclass_from_dict(Augmentation, json.loads(entry.augmentation)),  # pyright: ignore [reportArgumentType]
    )


def get_target(mixdb: MixtureDatabase, mixture: Mixture, targets_audio: list[AudioT]) -> AudioT:
    """Get the augmented target audio data for the given mixture record

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :param targets_audio: List of augmented target audio data (one per target in the mixup)
    :return: Sum of augmented target audio data
    """
    # Apply impulse responses to targets
    import numpy as np

    from .audio import read_ir
    from .augmentation import apply_impulse_response

    targets_ir = []
    for idx, target in enumerate(targets_audio):
        ir_idx = mixture.targets[idx].augmentation.ir
        if ir_idx is not None:
            targets_ir.append(
                apply_impulse_response(audio=target, ir=read_ir(mixdb.impulse_response_file(int(ir_idx))))
            )
        else:
            targets_ir.append(target)

    # Return sum of targets
    return np.sum(targets_ir, axis=0)


def get_transform_from_audio(audio: AudioT, transform: ForwardTransform) -> tuple[AudioF, EnergyT]:
    """Apply forward transform to input audio data to generate transform data

    :param audio: Time domain data [samples]
    :param transform: ForwardTransform object
    :return: Frequency domain data [frames, bins], Energy [frames]
    """
    import torch

    f, e = transform.execute_all(torch.from_numpy(audio))

    return f.numpy(), e.numpy()


def forward_transform(audio: AudioT, config: TransformConfig) -> AudioF:
    """Transform time domain data into frequency domain using the forward transform config from the feature

    A new transform is used for each call; i.e., state is not maintained between calls to forward_transform().

    :param audio: Time domain data [samples]
    :param config: Transform configuration
    :return: Frequency domain data [frames, bins]
    """
    from pyaaware import ForwardTransform

    audio_f, _ = get_transform_from_audio(
        audio=audio,
        transform=ForwardTransform(
            length=config.length,
            overlap=config.overlap,
            bin_start=config.bin_start,
            bin_end=config.bin_end,
            ttype=config.ttype,
        ),
    )
    return audio_f


def get_audio_from_transform(data: AudioF, transform: InverseTransform) -> tuple[AudioT, EnergyT]:
    """Apply inverse transform to input transform data to generate audio data

    :param data: Frequency domain data [frames, bins]
    :param transform: InverseTransform object
    :return: Time domain data [samples], Energy [frames]
    """

    import torch

    t, e = transform.execute_all(torch.from_numpy(data))

    return t.numpy(), e.numpy()


def inverse_transform(transform: AudioF, config: TransformConfig) -> AudioT:
    """Transform frequency domain data into time domain using the inverse transform config from the feature

    A new transform is used for each call; i.e., state is not maintained between calls to inverse_transform().

    :param transform: Frequency domain data [frames, bins]
    :param config: Transform configuration
    :return: Time domain data [samples]
    """
    from pyaaware import InverseTransform

    audio, _ = get_audio_from_transform(
        data=transform,
        transform=InverseTransform(
            length=config.length,
            overlap=config.overlap,
            bin_start=config.bin_start,
            bin_end=config.bin_end,
            ttype=config.ttype,
            gain=1,
        ),
    )
    return audio


def check_audio_files_exist(mixdb: MixtureDatabase) -> None:
    """Walk through all the noise and target audio files in a mixture database ensuring that they exist"""
    from os.path import exists

    from .tokenized_shell_vars import tokenized_expand

    for noise in mixdb.noise_files:
        file_name, _ = tokenized_expand(noise.name)
        if not exists(file_name):
            raise OSError(f"Could not find {file_name}")

    for target in mixdb.target_files:
        file_name, _ = tokenized_expand(target.name)
        if not exists(file_name):
            raise OSError(f"Could not find {file_name}")


def augmented_target_samples(
    target_files: list[TargetFile],
    target_augmentations: list[AugmentationRule],
    feature_step_samples: int,
) -> int:
    from itertools import product

    from .augmentation import estimate_augmented_length_from_length

    target_ids = list(range(len(target_files)))
    target_augmentation_ids = list(range(len(target_augmentations)))
    it = list(product(*[target_ids, target_augmentation_ids]))
    return sum(
        [
            estimate_augmented_length_from_length(
                length=target_files[fi].samples,
                tempo=target_augmentations[ai].tempo,
                frame_length=feature_step_samples,
            )
            for fi, ai in it
        ]
    )


def augmented_noise_samples(noise_files: list[NoiseFile], noise_augmentations: list[Augmentation]) -> int:
    from itertools import product

    noise_ids = list(range(len(noise_files)))
    noise_augmentation_ids = list(range(len(noise_augmentations)))
    it = list(product(*[noise_ids, noise_augmentation_ids]))
    return sum([augmented_noise_length(noise_files[fi], noise_augmentations[ai]) for fi, ai in it])


def augmented_noise_length(noise_file: NoiseFile, noise_augmentation: Augmentation) -> int:
    from .augmentation import estimate_augmented_length_from_length

    return estimate_augmented_length_from_length(length=noise_file.samples, tempo=noise_augmentation.tempo)


def get_textgrid_tier_from_target_file(target_file: str, tier: str) -> SpeechMetadata | None:
    from pathlib import Path

    from praatio import textgrid
    from praatio.utilities.constants import Interval

    from .tokenized_shell_vars import tokenized_expand

    textgrid_file = Path(tokenized_expand(target_file)[0]).with_suffix(".TextGrid")
    if not textgrid_file.exists():
        return None

    tg = textgrid.openTextgrid(str(textgrid_file), includeEmptyIntervals=False)

    if tier not in tg.tierNames:
        return None

    entries = tg.getTier(tier).entries
    if len(entries) > 1:
        return [entry for entry in entries if isinstance(entry, Interval)]

    if len(entries) == 1:
        return entries[0].label

    return None


def frames_from_samples(samples: int, step_samples: int) -> int:
    import numpy as np

    return int(np.ceil(samples / step_samples))

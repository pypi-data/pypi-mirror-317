from collections.abc import Iterable
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import NamedTuple
from typing import SupportsIndex
from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from dataclasses_json import DataClassJsonMixin
from praatio.utilities.constants import Interval

AudioT: TypeAlias = npt.NDArray[np.float32]

Truth: TypeAlias = Any
TruthDict: TypeAlias = dict[str, Truth]
Segsnr: TypeAlias = npt.NDArray[np.float32]

AudioF: TypeAlias = npt.NDArray[np.complex64]

EnergyT: TypeAlias = npt.NDArray[np.float32]
EnergyF: TypeAlias = npt.NDArray[np.float32]

Feature: TypeAlias = npt.NDArray[np.float32]

Predict: TypeAlias = npt.NDArray[np.float32]

# Json type defined to maintain compatibility with DataClassJsonMixin
Json: TypeAlias = dict | list | str | int | float | bool | None


class DataClassSonusAIMixin(DataClassJsonMixin):
    def __str__(self):
        return f"{self.to_dict()}"

    # Override DataClassJsonMixin to remove dictionary keys with values of None
    def to_dict(self, encode_json=False) -> dict[str, Json]:
        def del_none(d):
            if isinstance(d, dict):
                for key, value in list(d.items()):
                    if value is None:
                        del d[key]
                    elif isinstance(value, dict):
                        del_none(value)
                    elif isinstance(value, list):
                        for item in value:
                            del_none(item)
            elif isinstance(d, list):
                for item in d:
                    del_none(item)
            return d

        return del_none(super().to_dict(encode_json))


@dataclass(frozen=True)
class TruthConfig(DataClassSonusAIMixin):
    function: str
    stride_reduction: str
    config: dict = field(default_factory=dict)

    def __hash__(self):
        return hash(self.to_json())

    def __eq__(self, other):
        return isinstance(other, TruthConfig) and hash(self) == hash(other)


TruthConfigs: TypeAlias = dict[str, TruthConfig]
NumberStr: TypeAlias = float | int | str
OptionalNumberStr: TypeAlias = NumberStr | None
OptionalListNumberStr: TypeAlias = list[NumberStr] | None
EQ: TypeAlias = tuple[float | int, float | int, float | int]


@dataclass
class AugmentationRule(DataClassSonusAIMixin):
    normalize: OptionalNumberStr = None
    pitch: OptionalNumberStr = None
    tempo: OptionalNumberStr = None
    gain: OptionalNumberStr = None
    eq1: OptionalListNumberStr = None
    eq2: OptionalListNumberStr = None
    eq3: OptionalListNumberStr = None
    lpf: OptionalNumberStr = None
    ir: OptionalNumberStr = None
    mixup: int = 1


@dataclass
class Augmentation(DataClassSonusAIMixin):
    normalize: float | None = None
    pitch: float | None = None
    tempo: float | None = None
    gain: float | None = None
    eq1: EQ | None = None
    eq2: EQ | None = None
    eq3: EQ | None = None
    lpf: float | None = None
    ir: int | None = None


@dataclass(frozen=True)
class UniversalSNRGenerator:
    is_random: bool
    _raw_value: float | str

    @property
    def value(self) -> float:
        if self.is_random:
            from .augmentation import evaluate_random_rule

            return float(evaluate_random_rule(str(self._raw_value)))

        return float(self._raw_value)


class UniversalSNR(float):
    def __new__(cls, value: float, is_random: bool = False):
        return float.__new__(cls, value)

    def __init__(self, value: float, is_random: bool = False) -> None:
        float.__init__(value)
        self._is_random = bool(is_random)

    @property
    def is_random(self) -> bool:
        return self._is_random


Speaker: TypeAlias = dict[str, str]


@dataclass
class TargetFile(DataClassSonusAIMixin):
    name: str
    samples: int
    class_indices: list[int]
    truth_configs: TruthConfigs
    class_balancing_augmentation: AugmentationRule | None = None
    level_type: str | None = None
    speaker_id: int | None = None

    @property
    def duration(self) -> float:
        from .constants import SAMPLE_RATE

        return self.samples / SAMPLE_RATE


@dataclass
class AugmentedTarget(DataClassSonusAIMixin):
    target_id: int
    target_augmentation_id: int


@dataclass
class NoiseFile(DataClassSonusAIMixin):
    name: str
    samples: int

    @property
    def duration(self) -> float:
        from .constants import SAMPLE_RATE

        return self.samples / SAMPLE_RATE


ClassCount: TypeAlias = list[int]

GeneralizedIDs: TypeAlias = str | int | list[int] | range


@dataclass
class GenMixData:
    targets: list[AudioT] | None = None
    target: AudioT | None = None
    noise: AudioT | None = None
    mixture: AudioT | None = None
    truth_t: list[TruthDict] | None = None
    segsnr_t: Segsnr | None = None


@dataclass
class GenFTData:
    feature: Feature | None = None
    truth_f: TruthDict | None = None
    segsnr: Segsnr | None = None


@dataclass
class ImpulseResponseData:
    name: str
    sample_rate: int
    data: AudioT

    @property
    def length(self) -> int:
        return len(self.data)


@dataclass
class ImpulseResponseFile:
    file: str
    tags: list[str]


@dataclass(frozen=True)
class SpectralMask(DataClassSonusAIMixin):
    f_max_width: int
    f_num: int
    t_max_width: int
    t_num: int
    t_max_percent: int


@dataclass(frozen=True)
class TruthParameter(DataClassSonusAIMixin):
    name: str
    parameters: int | None


@dataclass
class Target(DataClassSonusAIMixin):
    file_id: int
    augmentation: Augmentation

    @property
    def gain(self) -> float:
        # gain is used to back out the gain augmentation in order to return the target audio
        # to its normalized level when calculating truth (if needed).
        if self.augmentation.gain is None:
            return 1.0
        return round(10 ** (self.augmentation.gain / 20), ndigits=5)


Targets: TypeAlias = list[Target]


@dataclass
class Noise(DataClassSonusAIMixin):
    file_id: int
    augmentation: Augmentation


@dataclass
class Mixture(DataClassSonusAIMixin):
    name: str
    targets: list[Target]
    noise: Noise
    noise_offset: int
    samples: int
    snr: UniversalSNR
    spectral_mask_id: int
    spectral_mask_seed: int
    target_snr_gain: float = 1.0
    noise_snr_gain: float = 1.0

    @property
    def noise_id(self) -> int:
        return self.noise.file_id

    @property
    def target_ids(self) -> list[int]:
        return [target.file_id for target in self.targets]

    @property
    def target_augmentations(self) -> list[Augmentation]:
        return [target.augmentation for target in self.targets]

    @property
    def is_noise_only(self) -> bool:
        return self.snr < -96

    @property
    def is_target_only(self) -> bool:
        return self.snr > 96

    def target_gain(self, target_index: int) -> float:
        return (self.targets[target_index].gain if not self.is_noise_only else 0) * self.target_snr_gain


@dataclass(frozen=True)
class TransformConfig:
    length: int
    overlap: int
    bin_start: int
    bin_end: int
    ttype: str


@dataclass(frozen=True)
class FeatureGeneratorConfig:
    feature_mode: str
    truth_parameters: dict[str, int | None]


@dataclass(frozen=True)
class FeatureGeneratorInfo:
    decimation: int
    stride: int
    step: int
    feature_parameters: int
    ft_config: TransformConfig
    eft_config: TransformConfig
    it_config: TransformConfig


ASRConfigs: TypeAlias = dict[str, dict[str, Any]]


@dataclass
class MixtureDatabaseConfig(DataClassSonusAIMixin):
    asr_configs: ASRConfigs
    class_balancing: bool
    class_labels: list[str]
    class_weights_threshold: list[float]
    feature: str
    impulse_response_files: list[ImpulseResponseFile]
    mixtures: list[Mixture]
    noise_mix_mode: str
    noise_files: list[NoiseFile]
    num_classes: int
    spectral_masks: list[SpectralMask]
    target_files: list[TargetFile]


SpeechMetadata: TypeAlias = str | list[Interval] | None


class SnrFMetrics(NamedTuple):
    avg: float | None = None
    std: float | None = None
    db_avg: float | None = None
    db_std: float | None = None


class SnrFBinMetrics(NamedTuple):
    avg: np.ndarray | None = None
    std: np.ndarray | None = None
    db_avg: np.ndarray | None = None
    db_std: np.ndarray | None = None


class SpeechMetrics(NamedTuple):
    pesq: float | None = None
    csig: float | None = None
    cbak: float | None = None
    covl: float | None = None


class AudioStatsMetrics(NamedTuple):
    dco: float | None = None
    min: float | None = None
    max: float | None = None
    pkdb: float | None = None
    lrms: float | None = None
    pkr: float | None = None
    tr: float | None = None
    cr: float | None = None
    fl: float | None = None
    pkc: float | None = None


@dataclass
class MetricDoc:
    category: str
    name: str
    description: str


class MetricDocs(list[MetricDoc]):
    def __init__(self, __iterable: Iterable[MetricDoc]) -> None:
        super().__init__(item for item in __iterable)

    def __setitem__(self, __key: SupportsIndex, __value: MetricDoc) -> None:  # type: ignore[override]
        super().__setitem__(__key, __value)

    def insert(self, __index: SupportsIndex, __object: MetricDoc) -> None:
        super().insert(__index, __object)

    def append(self, __object: MetricDoc) -> None:
        super().append(__object)

    def extend(self, __iterable: Iterable[MetricDoc]) -> None:
        if isinstance(__iterable, type(self)):
            super().extend(__iterable)
        else:
            super().extend(item for item in __iterable)

    @property
    def pretty(self) -> str:
        max_category_len = ((max([len(item.category) for item in self]) + 9) // 10) * 10
        max_name_len = 2 + ((max([len(item.name) for item in self]) + 1) // 2) * 2
        categories: list[str] = []
        for item in self:
            if item.category not in categories:
                categories.append(item.category)

        result = ""
        for category in categories:
            result += f"{category}\n"
            result += "-" * max_category_len + "\n"
            for item in [sub for sub in self if sub.category == category]:
                result += f"  {item.name:<{max_name_len}}{item.description}\n"
            result += "\n"

        return result

    @property
    def names(self) -> set[str]:
        return {item.name for item in self}

from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Truth


def truth_function(mixdb: MixtureDatabase, m_id: int) -> list[Truth]:
    from sonusai.mixture import TruthDict
    from sonusai.mixture import truth_functions

    result: list[Truth] = []
    for target_index in range(len(mixdb.mixture(m_id).targets)):
        truth: TruthDict = {}
        target_file = mixdb.target_file(mixdb.mixture(m_id).targets[target_index].file_id)
        for name, config in target_file.truth_configs.items():
            try:
                truth[name] = getattr(truth_functions, config.function)(mixdb, m_id, target_index, config.config)
            except AttributeError as e:
                raise AttributeError(f"Unsupported truth function: {config.function}") from e
            except Exception as e:
                raise RuntimeError(f"Error in truth function '{config.function}': {e}") from e

        result.append(truth)

    return result


def get_truth_indices_for_mixid(mixdb: MixtureDatabase, mixid: int) -> list[int]:
    """Get a list of truth indices for a given mixid."""
    indices: list[int] = []
    for target_id in [target.file_id for target in mixdb.mixture(mixid).targets]:
        indices.append(*mixdb.target_file(target_id).class_indices)

    return sorted(set(indices))


def truth_stride_reduction(truth: Truth, function: str) -> Truth:
    """Reduce stride dimension of truth.

    :param truth: Truth data [frames, stride, truth_parameters]
    :param function: Truth stride reduction function name
    :return: Stride reduced truth data [frames, stride or 1, truth_parameters]
    """
    import numpy as np

    if truth.ndim != 3:
        raise ValueError("Invalid truth shape")

    if function == "none":
        return truth

    if function == "max":
        return np.max(truth, axis=1, keepdims=True)

    if function == "mean":
        return np.mean(truth, axis=1, keepdims=True)

    if function == "first":
        return truth[:, 0, :].reshape((truth.shape[0], 1, truth.shape[2]))

    raise ValueError(f"Invalid truth stride reduction function: {function}")

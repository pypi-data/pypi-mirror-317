from functools import lru_cache
from typing import Any


@lru_cache
def load_object(name: str) -> Any:
    """Load an object from a pickle file (with LRU caching)"""
    import pickle
    from os.path import exists

    if exists(name):
        with open(name, "rb") as f:
            return pickle.load(f)  # noqa: S301

    raise FileNotFoundError(name)

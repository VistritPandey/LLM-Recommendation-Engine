import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if not a.any() or not b.any():
        return 0.0
    return float(a @ b) 
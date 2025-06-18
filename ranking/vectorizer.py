import numpy as np
from typing import List


def to_vec(tags: List[str], enum_list: List[str]):
    vec = np.zeros(len(enum_list), dtype=np.float32)
    for tag in tags:
        try:
            idx = enum_list.index(tag)
            vec[idx] = 1.0
        except ValueError:
            continue

    norm = np.linalg.norm(vec)
    return vec / norm if norm else vec 
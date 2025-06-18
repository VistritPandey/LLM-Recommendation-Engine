import numpy as np
from ranking.vectorizer import to_vec
from ranking.scorer import cosine_similarity


def test_similarity():
    enums = ["x", "y", "z"]
    a = to_vec(["x", "y"], enums)
    b = to_vec(["x"], enums)
    score = cosine_similarity(a, b)
    assert np.isclose(score, 0.7071067690849304) 
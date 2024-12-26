import numpy as np
from math import isclose

EPSILON = 1e-9


def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)


def test_cosine_similarity():
    a = [1, 2, 3]
    b = [4, 5, 6]
    assert isclose(cosine_similarity(a, b), 0.97, rel_tol=EPSILON)

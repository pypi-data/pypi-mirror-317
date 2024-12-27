import numpy as np


def discrimination_index(scores, responses, top_percent=27):
    if len(scores) != len(responses):
        raise ValueError("Scores and responses must have the same length.")
    n_students = len(scores)
    n_top = int(np.ceil(top_percent / 100 * n_students))

    sorted_indices = np.argsort(scores)
    lower_group = sorted_indices[:n_top]
    upper_group = sorted_indices[-n_top:]
    p_upper = np.mean([responses[i] for i in upper_group])
    p_lower = np.mean([responses[i] for i in lower_group])
    return p_upper - p_lower

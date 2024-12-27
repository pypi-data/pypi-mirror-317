#!/usr/bin/env python3

import numpy as np

DEBUG = True


def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                insert = dp[i][j - 1] + 1
                delete = dp[i - 1][j] + 1
                replace = dp[i - 1][j - 1] + (2 if s1[i - 1] != s2[j - 1] else 0)
                dp[i][j] = min(insert, delete, replace)

    if DEBUG:
        char_s1 = ["#", " "] + list(s1)
        char_s2 = [[" "] + list(s2)]

        df = np.array(char_s2 + dp)
        df = np.insert(df, 0, char_s1, axis=1)
        print(df)

    return dp[m][n]


def levenshtein_distance(s1, s2):
    l1 = len(s1)
    l2 = len(s2)

    dp = [[0] * (l2 + 1) for _ in range(l1 + 1)]
    for i in range(l1 + 1):
        dp[i][0] = i

    for j in range(l2 + 1):
        dp[0][j] = j

    for i in range(1, l1 + 1):
        for j in range(1, l2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                insert = dp[i][j - 1] + 1
                delete = dp[i - 1][j] + 1
                replace = dp[i - 1][j - 1] + 1
                dp[i][j] = min(insert, delete, replace)

    return dp[l1][l2]


def __test_edit_distance():
    s1 = "execution"
    s2 = "intention"
    assert edit_distance(s1, s2) == 8


def __test_levenshtein_distance():
    s1 = "execution"
    s2 = "intention"
    assert levenshtein_distance(s1, s2) == 5

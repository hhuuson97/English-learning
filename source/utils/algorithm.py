import logging

__author__ = 'son.hh'

from typing import List, Union

_logger = logging.getLogger(__name__)


# Find the longest common words in order and return the uncommon words in arr1
def longest_common_words(arr1, arr2):
    m = len(arr1)
    n = len(arr2)

    dp = [[[] for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if arr1[i-1][2] == arr2[j-1][2]:
                dp[i][j] = list(dp[i - 1][j - 1]) + [arr1[i-1][2]]
            else:
                if len(dp[i][j-1]) > len(dp[i-1][j]):
                    dp[i][j] = list(dp[i][j-1])
                else:
                    dp[i][j] = list(dp[i-1][j])
    no_matches = []
    i = 0
    for w in arr1:
        if i < len(dp[m][n]) and dp[m][n][i] == w[2]:
            i += 1
        else:
            no_matches.append(w)
    return dp[m][n], no_matches

from factory_sdk.dto.model import Token, GeneratedToken
from typing import List, Dict


def TokenLevensthein(
    label_tokens: List[Token], generated_tokens: List[GeneratedToken]
) -> Dict[str, float]:
    # Extract the text from both label_tokens and generated_tokens
    label_text = [token.text for token in label_tokens]
    generated_text = [token.text for token in generated_tokens]

    # Compute the Levenshtein distance between the two token sequences
    lev_distance = levenshtein(label_text, generated_text)

    # Normalize the distance into a score between 0 and 1
    max_len = max(len(label_text), len(generated_text))
    if max_len == 0:  # If both are empty, consider it a perfect match
        levenshtein_score = 1.0
    else:
        levenshtein_score = 1 - (lev_distance / max_len)

    # Return the Levenshtein score as a dictionary
    return {"score": levenshtein_score}


# Helper function to compute Levenshtein distance
def levenshtein(seq1: List[str], seq2: List[str]) -> int:
    # Initialize a matrix to store the distances
    n, m = len(seq1), len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Fill the first row and column
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    # Compute the distances
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

    # The final distance is in the bottom-right cell
    return dp[n][m]

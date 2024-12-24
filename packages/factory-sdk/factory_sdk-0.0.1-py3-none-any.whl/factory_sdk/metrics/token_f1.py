from factory_sdk.dto.model import Token, GeneratedToken
from typing import List, Dict
from collections import Counter


def TokenF1(
    label_tokens: List[Token], generated_tokens: List[GeneratedToken]
) -> Dict[str, float]:
    # Extract text from the tokens
    label_text = [token.text for token in label_tokens]
    generated_text = [token.text for token in generated_tokens]

    # Count the occurrences of each token in both lists
    label_counter = Counter(label_text)
    generated_counter = Counter(generated_text)

    # Compute the number of true positives (correct predictions)
    true_positives = sum((label_counter & generated_counter).values())

    # Compute precision and recall
    if len(generated_text) == 0:
        precision = 0.0
    else:
        precision = true_positives / len(generated_text)

    if len(label_text) == 0:
        recall = 0.0
    else:
        recall = true_positives / len(label_text)

    # Compute F1 score
    if precision + recall == 0:
        f1_score = 0.0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    # Return the scores as a dictionary
    return {"precision": precision, "recall": recall, "score": f1_score}

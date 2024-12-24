from factory_sdk.dto.model import Token, GeneratedToken
from typing import List, Dict


def TokenAccuracy(
    label_tokens: List[Token], generated_tokens: List[GeneratedToken]
) -> Dict[str, float]:
    # Determine the maximum length of the two lists
    max_len = max(len(label_tokens), len(generated_tokens))

    # Pad the shorter list with a padding token
    pad_token = Token("<PAD>")
    label_tokens_padded = label_tokens + [pad_token] * (max_len - len(label_tokens))
    generated_tokens_padded = generated_tokens + [
        GeneratedToken("<PAD>", logprob=0.0, rank=0)
    ] * (max_len - len(generated_tokens))

    # Count the number of correct predictions
    correct_predictions = 0
    for label, generated in zip(label_tokens_padded, generated_tokens_padded):
        if label.text == generated.text:
            correct_predictions += 1

    # Calculate accuracy
    accuracy = correct_predictions / max_len

    # Return the accuracy score as a dictionary
    return {"score": accuracy}

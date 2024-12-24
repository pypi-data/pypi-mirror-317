from factory_sdk.dto.model import Token, GeneratedToken
from typing import List, Dict
  
def ExactMatch(
    label_tokens: List[Token], generated_tokens: List[GeneratedToken]
) -> Dict[str, float]:
    # Check if the sequences match exactly
    if len(label_tokens) != len(generated_tokens):
        return {"exact_match": 0.0}

    # Compare the tokens one by one
    for label, generated in zip(label_tokens, generated_tokens):
        if label.text != generated.text:
            return {"exact_match": 0.0}

    # If all tokens match, return exact match as 1.0
    return {"score": 1.0}

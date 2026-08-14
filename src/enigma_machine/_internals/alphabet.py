"""Module containing alphabet related functionality."""

ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def normalize_letter(alph_letter: str) -> str:
    """Convert it to uppercase and validate that it is one letter in the alphabet."""
    if len(alph_letter) != 1:
        raise ValueError(f"{alph_letter} must be one character.")

    alph_letter_upper = alph_letter.upper()
    if alph_letter_upper not in ENGLISH_ALPHABET:
        raise ValueError(f"{alph_letter} is not contained in the alphabet [A-Z].")

    return alph_letter_upper

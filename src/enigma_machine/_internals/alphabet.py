"""Module containing alphabet related functionality."""

ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def normalize_letter(alph_letter: str) -> str:
    """Normalize letter by converting it to uppercase and validate if it's in the alphabet."""
    if len(alph_letter) != 1:
        raise ValueError('alph_letter should be one character.')

    alph_letter_upper = alph_letter.upper()
    if alph_letter_upper not in ENGLISH_ALPHABET:
        raise ValueError('alph_letter is not contained in the alphabet [A-Z].')

    return alph_letter_upper

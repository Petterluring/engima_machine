"""Module containing alphabet related functionality."""

from enum import Enum

ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Keyboard(Enum):
    LATIN_ALPHABET   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    GERMAN_ALPHABET  = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß"

    def __init__(self, layout: str) -> None:
        # TODO: validate if layout len is even?
        self.layout = layout

    def __len__(self) -> int:
        return len(self.value)


def normalize_letter(alph_letter: str, alphabet: str = Keyboard.LATIN_ALPHABET.layout) -> str:
    """Convert alph_letter to uppercase and validate that it is one letter in the alphabet."""
    if len(alph_letter) != 1:
        raise ValueError(f"{alph_letter} must be one character.")

    alph_letter_upper = alph_letter.upper()
    if alph_letter_upper not in alphabet:
        raise ValueError(f"{alph_letter} is not contained in the {alphabet}.")

    return alph_letter_upper

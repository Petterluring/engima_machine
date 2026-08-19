"""Module containing alphabet related functionality."""

from enum import Enum

ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Alphabet(Enum):
    """Defines the set of characters that can be used for encryption in terms of alphabets.

    This allows the user to encrypt messages using different input layouts such as the latin alphabet.
    """
    LATIN_ALPHABET   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    GERMAN_ALPHABET  = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß"

    def __len__(self) -> int:
        return len(self.value)


def strip_and_upper(value: str) -> str:
    """Wrapper for strip and upper string methods.

    Handles special cases such as when value contains ß, which incorrectly
    converts it to SS when applying .upper().
    """
    return value.strip().upper().replace("SS", "ß")


def normalize_letter(alph_letter: str, alphabet: str = Alphabet.LATIN_ALPHABET.value) -> str:
    """Convert alph_letter to uppercase and validate that it is one letter in the alphabet."""
    if len(alph_letter) != 1:
        raise ValueError(f"{alph_letter} must be one character.")

    alph_letter_upper = strip_and_upper(alph_letter)
    if alph_letter_upper not in alphabet:
        raise ValueError(f"{alph_letter} is not contained in the {alphabet}.")

    return alph_letter_upper

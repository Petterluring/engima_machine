"""Module containing alphabet related functionality."""

from enum import Enum


class Keyboard(Enum):
    """Defines the set of keyboards that can be used in the Enigma machine."""
    LATIN_ALPHABET   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    SWEDISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    GERMAN_ALPHABET  = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß"

    def __init__(self, alphabet: str) -> None:
        self.alphabet = alphabet

    def __len__(self) -> int:
        return len(self.value)


def normalize_letter(alph_letter: str, keyboard: Keyboard = Keyboard.LATIN_ALPHABET) -> str:
    """Convert alph_letter to uppercase and validate that it is one letter on the keyboard."""
    if len(alph_letter) != 1:
        raise ValueError(f"{alph_letter} must be one character.")

    alph_letter_upper = alph_letter.upper()
    if alph_letter_upper not in keyboard.alphabet:
        raise ValueError(f"{alph_letter} is not contained in the alphabet {keyboard.value}.")

    return alph_letter_upper

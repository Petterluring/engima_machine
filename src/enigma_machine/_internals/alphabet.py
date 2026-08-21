"""Module containing alphabet related functionality."""

from enum import Enum
from re import compile

ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

_REPLACE = {
    "SS": "ß"
}

def upper(value: str) -> str:
    """Wrapper for upper method.

    Handles special cases such as when value contains ß, which incorrectly
    converts it to SS.
    """
    value_upper = value.upper()
    for k, v in _REPLACE.items():
        value_upper = value_upper.replace(k, v)
    return value_upper

class Alphabet(Enum):
    """Defines the set of characters that can be used for encryption in terms of alphabets.

    This allows the user to encrypt messages using different input layouts such as the latin alphabet.
    """
    LATIN_ALPHABET   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    GERMAN_ALPHABET  = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß"

    def normalize(self, letter: str) -> str:
        """Convert alph_letter to uppercase and validate that it is one letter in the alphabet."""
        if len(letter) != 1:
            raise ValueError(f"{letter} must be one character.")

        letter_upper = upper(letter)
        if letter_upper not in self.value:
            raise ValueError(f"{letter_upper} is not contained in {self.value}.")

        return letter_upper


    def __len__(self) -> int:
        return len(self.value)

def normalize_letter(alph_letter: str, alphabet: str = Alphabet.LATIN_ALPHABET.value) -> str:
    """Convert alph_letter to uppercase and validate that it is one letter in the alphabet."""
    if len(alph_letter) != 1:
        raise ValueError(f"{alph_letter} must be one character.")

    alph_letter_upper = upper(alph_letter)
    if alph_letter_upper not in alphabet:
        raise ValueError(f"{alph_letter} is not contained in the {alphabet}.")

    return alph_letter_upper

_REGEX_PATTERNS = {
    Alphabet.LATIN_ALPHABET: r"[A-Z]{26}",
    Alphabet.GERMAN_ALPHABET: r"[A-ZÄÖÜß]{30}"
}

def validate_alph_permutation(value: str) -> tuple[str, str]:
    """Validate a permutation against a predefined alphabet and return that alphabet and the permutation in uppercase.

    Args:
        value: str - The permutation to validate.

    Returns:
        tuple[str, str] - (alphabet, permutation)
    """
    value_upper = upper(value)

    for alphabet in Alphabet:
        regex_pattern = _REGEX_PATTERNS[alphabet]
        pattern = compile(regex_pattern)

        if bool(pattern.fullmatch(value_upper)):
            if len(alphabet.value) != len(set(value_upper)):
                break
            return (alphabet.value, value_upper)

    raise ValueError(
        f"{value_upper} must be a permutation of one of the following alphabets: " +
        ", ".join([alphabet.value for alphabet in Alphabet])
    )

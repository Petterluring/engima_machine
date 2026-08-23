"""Module containing alphabet related functionality."""

from enum import Enum
from random import shuffle

ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

_REPLACE = {
    "SS": "ẞ"
}

def upper(value: str) -> str:
    """Wrapper for string.upper() method.

    Handles special cases such as when value contains ß, which incorrectly
    converts it to SS.
    """
    value_upper = value.upper()
    for k, v in _REPLACE.items():
        value_upper = value_upper.replace(k, v)
    return value_upper

class Alphabet(Enum):
    """Defines different ranges of letters that are subject for encryption.

    Ranges ared defined by alphabets, which physically represent different keyboard layout on the enigma machine.
    For each alphabet, the class provides functionality such as validation and generation of alphabet permutations,
    normalization of letters, etc (see details in methods).
    """
    LATIN_ALPHABET   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    GERMAN_ALPHABET  = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ"



    def normalize(self, letter: str) -> str:
        """Convert letter to uppercase and validate that it is one letter in the alphabet.

        Args:
            letter: str - Letter to normalize.

        Returns:
            str - Letter in uppercase.

        Raises:
            ValueError: If letter is not one character or not contained in the alphabetic letters.
        """
        if len(letter) != 1:
            raise ValueError(f"{letter} must be one character.")

        letter_upper = upper(letter)
        if letter_upper not in self.value:
            raise ValueError(f"{letter_upper} is not contained in {self.value}.")

        return letter_upper

    def index(self, letter: str) -> int:
        """Return the index of 'letter' in the alphabet."""
        return self.value.index(letter)

    def validate_permutation(self, value: str) -> bool:
        """Validate that 'value' is a permutation of the alphabet.

        Args:
            value: str - Chosen permutation to validate.

        Returns:
            bool - True if valid, False otherwise.

        """
        return set(value) == set(self.value)

    @staticmethod
    def infer_alphabet_and_normalize(permutation: str) -> tuple[Alphabet, str]:
        """Normalize 'permutation' by converting it to uppercase and return this value along with the alphabet from which it is a permutation of.

        Args:
            permutation: str - The permutation subject to normalization.

        Returns:
            tuple[Alphabet, str] - The inferred alphabet and the normalized permutation.

        Raises:
            ValueError - If the permutation validation fails for all alphabets.
        """  # noqa: E501
        permutation_upper = upper(permutation)
        for alphabet in Alphabet:
            if alphabet.validate_permutation(permutation_upper):
                return alphabet, permutation_upper
        raise ValueError("permutation value must be one permutation of the following alphabets: " +
                         ", ".join(alphabet.value for alphabet in Alphabet))


    def random_permutation(self) -> str:
        """Return a random permutation of the alphabet."""
        chars = list(self.value)
        shuffle(chars)
        return "".join(chars)

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, index: int) -> str:
        return self.value[index]

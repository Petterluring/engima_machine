"""Module for representing the wiring inside a rotor in the Enigma machine.

The wiring of a rotor defines a mapping between letters in the alphabet. Specifically, a wiring maps the alphabet
[A-Z] to a permutation of [A-Z]. For instance, a wiring of
"EKMFLGDQVZNTOWYHXUSPAIBRCJ" means that A -> E, B -> K, C -> M, and so on.
"""

from dataclasses import dataclass

from bidict import bidict

from enigma_machine.utils.constants import ENGLISH_ALPHABET as ALPHABET
from enigma_machine.utils.regex import build_regex_pattern

from .utils import _normalize_letter

REGEX_PATTERN = f"[A-Z]{{{26}}}"
REGEX_MATCHER = build_regex_pattern(REGEX_PATTERN)

@dataclass(frozen=True, slots=True)
class _Permutation:
    """Validates a permutation of the alphabet by ensuring it contains 26 unique letters."""

    value: str

    def __post_init__(self) -> None:
        """Validate the permutation and convert it to uppercase."""
        value = self.value.strip().upper()

        # Require value to only include alphabetic letters of length 26
        if not REGEX_MATCHER(value):
            raise ValueError(f"{value} must match {REGEX_PATTERN} regex pattern.")

        # Require the letters in value to be unique
        if not len(value) == len(set(value)):
            raise ValueError(f"{value} must have unique letters.")

        object.__setattr__(self, "value", value)


class Wiring:
    """Represents a wiring inside a rotor.

    The wiring is represented by a permutation of the alphabet, such as QWZJTYRLPFNSVXCHAMOEGKUBID.
    This means that A maps to (->) Q, B -> W, C -> C, and so forth.

    Attributes:
        value: str - a 26 character long string containing a permutation of the alphabet [A-Z].
    """

    def __init__(self, value: str) -> None:
        _permutation = _Permutation(value=value)
        self._wiring = bidict(dict(zip(ALPHABET, _permutation.value, strict=False)))

    def encode(self, alph_letter: str, reverse: bool = False) -> str:
        """Return the encoded letter that is wired to 'letter'.

        For instance, if the letter A is wired to C, then this function returns C for input letter A.

        Args:
            alph_letter: str - a single alphabet letter [A-Z]
            reverse: bool - Reverses the mapping, meaning that input letter C yields A in our example.

        Returns:
            str - a single character string representing the encoded letter.

        """
        letter_norm = _normalize_letter(alph_letter)

        encoded_letter = self._wiring.get(letter_norm) if not reverse else self._wiring.inverse.get(letter_norm)

        if encoded_letter is None:
            raise KeyError(f"{letter_norm} has no encoding")

        return encoded_letter

    @property
    def permutation(self) -> str:
        """Return the wiring of the alphabet."""
        return "".join(v for v in self._wiring.values())

    def __len__(self) -> int:
        return len(self._wiring)

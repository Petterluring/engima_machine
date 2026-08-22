
"""Module containing the Reflector class."""
from ..alphabet.alphabet import normalize_letter, validate_alph_permutation


class Reflector:
    """Represents the reflector in the enigma machine.

    The reflector wires alphabetic letters in unique pairs with bidirectional encoding.
    A unique pair means that two letters in a pair cannot be found in a different pair.

    The wiring is defined by a permutation of a supported alphabet where the first half of the
    permutation is wired/mapped to the second half. For instance, the permutation QWZJTYRLPFNSVXCHAMOEGKUBID
    would be wired as follows:
                        QWZJTYRLPFNSV
                        XCHAMOEGKUBID

    See alphabet.py for supported alphabets.
    """
    def __init__(self, permutation: str) -> None:
        """Class initializer.

        Args:
            permutation: str - A permutation of a supported alphabet.
        """
        alphabet, valid_permutation = validate_alph_permutation(value=permutation)

        self._alphabet = alphabet.value
        self._wiring = valid_permutation

    def encode(self, alph_letter: str) -> str:
        """Return the letter that is wired to 'alph_letter'.

        For instance, if the input letter A is wired to C, return C.

        Args:
            alph_letter: str - An alphabetic letter contained in... .

        Returns:
            str - String representing the encoded letter.

        """
        norm_letter = normalize_letter(alph_letter)
        divider = len(self._wiring) // 2
        i = self._wiring.index(norm_letter)
        return self._wiring[i + divider] if i < divider else self._wiring[i - divider]

    @property
    def permutation(self) -> str:
        """Return the wiring of the alphabet."""
        return "".join(self.encode(letter) for letter in self._alphabet)

    @property
    def alphabet(self) -> str:
        """Return the alphabet."""
        return self._alphabet

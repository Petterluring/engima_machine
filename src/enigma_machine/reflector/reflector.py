
"""Module containing the Reflector class."""
from ..alphabet.alphabet import Alphabet


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
    def __init__(self, wiring: str) -> None:
        """Class initializer.

        Args:
            wiring: str - A wiring of a supported alphabet.
        """
        alphabet, norm_wiring = Alphabet.infer_alphabet_and_normalize(wiring)

        self._alphabet = alphabet
        self._wiring = norm_wiring

    def encode(self, alph_letter: str, normalize: bool = True) -> str:
        """Return the letter that is wired to 'alph_letter'.

        For instance, if the input letter A is wired to C, return C.

        Args:
            alph_letter: str - Alphabetic letter to encode.
            normalize: bool  - Flag for normalizing input letter.

        Returns:
            str - String representing the encoded letter.

        """
        alph_letter = self._alphabet.normalize(alph_letter) if normalize else alph_letter
        divider = len(self._wiring) // 2
        i = self._wiring.index(alph_letter)
        return self._wiring[i + divider] if i < divider else self._wiring[i - divider]

    @property
    def permutation(self) -> str:
        """Return the wiring of the alphabet."""
        return "".join(self.encode(letter) for letter in self._alphabet.value)

    @property
    def alphabet(self) -> Alphabet:
        """Return the alphabet."""
        return self._alphabet

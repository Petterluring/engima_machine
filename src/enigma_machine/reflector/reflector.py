
"""Module containing the Reflector class."""
from ..alphabet.alphabet import Alphabet


class Reflector:
    """Represents the reflector in the enigma machine.

    The reflector wires alphabetic letters in unique pairs with bidirectional encoding.
    A unique pair means that two letters in a pair cannot be found in a different pair.

    The wiring is defined by a permutation of an alphabetic set of letters where the first half
    is wired/mapped with the second half. For instance, the permutation QWZJTYRLPFNSVXCHAMOEGKUBID
    is wired as follows:
                        QWZJTYRLPFNSV
                        XCHAMOEGKUBID
    See Alphabet enum for supported letter sets.
    """
    def __init__(self, wiring: str) -> None:
        """Class initializer.

        Args:
            wiring: str - Permutation of an alphabetic set of letters defining the wiring of the reflector.
        """
        alphabet, norm_wiring = Alphabet.infer_alphabet_and_normalize(wiring)

        self._alphabet = alphabet
        self._wiring = norm_wiring

    def encode(self, alph_letter: str, normalize: bool = True) -> str:
        """Return the letter wired to 'alph_letter'.

        For instance, if input letter A is wired to C, return C.

        Args:
            alph_letter: Alphabetic letter to encode.
            normalize:   Flag stating if input should be normalized before encoded.
        """
        alph_letter = self._alphabet.normalize(alph_letter) if normalize else alph_letter
        divider = len(self._wiring) // 2
        i = self._wiring.index(alph_letter)
        return self._wiring[i + divider] if i < divider else self._wiring[i - divider]

    @property
    def permutation(self) -> str:
        """Return the wiring."""
        return "".join(self.encode(letter) for letter in self._alphabet.value)

    @property
    def alphabet(self) -> Alphabet:  # noqa: D102
        return self._alphabet

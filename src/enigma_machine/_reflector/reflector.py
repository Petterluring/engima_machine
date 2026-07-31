
"""Module containing the Reflector class."""
from bidict import bidict

from .._internals.alphabet import ENGLISH_ALPHABET
from .._internals.permutation import validate_alph_permutation


class Reflector:
    """Represents the reflector in the enigma machine.

    The reflector wires the alphabetic letters [A-Z] in 13 unique pairs that has a bidirectional encoding.
    """
    def __init__(self, permutation: str) -> None:
        """Class initializer.

        Args:
            permutation: str - A permutation of the alphabet [A-Z]. Example: QWZJTYRLPFNSVXCHAMOEGKUBID.
                               The first half of the permutation is wired accordingly with the second half,
                               meaning that QWZJTYRLPFNSVXCHAMOEGKUBID is encoded as:
                                                QWZJTYRLPFNSV
                                                XCHAMOEGKUBID
        """
        valid_permutation = validate_alph_permutation(value=permutation)
        first_half, second_half = valid_permutation[:13], valid_permutation[13:26]
        self._wiring = bidict(dict(zip(first_half, second_half, strict=True)))

    def encode(self, alph_letter: str) -> str:
        """Return the encoded letter that is wired to 'alph_letter'.

        For instance, if the letter A is wired to C, then this function returns C for input letter A.

        Args:
            alph_letter: str - a single alphabet letter [A-Z]

        Returns:
            str - a single character string representing the encoded letter.

        """
        encoded_letter = self._wiring.get(alph_letter)

        # mypy is ignored here as Reflector class is a component of the Rotor class which
        # ensures that alph_letter exists in _wiring dict before parsed as an argument.
        return encoded_letter if encoded_letter is not None else self._wiring.inverse.get(alph_letter) # type: ignore[return-value]

    @property
    def permutation(self) -> str:
        """Return the wiring of the alphabet."""
        return "".join(self.encode(letter) for letter in ENGLISH_ALPHABET)

    def __len__(self) -> int:
        return len(self._wiring)

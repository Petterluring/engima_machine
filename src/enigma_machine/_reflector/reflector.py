
"""Module containing the Reflector class."""
from bidict import bidict

from .._internals.keyboard import ENGLISH_ALPHABET
from .._internals.permutation import validate_alph_permutation


class Reflector:
    """Represents the reflector in the enigma machine.

    The reflector wires the alphabetic letters [A-Z] in 13 unique pairs with bidirectional encoding.
    A unique pair means that two letters in a pair cannot be found in a different pair.
    """
    def __init__(self, permutation: str) -> None:
        """Class initializer.

        Args:
            permutation: str - A permutation of the alphabet [A-Z]. Example: QWZJTYRLPFNSVXCHAMOEGKUBID.
                               The first half of the permutation is wired with the second half,
                               meaning that QWZJTYRLPFNSVXCHAMOEGKUBID is encoded as:
                                                QWZJTYRLPFNSV
                                                XCHAMOEGKUBID
        """
        alphabet, valid_permutation = validate_alph_permutation(value=permutation)

        alph_len = len(alphabet)
        first_half, second_half = valid_permutation[:alph_len//2], valid_permutation[alph_len//2:alph_len]
        self._wiring = bidict(dict(zip(first_half, second_half, strict=True)))

    def encode(self, alph_letter: str) -> str:
        """Return the letter that is wired to 'alph_letter'.

        For instance, if the input letter A is wired to C, return C.

        Args:
            alph_letter: str - An alphabetic letter contained in [A-Z].

        Returns:
            str - String representing the encoded letter.

        """
        encoded_letter = self._wiring.get(alph_letter)

        # mypy is ignored here as Reflector class is a component of the Machine class (see machine.py) which
        # ensures that alph_letter exists in _wiring dict before it is passed to this method.
        return encoded_letter if encoded_letter is not None else self._wiring.inverse.get(alph_letter) # type: ignore[return-value]

    @property
    def permutation(self) -> str:
        """Return the wiring of the alphabet."""
        return "".join(self.encode(letter) for letter in ENGLISH_ALPHABET)

    def __len__(self) -> int:
        return len(self._wiring)

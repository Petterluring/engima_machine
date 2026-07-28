
"""Module containing the Reflector class."""
from .._internals.alphabet import ENGLISH_ALPHABET
from .._internals.permutation import Permutation


class Reflector:
    """Represents the reflector in the enigma machine.

    The reflector is simply a one-way wiring, mapping alphabetic letters [A-Z] to a permutation of [A-Z].
    """
    def __init__(self, permutation: str) -> None:
        """Class initializer.

        Args:
            permutation: str - A permutation of the alphabet [A-Z]. Example: QWZJTYRLPFNSVXCHAMOEGKUBID.
        """
        _permutation = Permutation(value=permutation)
        self._wiring = dict(zip(ENGLISH_ALPHABET, _permutation.value, strict=True))

    def encode(self, alph_letter: str) -> str:
        """Return the encoded letter that is wired to 'alph_letter'.

        For instance, if the letter A is wired to C, then this function returns C for input letter A.

        Args:
            alph_letter: str - a single alphabet letter [A-Z]

        Returns:
            str - a single character string representing the encoded letter.

        """
        encoded_letter = self._wiring.get(alph_letter)

        return encoded_letter # type: ignore[return-value]
                              # mypy is ignored here as Reflector class is a component of the Rotor class which
                              # ensures that alph_letter exists in _wiring dict before parsed as an argument.

    @property
    def permutation(self) -> str:
        """Return the wiring of the alphabet."""
        return "".join(v for v in self._wiring.values())

    def __len__(self) -> int:
        return len(self._wiring)

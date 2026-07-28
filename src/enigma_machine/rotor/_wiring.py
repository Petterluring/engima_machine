"""Module containing the Wiring class."""

from bidict import bidict

from .._internals.alphabet import ENGLISH_ALPHABET
from .._internals.permutation import Permutation


class Wiring:
    """Represents a wiring inside a rotor.

    The wiring is represented by a permutation of the alphabet, such as QWZJTYRLPFNSVXCHAMOEGKUBID.
    This means that A maps to (->) Q, B -> W, C -> Z, and so forth. A wiring is bidirectional, meaning that
    Q -> A, W -> B, Z -> C, and so on.
    """

    def __init__(self, permutation: str) -> None:
        """Class initializer.

        Args:
            permutation: str - A permutation of the alphabet [A-Z]. Example: QWZJTYRLPFNSVXCHAMOEGKUBID.
        """
        _permutation = Permutation(value=permutation)
        self._wiring = bidict(dict(zip(ENGLISH_ALPHABET, _permutation.value, strict=True)))

    def encode(self, alph_letter: str, reverse: bool = False) -> str:
        """Return the encoded letter that is wired to 'letter'.

        For instance, if the letter A is wired to C, then this function returns C for input letter A.

        Args:
            alph_letter: str - a single alphabet letter [A-Z]
            reverse: bool - Reverses the mapping, meaning that input letter C yields A in our example.

        Returns:
            str - a single character string representing the encoded letter.

        """
        encoded_letter = self._wiring.get(alph_letter) if not reverse else self._wiring.inverse.get(alph_letter)

        return encoded_letter # type: ignore[return-value]
                              # mypy is ignored here as Wiring class is a component of the Rotor class which ensures
                              # that alph_letter exists in _wiring bidict before parsed as an argument.

    @property
    def permutation(self) -> str:
        """Return the wiring of the alphabet."""
        return "".join(v for v in self._wiring.values())

    def __len__(self) -> int:
        return len(self._wiring)

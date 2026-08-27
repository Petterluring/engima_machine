"""Module containins the Plugboard class."""

from ..alphabet.alphabet import Alphabet
from ..alphabet.errors import InternalStateError
from ..config import PlugboardConfig


class Plugboard:
    """Represents the plugboard in the enigma machine.

    The plugboard exposes a number of outlets, each representing an alphabetic letter, which
    the user can connect in pairs using cords. The connections define bidirectional encoding rules stating
    which letter a given input should be substituted with. A letter simply encodes to itself when it has no cord
    connection.


    Example:
        Suppose A is connected to G and the user enters A, then A is encoded as G which becomes
        the entering letter in the rotor set and vice versa.
    """

    def __init__(self,
        *cords: tuple[str, str],
        alphabet: Alphabet = Alphabet.LATIN_ALPHABET
    ) -> None:
        """Class initializer.

        Args:
            *cords:   A cord is represented as a pair of letters. Example: ("A", "G").
            alphabet: Defines the set of letters that can be connected.
        """
        self._mappings: dict[str, str] = {}
        self._alphabet: Alphabet = alphabet

        if cords:
            max_pairs = self._max_pairs
            if len(cords) > max_pairs:
                raise ValueError(f"At most {max_pairs} cords can be used simultanously in the plugboard")
            for cord in cords:
                self.add_cord(cord)

    @classmethod
    def from_config(cls, config: PlugboardConfig) -> Plugboard:
        """Return Plugboard instance based on config."""
        return cls(
            *config.cords,
            alphabet=Alphabet[config.alphabet]
        )

    def encode(self, alph_letter: str, normalize: bool = True) -> str:
        """Encode a letter using the given plugboard configuration and return the result.

        Args:
            alph_letter: Letter in the alphabet.
            normalize:   Flag stating if the input letter should be normalized before encoded.
        """
        alph_letter = self._alphabet.normalize(alph_letter) if normalize else alph_letter

        encoding = self._mappings.get(alph_letter)
        if encoding is not None:
            return encoding
        encoding = self._mappings.get(alph_letter)
        if encoding is not None:
            return encoding

        return alph_letter

    def add_cord(self, cord: tuple[str, str]) -> None:
        """Connect a new cord to the plugboard.

        Args:
            cord: Represented as a pair of letters. Example: ("A", "G").
        """
        pairs = self._max_pairs
        if len(self) == pairs:
            raise InternalStateError(f"At most {pairs} cords can be used simultanously in the plugboard")

        a1, a2 = self._normalize_cord(cord)

        if a1 in self._mappings or a2 in self._mappings:
            raise ValueError(f"{a1} or {a2} are already connected by a cord.")

        self._mappings[a1] = a2
        self._mappings[a2] = a1

    def remove_cord(self, cord: tuple[str, str]) -> None:
        """Remove a cord from the plugboard.

        Args:
            cord: Represented as a pair of letters. Example: ("A", "G").
        """
        a1, a2 = self._normalize_cord(cord)

        if self._mappings.get(a1) == a2 and self._mappings.get(a2) == a1:
            del self._mappings[a1]
            del self._mappings[a2]

    def cord_exists(self, cord: tuple[str, str]) -> bool:
        """Return true if the cord (c1, c2) or (c2, c1) exists, false otherwise.

        Args:
            cord: Represented as a pair of letters. Example: ("A", "G").
        """
        a1, a2 = self._alphabet.normalize(cord[0]), self._alphabet.normalize(cord[1])
        return self._mappings.get(a1) == a2 or self._mappings.get(a2) == a1

    @property
    def alphabet(self) -> Alphabet:  # noqa: D102
        return self._alphabet

    def __len__(self) -> int:
        """Return the number of cords in the plugboard."""
        return len(self._mappings) // 2

    @property
    def _max_pairs(self) -> int:
        return len(self._alphabet) // 2

    def _normalize_cord(self, cord: tuple[str, str]) -> tuple[str, str]:
        a1, a2 = self._alphabet.normalize(cord[0]), self._alphabet.normalize(cord[1])
        if a1 == a2:
            raise ValueError("Alphabetic letters in the cord must be different.")
        return a1, a2

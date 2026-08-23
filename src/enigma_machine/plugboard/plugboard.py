"""Module containins the Plugboard class."""

from ..alphabet.alphabet import Alphabet
from ..alphabet.errors import InternalStateError


class Plugboard:
    """Represents the plugboard in the enigma machine.

    The plugboard allows the user to dynamically pair alphabetic letters,
    facilitating further letter scrambling and more encoding configurations.
    The plugboard encode letters by mapping an input letter with its corded letter.
    If no cording exists, the plugboard simply maps the input letter to itself.

    Example:
                Figure 1
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        |__|    |_______|      |_|

        Figure 1 shows a simple plugboard configuration where A is connected to (<->) D, I <-> Q, and X <-> Z.
        The connection is bidirectional, meaning that input letter A is encoded as D, D as A, and so forth.
        The reader should realize that the plugboard can connect at most 13 cords as this occupies all
        available letter outlets. Each cord represent a unique pair of letters, meaning that letters in a pair
        cannot be found in a different pair.
    """

    def __init__(self,
        *cords: tuple[str, str],
        alphabet: Alphabet = Alphabet.LATIN_ALPHABET
    ) -> None:
        """Class initializer.

        Args:
            *cords: typle[str, str] - A cord is represented as a tuple of two strings. Example: ("A", "G") means
                                      A <-> G.
            alphabet: Alphabet - Alphabet to validate cords against.
        """
        self._mappings: dict[str, str] = {}
        self._alphabet: Alphabet = alphabet

        if cords:
            pairs = len(self._alphabet) // 2
            if len(cords) > pairs:
                raise ValueError(f"At most {pairs} cords can be used simultanously in the plugboard")
            for cord in cords:
                self.add_cord(cord)

    def encode(self, alph_letter: str) -> str:
        """Encode an alphabetic letter using the plugboard configuration.

        Args:
            alph_letter: str - Alphabetic letter to encode.

        Returns:
            str - Encoded letter.
        """
        # Simply return alph_letter if _mappings is empty.
        if not self._mappings:
            return alph_letter

        encoding = self._mappings.get(alph_letter)
        if encoding is not None:
            return encoding
        encoding = self._mappings.get(alph_letter)
        if encoding is not None:
            return encoding

        return alph_letter

    def add_cord(self, cord: tuple[str, str]) -> None:
        """Add a new cord to the plugboard.

        Args:
            cord: tuple[str, str] - Cord to be added.
        """
        pairs = len(self._alphabet) // 2
        if len(self) == pairs:
            raise InternalStateError(f"At most {pairs} cords can be used simultanously in the plugboard")

        a1, a2 = self._normalize_cord(cord)

        if a1 in self._mappings or a2 in self._mappings:
            raise ValueError(f"{a1} or {a2} already exists as a mapping")

        self._mappings[a1] = a2
        self._mappings[a2] = a1

    def remove_cord(self, cord: tuple[str, str]) -> None:
        """Remove a cord from the plugboard.

        Removing a cord means that the involved letters will map to themselves.

        Args:
            cord: tuple[str, str] - Cord to be removed.
        """
        a1, a2 = self._normalize_cord(cord)

        if self._mappings.get(a1) == a2 and self._mappings.get(a2) == a1:
            del self._mappings[a1]
            del self._mappings[a2]

    def cord_exists(self, cord: tuple[str, str]) -> bool:
        """Return true if the cord (c1, c2) or (c2, c1) exists.

        Args:
            cord: tuple[str, str] - Cord to test.

        Returns:
            bool - True if cord exists, else false.
        """
        a1, a2 = self._alphabet.normalize(cord[0]), self._alphabet.normalize(cord[1])
        return self._mappings.get(a1) == a2 or self._mappings.get(a2) == a1

    def __len__(self) -> int:
        """Return the number of cords in the plugboard."""
        return len(self._mappings) // 2

    def _normalize_cord(self, cord: tuple[str, str]) -> tuple[str, str]:
        a1, a2 = self._alphabet.normalize(cord[0]), self._alphabet.normalize(cord[1])
        if a1 == a2:
            raise ValueError("Alphabetic letters in the cord must be different.")
        return a1, a2

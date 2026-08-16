"""Module containins the Plugboard class."""

from bidict import bidict

from .._internals.keyboard import normalize_letter
from .._internals.errors import InternalStateError


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

    def __init__(self, *cords: tuple[str, str]) -> None:
        """Class initializer.

        Args:
            *cords: typle[str, str] - A cord is represented as a tuple of two strings. Example: ("A", "G") means
                                      A <-> G.
        """
        self._mappings: bidict[str, str] = bidict()
        if cords:
            if len(cords) > 13:
                raise ValueError("At most 13 cords can be used simultanously in the plugboard")
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
        encoding = self._mappings.inverse.get(alph_letter)
        if encoding is not None:
            return encoding

        return alph_letter

    def add_cord(self, cord: tuple[str, str]) -> None:
        """Add a new cord to the plugboard.

        Args:
            cord: tuple[str, str] - Cord to be added.
        """
        if len(self._mappings) == 13:
            raise InternalStateError("At most 13 cords can be used simultanously in the plugboard")

        a1, a2 = Plugboard._normalize_cord(cord)

        if a1 in self._mappings or a2 in self._mappings:
            raise ValueError(f"{a1} or {a2} already exists as a mapping")
        if a1 in self._mappings.inverse or a2 in self._mappings.inverse:
            raise ValueError(f"{a1} or {a2} already exists as a mapping")

        self._mappings[a1] = a2

    def remove_cord(self, cord: tuple[str, str]) -> None:
        """Remove a cord from the plugboard.

        Removing a cord means that the involved letters will map to themselves.

        Args:
            cord: tuple[str, str] - Cord to be removed.
        """
        a1, a2 = Plugboard._normalize_cord(cord)

        if self._mappings.get(a1) == a2:
            del self._mappings[a1]
        elif self._mappings.inverse.get(a1) == a2:
            del self._mappings.inverse[a1]

    def cord_exists(self, cord: tuple[str, str]) -> bool:
        """Return true if the cord (c1, c2) or (c2, c1) exists.

        Args:
            cord: tuple[str, str] - Cord to test.

        Returns:
            bool - True if cord exists, else false.
        """
        a1, a2 = normalize_letter(cord[0]), normalize_letter(cord[1])
        return self._mappings.get(a1) == a2 or self._mappings.inverse.get(a1) == a2

    def __len__(self) -> int:
        return len(self._mappings)

    @staticmethod
    def _normalize_cord(cord: tuple[str, str]) -> tuple[str, str]:
        a1, a2 = normalize_letter(cord[0]), normalize_letter(cord[1])
        if a1 == a2:
            raise ValueError("Alphabetic letters in the cord must be different.")
        return a1, a2

"""Module representing a rotor in the Enigma machine.

The rotor is a key component of the Enigma machine. It is reponsible for one of several substitutions of
letters during the encryption and decryption process. Each rotor has a fixed wiring
that maps input letters [A-Z] to output letters [A-Z] (read more about wiring in wiring.py). Once a
letter is entered, the rotor will make a substitution based on its wiring and current position. The position
of the rotor decides how input letters are shifted before the substitution is made. A shift is essentially a mapping
between input letters. For instance, if the rotor position is at 1, then input letter A, the first letter in the
alphabet, will effectively translate to its neighbouring letter B as we "shift" A by 1 step.

Example:
Assume that the letters in the alphabet ABCDEFGHIJKLMNOPQRSTUVWXY are wired to the permutation
BCDEFGHIJKLMNOPQRSTUVWXYA. This means that input letters A maps (->) to B, B -> C, C -> D and so on.
If rotor position is at 1, then input letter A is shifted by 1, effectively becoming B, which is encoded as C.
So A -> B -> C, meaning that A -> C at rotor position 1.

"""

from enum import Enum
from typing import ClassVar

from enigma_machine.utils.constants import ENGLISH_ALPHABET

from .utils import _normalize_letter
from .wiring import Wiring


class Rotor:
    """Class for representing a rotor in the Enigma machine.

    Attributes:
        wiring: Wiring   - Defines a mapping between input letters and encoded letters. Wiring is either referred to
                           the class object named 'Wiring' that encapsulates wiring logic, or an encoding/mapping of the
                           alphabet: [A-Z] -> [A-Z].
        position: int    - Starting position of the rotor. Any integer value is accepted, as the position is normalized
                           using modulo 26 to ensure that the internal representation is always in the range [0, 25].
                           This internal representation is an implementation detail; the public interface exposes rotor
                           positions in the range [1, 26], matching the conventional numbering of Enigma rotor
                           positions. The rotor positions can also be viewed in terms of alphabetic letters where
                           position 1 corresponds to the letter A, 2 to B, and so on.
    """
    ALPHABET: str = ENGLISH_ALPHABET
    ALPHABET_MAPPING: ClassVar = {
        k: v for v, k in enumerate(ENGLISH_ALPHABET)
    }

    def __init__(self, wiring: Wiring | str, position: int = 0) -> None:
        """Class initializer.

        When 'wiring' arg is a string, then that string should be an encoding of the alphabet.

        Example string: QXJEMWSYCGARHKOFLIBDTVZUNP.
        """
        if isinstance(wiring, str):
            self._wiring = Wiring(wiring)
        else:
            self._wiring = wiring

        self._position = position % len(self._wiring)

    def encode(self, alph_letter: str, reverse: bool = False, turn: bool = False) -> str:
        """Encode an alphabetic letter under the current position and wiring.

        Args:
            alph_letter: str - Alphabetic letter to be encoded.
            reverse: bool    - Reverses the encoding, i.e., return an encoded letter 'alph_letter' to its
                               original mapping.
            turn: bool       - Turns the rotor by one step if true, i.e. increases the position by 1.

        Returns:
            str - The encoded letter.
        """
        if turn:
            self.turn()

        letter_norm = _normalize_letter(alph_letter)

        alph_index = Rotor.ALPHABET_MAPPING.get(letter_norm)

        # Apply the shift and fetch the effective input letter
        shifted_alph_index = (alph_index + self._position) % len(Rotor.ALPHABET)
        shifted_alph = Rotor.ALPHABET[shifted_alph_index]

        return self._wiring.encode(shifted_alph, reverse)


    def turn(self, steps: int = 1) -> int:
        """Modify the position of the rotor.

        Args:
            steps: int - number of steps to turn

        Returns:
            int - current position of the rotor
        """
        self._position = (self._position + steps) % len(Rotor.ALPHABET)
        return self.position

    @property
    def position(self) -> int:
        """Return the rotor position.

        Externally, the position has 1-based indexing.
        """
        return self._position + 1

    @position.setter
    def position(self, value: int) -> None:
        """Set position attribute using an integer value between [1, 26]."""
        if not (1 <= value <= 26):
            raise ValueError("'value' must be in the range 1 <= value <= 26")
        self._position = value - 1


    @property
    def letter_position(self) -> str:
        """Return the position in terms of an alphabetic letter.

        For instance, position 1 correspond to the letter A as it is the first letter in the
        alphabet.
        """
        return Rotor.ALPHABET[self._position]

    @property
    def wiring(self) -> Wiring:
        """Return Wiring object."""
        return self._wiring


class RotorFactory(Enum):
    """Factory class that builds rotor instances based on predefined wirings.

    The predefined wirings are based on the ones used in the real enigma machine.
    See Enigma I section in https://www.cryptomuseum.com/crypto/enigma/wiring.htm#23 for details.
    """
    ROTOR_I   = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    ROTOR_II  = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    ROTOR_IV  = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    ROTOR_V   = "VZBRGITYUPSDNHLXAWMJQOFECK"

    def __init__(self, wiring: str) -> None:
        self.wiring = wiring

    def build(self) -> Rotor:
        """Build and return a rotor based on the wiring attribute."""
        return Rotor(self.wiring)

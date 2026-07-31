"""Module containing rotor related functionality."""

from enum import Enum

from bidict import bidict

from .._internals.alphabet import ENGLISH_ALPHABET, normalize_letter
from ._wiring import Wiring


class Rotor:
    """Class for representing a rotor in the Enigma machine.

    The rotor is a key component of the Enigma machine. It is reponsible for one of several substitutions of
    letters during the encryption and decryption process. Each rotor has a fixed wiring
    that maps input letters [A-Z] to output letters [A-Z] (read more about wiring in _wiring.py). Once a
    letter is entered, the rotor will make a substitution based on its wiring and current position. The position
    of the rotor decides how input letters are shifted before and after the substitution is made. A shift is essentially
    a mapping between input letters. For instance, if the rotor position is at 1, then input letter A, the first letter
    in the alphabet, will effectively translate to its neighbouring letter B as we "shift" A by 1 step.

    Example:
    Assume that the letters in the alphabet ABCDEFGHIJKLMNOPQRSTUVWXY are wired to the permutation
    BCDEFGHIJKLMNOPQRSTUVWXYA. This means that input letters A encodes (->) to B, B -> C, C -> D and so on.
    If rotor position is at 1, then input letter A is shifted by 1, effectively becoming B, which is encoded as C.
    So A -> B -> C, meaning that A -> C at rotor position 1.
    """

    ALPHABET_INDICES = bidict({ k: v for v, k in enumerate(ENGLISH_ALPHABET) })

    def __init__(self, wiring: str, position: int = 1) -> None:
        """Class initializer.

        Args:
            wiring: str   - A permutation of the alphabet. Example: QXJEMWSYCGARHKOFLIBDTVZUNP.
            position: int - Starting position of the rotor. Valid values are [1, 26].

        """
        self._wiring = Wiring(wiring)

        self._offset = 0 # initializes _offset attribute
        self.position = position # adjusts _offset accordingly

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

        letter_norm = normalize_letter(alph_letter)

        alph_index = Rotor.ALPHABET_INDICES[letter_norm]

        divisor = len(ENGLISH_ALPHABET)

        # Apply the shift and fetch the effective input letter
        shifted_alph = Rotor.ALPHABET_INDICES.inverse[(alph_index + self._offset) % divisor]

        wired_letter = self._wiring.encode(shifted_alph, reverse)

        output_index = Rotor.ALPHABET_INDICES[wired_letter]

        encoded_letter = Rotor.ALPHABET_INDICES.inverse[(output_index - self._offset) % 26]

        return encoded_letter


    def turn(self, steps: int = 1) -> int:
        """Modify the position of the rotor and return the new position.

        Args:
            steps: int - number of steps to turn

        Returns:
            int - current position of the rotor
        """
        self._offset = (self._offset + steps) % len(ENGLISH_ALPHABET)
        return self.position

    @property
    def offset(self) -> int:
        """Return the offset."""
        return self._offset

    @property
    def position(self) -> int:
        """Return the rotor position."""
        return self._offset + 1

    @position.setter
    def position(self, value: int) -> None:
        """Set position attribute using an integer value between [1, 26]."""
        if not (1 <= value <= 26):
            raise ValueError("'value' must be in the range 1 <= value <= 26")
        self._offset = value - 1


    @property
    def letter_position(self) -> str:
        """Return the position in terms of an alphabetic letter.

        For instance, position 1 correspond to the letter A as it is the first letter in the
        alphabet.
        """
        return ENGLISH_ALPHABET[self._offset]

    @property
    def wiring(self) -> str:
        """Return the letter wiring in the rotor."""
        return self._wiring.permutation

class Rotors:
    """Class representing a set of rotors in the enigma machine.

    Rotors are attached in a sequence as shown in https://www.cryptomuseum.com/crypto/enigma/i/img/300002/033/full.jpg.
    The right-most rotor is called 'fast rotor', the middle 'middle rotor', and the left-most 'slow rotor'. The fast
    rotor turns one step every time the user types a letter, while the middle and the slow rotors turns once the rotor
    to its right has made a full turn. This means for instance that the middle rotor turns one step when the fast
    rotor overflows and is back to 1.
    """
    def __init__(self,
            fast_rotor: Rotor,
            middle_rotor: Rotor,
            slow_rotor: Rotor,
    ) -> None:
        self._fast_rotor = fast_rotor
        self._middle_rotor = middle_rotor
        self._slow_rotor = slow_rotor

    def forward(self, alph_letter: str) -> str:
        """Encode 'alph_letter' by passing it through all rotors from right to left and turn the rotors accordingly."""
        old_fast_pos = self._fast_rotor.position
        encoded_letter = self._fast_rotor.encode(alph_letter, turn = True)
        new_fast_pos = self._fast_rotor.position


        # Test if fast rotor made a full turn.
        turn_condition = new_fast_pos - old_fast_pos < 0

        old_middle_pos = self._middle_rotor.position
        encoded_letter = self._middle_rotor.encode(encoded_letter, turn = turn_condition)
        new_middle_pos = self._middle_rotor.position

        # test if middle rotor made a full turn.
        turn_condition = new_middle_pos - old_middle_pos < 0

        encoded_letter = self._slow_rotor.encode(encoded_letter, turn = turn_condition)

        return encoded_letter

    def backward(self, alph_letter: str) -> str:
        """Encode 'alph_letter' by passing it through all rotors from left to right with no turning."""
        encoded_letter = self._slow_rotor.encode(alph_letter, reverse=True)
        encoded_letter = self._middle_rotor.encode(encoded_letter, reverse=True)
        return self._fast_rotor.encode(encoded_letter, reverse=True)

    @property
    def setting(self) -> tuple[int, int, int]:
        """Return the current rotor setting by returning the rotor positions.

        The rotor settings are of great importance for decoding since
        the initial rotor setting used in the encoding process must be used when decoding.

        Returns:
            tuple[int, int, int] - (SLOW_ROTOR_POSITION, MIDDLE_ROTOR_POSITION, FAST_ROTOR_POSITION)
        """
        return (
            self._slow_rotor.position,
            self._middle_rotor.position,
            self._fast_rotor.position,
        )

    @setting.setter
    def setting(self, value: tuple[int, int, int]) -> None:
        slow_pos, middle_pos, fast_pos = value
        self._slow_rotor.position = slow_pos
        self._middle_rotor.position = middle_pos
        self._fast_rotor.position = fast_pos


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

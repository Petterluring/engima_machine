"""Module containing rotor related functionality."""

from bidict import bidict

from .._internals.alphabet import ENGLISH_ALPHABET, normalize_letter
from ._wiring import Wiring


class Rotor:
    """Class for representing a rotor in the Enigma machine.

    The rotor is a component that encodes letters based on its wiring and position. The wiring is understood as a
    mapping between the alphabet and a permutation of the alphabet (see _wiring.py for more details), while the position
    decides how letters are shifted in the alphabet before and after letters are passed through the wiring.

    Example:
    Assume that the letters in the alphabet ABCDEFGHIJKLMNOPQRSTUVWXY are wired to the permutation
    QWZJTYRLPFNSVXCHAMOEGKUBID. This means that input letters A encodes (->) to Q, B -> W, C -> Z and so on.
    If rotor position is at 2, then input letter A is shifted by 1, effectively becoming B since B is 1 step to the
    right of A. B is encoded as W according to the wiring. Since the rotor shifted the alphabet by 1,
    we must shift back by one, meaning that W effectively becomes V.
    So A -> B -> W -> V, meaning that A -> V at rotor position 2.
    """

    ALPHABET_INDICES = bidict({ k: v for v, k in enumerate(ENGLISH_ALPHABET) })

    def __init__(self, wiring: str, position: int = 1, turnover: int | str = 1) -> None:
        """Class initializer.

        Args:
            wiring: str         - A permutation of the alphabet. Example: QXJEMWSYCGARHKOFLIBDTVZUNP.
            position: int       - Starting position of the rotor. Valid values are [1, 26].
            turnover: int | str - Defines when the rotor makes a full turn in terms of a position. For instance, if
                                  turnover is 2, then rotor makes a full turn when reaching position 2. Valid values are
                                  [1, 26] (int) or [A-Z] (str).

        """
        self._wiring = Wiring(wiring)

        self._offset = 0 # initializes _offset attribute
        self.position = position # adjusts _offset accordingly

        self._turnover = 0
        self.turnover = turnover

    def encode(self, alph_letter: str, reverse: bool = False, turn: bool = False) -> str:
        """Encode an alphabetic letter given the current position and wiring.

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

        encoded_letter = Rotor.ALPHABET_INDICES.inverse[(output_index - self._offset) % divisor]

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
    def position(self) -> int:
        """Return the rotor position."""
        return self._offset + 1

    @position.setter
    def position(self, value: int | str) -> None:
        """Set position attribute using an integer value between [1, 26] or a character value in [A-Z]."""
        if isinstance(value, str):
            if len(value) != 1:
                raise ValueError(f"{value} must be one character when string type.")
            value_upper = value.upper()
            if value_upper not in ENGLISH_ALPHABET:
                raise ValueError(f"{value_upper} is not contained in the alphabet: {ENGLISH_ALPHABET}")
            self._offset = ENGLISH_ALPHABET.index(value_upper)
        else:
            if not (1 <= value <= 26):
                raise ValueError("value must be in the range [1, 26]")
            self._offset = value - 1

    @property
    def position_alph(self) -> str:
        """Return the position in terms of an alphabetic letter.

        For instance, position 1 correspond to the letter A as it is the first letter in the
        alphabet.
        """
        return ENGLISH_ALPHABET[self._offset]

    @property
    def wiring(self) -> str:
        """Return the letter wiring in the rotor."""
        return self._wiring.permutation

    @property
    def turnover(self) -> int:
        """Return the turnover attribute."""
        return self._turnover

    @turnover.setter
    def turnover(self, value: int | str) -> None:
        """Set position attribute using an integer value between [1, 26] or a character string in [A-Z]."""
        if isinstance(value, str):
            if len(value) != 1:
                raise ValueError(f"{value} must be one character when string type.")
            value_upper = value.upper()
            if value_upper not in ENGLISH_ALPHABET:
                raise ValueError(f"{value_upper} is not contained in the alphabet: {ENGLISH_ALPHABET}")
            self._turnover = ENGLISH_ALPHABET.index(value_upper) + 1
        else:
            if not (1 <= value <= 26):
                raise ValueError("value must be in the range [1, 26]")
            self._turnover = value

    @property
    def turnover_alph(self) -> str:
        """Return the turnover attribute in terms of an alphabetic letter.

        For instance, turnover 1 correspond to the letter A as it is the first letter in the
        alphabet.
        """
        return ENGLISH_ALPHABET[self._turnover - 1]


class Rotors:
    """Class representing a set of rotors in the enigma machine.

    Rotors are attached in a sequence. The right-most rotor is called 'fast rotor', the middle 'middle rotor',
    and the left-most 'slow rotor'. The fast rotor turns one step every time the user types a letter, while the middle
    and the slow rotors turns once the rotor to its right has made a full turn. This means for instance that the middle
    rotor turns one step when the fast rotor overflows and goes back to 1, like a clock.
    """
    def __init__(self,
            fast_rotor: Rotor | str,
            middle_rotor: Rotor | str,
            slow_rotor: Rotor | str,
    ) -> None:
        """Class initializer.

        Args:
            fast_rotor: Rotor | str   - If string object, the value should be a rotor wiring, represented by a
                                        permutation of the alphabet such as QJXRMPLVOGSIBZTEWCKUYAFNDH.
            middle_rotor: Rotor | str - See fast_rotor comment.
            slow_rotor: Rotor | str   - See fast_rotor comment.
        """
        self._fast_rotor = fast_rotor if isinstance(fast_rotor, Rotor) else Rotor(fast_rotor)
        self._middle_rotor = middle_rotor if isinstance(middle_rotor, Rotor) else Rotor(middle_rotor)
        self._slow_rotor = slow_rotor if isinstance(slow_rotor, Rotor) else Rotor(slow_rotor)

    def forward(self, alph_letter: str) -> str:
        """Encode alph_letter by passing it through all rotors from right to left and turn the rotors accordingly.

        Args:
            alph_letter: str - Alphabetic letter to encode.

        Returns:
            str - Encoded letter.
        """
        old_fast_pos = self._fast_rotor.position
        encoded_letter = self._fast_rotor.encode(alph_letter, turn = True)
        new_fast_pos = self._fast_rotor.position
        turnover = self._fast_rotor.turnover

        old_middle_pos = self._middle_rotor.position
        encoded_letter = self._middle_rotor.encode(
            encoded_letter,
            turn = Rotors._turn_condition(old_fast_pos, new_fast_pos, turnover)
        )
        new_middle_pos = self._middle_rotor.position
        turnover = self._middle_rotor.turnover

        encoded_letter = self._slow_rotor.encode(
            encoded_letter,
            turn = Rotors._turn_condition(old_middle_pos, new_middle_pos, turnover)
        )

        return encoded_letter

    def backward(self, alph_letter: str) -> str:
        """Encode 'alph_letter' by passing it through all rotors from left to right with no turning.

        Args:
            alph_letter: str - Alphabetic letter to encode.

        Returns:
            str - Encoded letter.
        """
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
    def setting(self, value: tuple[int, int, int] | tuple[str, str, str]) -> None:
        slow_pos, middle_pos, fast_pos = value
        self._slow_rotor.position = slow_pos
        self._middle_rotor.position = middle_pos
        self._fast_rotor.position = fast_pos

    @property
    def setting_alph(self) -> tuple[str, str, str]:
        """Return the current rotor setting by returning the rotor positions as alphabetic letters.

        The rotor settings are of great importance for decoding since
        the initial rotor setting used in the encoding process must be used when decoding.

        Returns:
            tuple[str, str, str] - (SLOW_ROTOR_POSITION_ALPH, MIDDLE_ROTOR_POSITION_ALPH, FAST_ROTOR_POSITION_ALPH)
        """
        return (
            self._slow_rotor.position_alph,
            self._middle_rotor.position_alph,
            self._fast_rotor.position_alph
        )


    @property
    def turnover_setting(self) -> tuple[int, int, int]:
        """Return the current turnover setting on the rotors.

        Returns:
            tuple[int, int, int] - (SLOW_ROTOR_TURNOVER, MIDDLE_ROTOR_TURNOVER, FAST_ROTOR_TURNOVER)
        """
        return (
            self._slow_rotor.turnover,
            self._middle_rotor.turnover,
            self._fast_rotor.turnover,
        )

    @turnover_setting.setter
    def turnover_setting(self, value: tuple[int, int, int] | tuple[str, str, str]) -> None:
        slow_turn, middle_turn, fast_turn = value
        self._slow_rotor.turnover = slow_turn
        self._middle_rotor.turnover = middle_turn
        self._fast_rotor.turnover = fast_turn

    @property
    def turnover_setting_alph(self) -> tuple[str, str, str]:
        """Return the current turnover setting on the rotors in terms of alphabetic letters.

        Returns:
            tuple[str, str, str] - (SLOW_ROTOR_TURNOVER_ALPH, MIDDLE_ROTOR_TURNOVER_ALPH, FAST_ROTOR_TURNOVER_ALPH)
        """
        return (
            self._slow_rotor.turnover_alph,
            self._middle_rotor.turnover_alph,
            self._fast_rotor.turnover_alph,
        )

    @property
    def slow_rotor(self) -> Rotor:
        """Return the slow rotor in the machine."""
        return self._slow_rotor

    @property
    def middle_rotor(self) -> Rotor:
        """Return the slow rotor in the machine."""
        return self._middle_rotor

    @property
    def fast_rotor(self) -> Rotor:
        """Return the slow rotor in the machine."""
        return self._fast_rotor

    @staticmethod
    def _turn_condition(old_position: int, new_position: int, turnover: int) -> bool:
        t1 = (old_position - turnover) % 26
        t2 = (new_position - turnover) % 26
        return t2 - t1 < 0

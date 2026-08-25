"""Module containing rotor related functionality."""

from ..alphabet.alphabet import Alphabet


class Rotor:
    """Class for representing a rotor in the Enigma machine.

    The rotor is a component that encodes letters based on its wiring and position. The wiring is understood as a
    mapping between some alphabet and a permutation of that alphabet, while the position
    decides how letters are shifted in the alphabet before and after letters are passed through the wiring.

    Example:
    Assume that the letters in the alphabet ABCDEFGHIJKLMNOPQRSTUVWXY are wired to the permutation
    QWZJTYRLPFNSVXCHAMOEGKUBID. This means that input letters A encodes (->) to Q, B -> W, C -> Z and so on.
    If rotor position is at 2, then input letter A is shifted by 1, effectively becoming B since B is 1 step to the
    right of A. B is encoded as W according to the wiring. Since the rotor shifted the alphabet by 1,
    we must shift back by one, meaning that W effectively becomes V.
    So A -> B -> W -> V, meaning that A -> V at rotor position 2.
    """

    def __init__(self, wiring: str, position: int = 1, turnover: int | str = 1) -> None:
        """Class initializer.

        Args:
            wiring: str         - A permutation of some supported alphabet. Example: QXJEMWSYCGARHKOFLIBDTVZUNP.
                                  See alphabet.py for supported alphabets.
            position: int       - Starting position of the rotor. Valid values are [1, len(wiring)] (int) and
                                  (A-<LAST_LETTER>) in the alphabet that the permutation in 'wiring' originates from.
            turnover: int | str - Defines when the rotor makes a full turn in terms of a position. For instance, if
                                  turnover is 2, then rotor makes a full turn when reaching position 2. See previous
                                  arg for valid values.


        """
        alphabet, norm_wiring = Alphabet.infer_alphabet_and_normalize(wiring)

        self._alphabet: Alphabet = alphabet
        self._wiring: str = norm_wiring

        self._offset = 0 # initializes _offset attribute
        self.position = position # adjusts _offset accordingly

        self._turnover = 0
        self.turnover = turnover

    def encode(self,
        alph_letter: str,
        reverse: bool = False,
        turn: bool = False,
        normalize: bool = True
    ) -> str:
        """Encode an alphabetic letter given the current position and wiring.

        Args:
            alph_letter: str - Alphabetic letter to be encoded.
            reverse: bool    - Reverses the encoding, i.e., return an encoded letter 'alph_letter' to its
                               original mapping.
            turn: bool       - Turns the rotor by one step if true, i.e. increases the position by 1.
            normalize: bool  - Flag for normalizing input letter.

        Returns:
            str - The encoded letter.
        """
        if turn:
            self.turn()

        alph_letter = self._alphabet.normalize(alph_letter) if normalize else alph_letter

        divisor = len(self._alphabet)

        alph_index = self._alphabet.index(alph_letter)
        shift_forward = (alph_index + self._offset) % divisor

        wired_letter = self._encode(shift_forward) if not reverse else self._encode_reverse(
            self._alphabet[shift_forward]
        )

        output_index = self._alphabet.index(wired_letter)
        shift_back = (output_index - self._offset) % divisor
        return self._alphabet[shift_back]

    def _encode(self, alph_letter: str | int) -> str:
        """Return the encoded letter of alph_letter."""
        if isinstance(alph_letter, int):
            return self._wiring[alph_letter]

        i = self._alphabet.index(alph_letter)
        return self._wiring[i]


    def _encode_reverse(self, wired_letter: str | int) -> str:
        """Return the reversed wiring of wired_letter."""
        if isinstance(wired_letter, int):
            return self._alphabet[wired_letter]

        i = self._wiring.index(wired_letter)
        return self._alphabet[i]


    def turn(self, steps: int = 1) -> int:
        """Modify the position of the rotor and return the new position.

        Args:
            steps: int - number of steps to turn

        Returns:
            int - current position of the rotor
        """
        self._offset = (self._offset + steps) % len(self._alphabet)
        return self.position

    @property
    def position(self) -> int:
        """Return the rotor position."""
        return self._offset + 1

    @position.setter
    def position(self, value: int | str) -> None:
        """Set position attribute using an integer or string.

        Valid values are [1, len(alphabet)] (int) or (A, LAST) where LAST
        is the last letter in the alphabet.
        """
        if isinstance(value, str):
            value_upper = self._alphabet.normalize(value)
            self._offset = self._alphabet.index(value_upper)
        else:
            length = len(self._alphabet)
            if not (1 <= value <= length):
                raise ValueError(f"value must be in the range [1, {length}]")
            self._offset = value - 1

    @property
    def position_alph(self) -> str:
        """Return the position in terms of an alphabetic letter.

        For instance, position 1 correspond to the letter A as it is the first letter in the
        alphabet.
        """
        return self._alphabet[self._offset]

    @property
    def alphabet(self) -> Alphabet:
        """Return the alphabet of the rotor."""
        return self._alphabet

    @property
    def wiring(self) -> str:
        """Return the wiring in the rotor."""
        return self._wiring

    @property
    def turnover(self) -> int:
        """Return the turnover attribute."""
        return self._turnover

    @turnover.setter
    def turnover(self, value: int | str) -> None:
        """Set turnover attribute using an integer or string.

        Valid values are:
            - [1, 26] and [A-Z] if using latin alphabet.
            - [1, 30] and [A-ß] if using german alphabet.
        """
        if isinstance(value, str):
            value_upper = self._alphabet.normalize(value)
            self._turnover = self._alphabet.index(value_upper) + 1
        else:
            leN = len(self._alphabet)
            if not (1 <= value <= leN):
                raise ValueError(f"value must be in the range [1, {leN}]")
            self._turnover = value

    @property
    def turnover_alph(self) -> str:
        """Return the turnover attribute in terms of an alphabetic letter.

        For instance, turnover 1 correspond to the letter A as it is the first letter in the
        alphabet.
        """
        return self._alphabet[self._turnover - 1]


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
                                        permutation of a supported alphabet such as QJXRMPLVOGSIBZTEWCKUYAFNDH.
            middle_rotor: Rotor | str - See fast_rotor comment.
            slow_rotor: Rotor | str   - See fast_rotor comment.
        """
        self._fast_rotor = fast_rotor if isinstance(fast_rotor, Rotor) else Rotor(fast_rotor)
        self._middle_rotor = middle_rotor if isinstance(middle_rotor, Rotor) else Rotor(middle_rotor)
        self._slow_rotor = slow_rotor if isinstance(slow_rotor, Rotor) else Rotor(slow_rotor)

        if not (self._slow_rotor.alphabet == self._middle_rotor.alphabet == self._fast_rotor.alphabet):
            raise ValueError("All rotors must use wirings that originate from the same alphabet. Current alphabets: " +
                             ", ".join(rotor.alphabet.value for rotor in [
                                 self._slow_rotor, self._middle_rotor, self._fast_rotor
                                ]))

    def forward(self, alph_letter: str, normalize: bool = True) -> str:
        """Encode alph_letter by passing it through all rotors from right to left and turn the rotors accordingly.

        Args:
            alph_letter: str - Alphabetic letter to encode.
            normalize: bool  - Flag for normalizing input letter.

        Returns:
            str - Encoded letter.
        """
        old_fast_pos = self._fast_rotor.position
        encoded_letter = self._fast_rotor.encode(alph_letter, turn=True, normalize=normalize)
        new_fast_pos = self._fast_rotor.position
        turnover = self._fast_rotor.turnover

        old_middle_pos = self._middle_rotor.position
        encoded_letter = self._middle_rotor.encode(
            encoded_letter,
            turn = self._turn_condition(old_fast_pos, new_fast_pos, turnover),
            normalize=False
        )
        new_middle_pos = self._middle_rotor.position
        turnover = self._middle_rotor.turnover

        encoded_letter = self._slow_rotor.encode(
            encoded_letter,
            turn = self._turn_condition(old_middle_pos, new_middle_pos, turnover),
            normalize=False
        )

        return encoded_letter

    def backward(self, alph_letter: str, normalize: bool = True) -> str:
        """Encode 'alph_letter' by passing it through all rotors from left to right with no turning.

        Args:
            alph_letter: str - Alphabetic letter to encode.
            normalize: bool  - Flag for normalizing input letter.

        Returns:
            str - Encoded letter.
        """
        encoded_letter = self._slow_rotor.encode(alph_letter, reverse=True, normalize=normalize)
        encoded_letter = self._middle_rotor.encode(encoded_letter, reverse=True, normalize=False)
        return self._fast_rotor.encode(encoded_letter, reverse=True, normalize=False)

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

    @property
    def rotor_alphabet(self) -> Alphabet:
        """Return the rotor alphabet."""
        return self.fast_rotor.alphabet # Any rotor is ok to use here as they use the same alphabet

    def _turn_condition(self, old_position: int, new_position: int, turnover: int) -> bool:
        divisor = len(self.rotor_alphabet)
        t1 = (old_position - turnover) % divisor
        t2 = (new_position - turnover) % divisor
        return t2 - t1 < 0

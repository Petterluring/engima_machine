"""Module for enigma machine related functionality."""
from .alphabet.alphabet import upper
from .plugboard import Plugboard
from .reflector import Reflector
from .rotor import Rotor, Rotors


class EnigmaMachine:
    """Class representing the enigma machine.

    The machine composes a rotor set (usually three rotors), a reflector, and a plugboard that together encrypts
    a given letter. The encryption starts at the plugboard which encodes the input letter according to plugboard
    configurations. The resulting letter is then passed through the rotors in the rotor set from right to left,
    through the reflector, and back through the rotors in the reversed order. The plugboard then makes a final
    substitution on the resulting letter before the encoded letter is returned (lit on the lampboard).
    """

    def __init__(self,
            rotors: Rotors | tuple[str, str, str],
            reflector: Reflector | str,
            plugboard: Plugboard | list[tuple[str, str]] | None = None
    ) -> None:
        """Class initializer.

        Args:
            rotors: Rotors | tuple[str, str, str] - Rotors used in the machine. If type is
                                                    tuple[str, str, str], then tuple should contain rotor wiring
                                                    for slow, middle, and fast rotor in that order:
                                                    (SLOW_ROTOR_WIRING, MIDDLE_ROTOR_WIRING, FAST_ROTOR_WIRING).

            reflector: str - A permutation of the alphabet [A-Z] defining the reflector wiring.
                                    Example: QWZJTYRLPFNSVXCHAMOEGKUBID. Since the reflector pairs alphabetic letters
                                    uniquely, the first half of the permutation is wired with the second half,
                                    meaning that QWZJTYRLPFNSVXCHAMOEGKUBID is encoded as:
                                                    QWZJTYRLPFNSV
                                                    XCHAMOEGKUBID

            plugboard: Plugboard | list[tuple[str, str]] | None - Plugboard to be used. None object triggers
                                                                  initialization of an empty Plugboard.
                                                                  User can also use list[tuple[str, str]]
                                                                  type to list all cords to include in the
                                                                  Plugboard
        """
        self._rotors = rotors if isinstance(rotors, Rotors) else Rotors(
            slow_rotor=Rotor(rotors[0]),
            middle_rotor=Rotor(rotors[1]),
            fast_rotor=Rotor(rotors[2]),
        )

        self._reflector = reflector if isinstance(reflector, Reflector) else Reflector(reflector)

        if plugboard is None:
            self._plugboard = Plugboard()
        elif isinstance(plugboard, list):
            self._plugboard = Plugboard(*plugboard)
        else:
            self._plugboard = plugboard

        if not (self._rotors.rotor_alphabet == self._reflector.alphabet == self._plugboard.alphabet):
            raise ValueError("Rotors, reflector, and plugboard must use the same alphabet.")

    def encode(self, alph_letter: str) -> str:
        """Encode an alphabetic letter by passing it through the plugboard, rotors, reflector, etc.

        For a given input letter, the enigma machine does the following encodings:
            1. Encode alph_letter to the connected letter according to given plugboard configuration.
            2. Forward the corded letter in the rotor set.
            3. Enter the forwared letter to the reflector.
            4. Enter the reflected letter to the rotor set in the reversed rotor order.
            5. Make a final substitution in the plugboard and return the final encoded letter.

        Args:
            alph_letter: str - Alphabetic letter ([A-Z]) to encode.

        Returns:
            str - Encoded letter.
        """
        encoded_letter = self._plugboard.encode(alph_letter)    # PLUGBOARD
        encoded_letter = self._rotors.forward(encoded_letter)   # ROTOR FORWARD
        encoded_letter = self._reflector.encode(encoded_letter) # REFLECT
        encoded_letter = self._rotors.backward(encoded_letter)  # ROTOR BACKWARD
        return self._plugboard.encode(encoded_letter)           # PLUGBOARD

    def encode_message(self, message: str) -> str:
        """Return the encoding of a full message.

        Characters not contained in the alphabet [A-Z] are ignored.

        Args:
            message: str - Message to encode.

        Returns:
            str - Encoded message.
        """
        encoded_msg = ""

        for letter in message:
            letter_upper = upper(letter)
            if letter_upper not in self._plugboard.alphabet.value: # Rotors or reflector are alph ok to use as well.
                continue
            encoded_msg += self.encode(letter_upper)

        return encoded_msg

    @property
    def rotor_setting(self) -> tuple[int, int, int]:
        """Return the current rotor setting."""
        return self._rotors.setting

    @rotor_setting.setter
    def rotor_setting(self, value: tuple[int, int, int]) -> None:
        self._rotors.setting = value

    @property
    def rotor_turnover_setting(self) -> tuple[int, int, int]:
        """Return the current rotor turnover setting."""
        return self._rotors.turnover_setting

    @rotor_turnover_setting.setter
    def rotor_turnover_setting(self, value: tuple[int, int, int]) -> None:
        self._rotors.turnover_setting = value

    @property
    def rotors(self) -> Rotors:
        """Return the Rotors instance."""
        return self._rotors

    @property
    def reflector_wiring(self) -> str:
        """Return the reflector wiring."""
        return self._reflector.permutation

"""Module for enigma machine related functionality."""
from ._internals.alphabet import ENGLISH_ALPHABET
from ._reflector import Reflector
from .plugboard import Plugboard
from .rotor import Rotors


class EnigmaDevice:
    """Class representing the enigma machine.

    The machine composes a rotor set (usually three rotors), a reflector, and a plugboard that together encrypts
    a given letter.
    """

    def __init__(self,
            rotors: Rotors,
            reflector_wiring: str,
            plugboard: Plugboard | None = None
    ) -> None:
        self._rotors = rotors
        self._reflector = Reflector(reflector_wiring)
        self._plugboard = plugboard if plugboard is not None else Plugboard()

    def encode(self, alph_letter: str) -> str:
        """Encode an alphabetic letter by passing it through the plugboard, rotors, reflector, etc.

        For a given input letter, the enigma machine does the following encodings:
            1. Encode alph_letter to the connected letter according to given plugboard configuration.
            2. Forward the letter in the rotor set.
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
            letter_upper = letter.upper()
            if letter_upper not in ENGLISH_ALPHABET:
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

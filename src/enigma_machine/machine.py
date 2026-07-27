"""Module for enigma machine related functionality."""
from ._internals.alphabet import ENGLISH_ALPHABET
from .rotor import Rotor
from .rotor._wiring import Wiring


class Machine:
    """Class representing the enigma machine.

    The machine composes three rotors, a reflector, and a plugboard that together encrypts a given letter.

    Attributes:
        fast_rotor: Rotor       - Right most rotor in the machine. Turns at every encoding.
        middle_rotor: Rotor     - Middle rotor in the machine. Turns once fast_rotor makes a full turn.
        slow_rotor: Rotor       - Left most rotor in the machine. Turns once middle_rotor makes a full turn.
        reflector: Wiring | str - The reflector is a simple wiring as described in the Wiring class. After an input
                                  letter passes through the rotors, the reflector makes a simple substitution before
                                  it is passed through the rotors again from the left.
        TODO: add docstring for plugboard once implemented.
    """

    def __init__(self,
            fast_rotor: Rotor,
            middle_rotor: Rotor,
            slow_rotor: Rotor,
            reflector_wiring: str,
    ) -> None:
        self._fast_rotor = fast_rotor
        self._middle_rotor = middle_rotor
        self._slow_rotor = slow_rotor
        self._reflector = Wiring(reflector_wiring)
        self._turn_counter = 0

    def encode(self, alph_letter: str) -> str:
        """Encode an alphabetic letter by passing it through the plugboard, rotors, reflector, etc.

        For a given input letter, the enigma machine does the following encodings:
            1. Encode input letter (alph_letter) to the connected letter according to given plugboard configuration.
            2. Use that encoded letter as input in the fast rotor (first rotor from the right on the physical machine)
               and encode it accordingly to given rotor configuration. Rotor is turned before encoding occurs.
            3. Same as 2 but for the middle rotor. Rotor is turned once the fast rotor makes a full turn.
            4. Same as 3 but for the slow rotor. Rotor is turned once the middle rotor makes a full turn.
            5. The encoded letter then enters the reflector, which makes a simple letter substitution accordingly to
               the wiring configuration.
            6. The reflected letter is then encoded in the slow rotor using the inverse mapping of the wiring and
               current rotor configuration. Rotor is not turned.
            7. Same as 6 but between the slow and the middle rotor.
            8. Same as 7 but between the middle and the fast rotor.
            9. Finally, the encoded letter is subsituted once more in the plugboard before returned.

        Args:
            alph_letter: str - Alphabetic letter ([A-Z]) to encode.

        Returns:
            str - Encoded letter.
        """
        # TODO: pass alph_letter through plugboard

        self._turn_counter += 1
        # FORWARD PASS
        encoded_letter = self._fast_rotor.encode(alph_letter, turn=True)
        encoded_letter = self._middle_rotor.encode(
            encoded_letter, turn=self._turn_counter % 26 == 0
        )
        encoded_letter = self._slow_rotor.encode(
            encoded_letter, turn=self._turn_counter % 676 == 0 # 26*26 = 676
        )

        # REFLECTION
        encoded_letter = self._reflector.encode(encoded_letter)

        # BACKWARD PASS
        encoded_letter = self._slow_rotor.encode(encoded_letter, reverse=True)
        encoded_letter = self._middle_rotor.encode(encoded_letter, reverse=True)
        encoded_letter = self._fast_rotor.encode(encoded_letter, reverse=True)

        # TODO: pass encoded_letter through plug board

        return encoded_letter

    def encode_message(self, message: str) -> str:
        """Return the encoding of a full message.

        Characters not contained in the alphabet [A-Z] are ignored

        Args:
            message: str - Message to encode.

        Returns:
            str - Encoded message.
        """
        encoded_msg = ""

        for letter in message:
            letter_upper = letter.upper()
            if letter not in ENGLISH_ALPHABET:
                continue
            encoded_msg += self.encode(letter_upper)

        return encoded_msg

    def set_rotor_config(self,
        slow_rotor_pos: int = 1,
        middle_rotor_pos: int = 1,
        fast_rotor_pos: int = 1
    ) -> None:
        """Configure the rotors by assigning values 1-26 to respective position.

        To decode a message, the user should the same starting rotor positions that was used
        for encoding.

        Args:
            slow_rotor_pos: int   - position value for the slow rotor.
            middle_rotor_pos: int - position value for the middle rotor.
            fast_rotor_pos: int   - position value for the fast rotor.
        """
        self._slow_rotor.position = slow_rotor_pos
        self._middle_rotor.position = middle_rotor_pos
        self._fast_rotor.position = fast_rotor_pos

        # _turn_counter must be changed to ensure correct rotoring
        self._turn_counter = slow_rotor_pos * middle_rotor_pos * fast_rotor_pos - 1

    @property
    def rotor_config(self) -> tuple[int, int, int]:
        """Return the current rotor config as integers."""
        return (
            self._slow_rotor.position,
            self._middle_rotor.position,
            self._fast_rotor.position,
        )

    @property
    def rotor_config_letters(self) -> tuple[str, str, str]:
        """Return the current rotor config as alphabetic letters.

        For instance, rotor position 1 correspond to letter A.
        """
        return (
            ENGLISH_ALPHABET[self._slow_rotor.position - 1],
            ENGLISH_ALPHABET[self._middle_rotor.position - 1],
            ENGLISH_ALPHABET[self._fast_rotor.position - 1],
        )

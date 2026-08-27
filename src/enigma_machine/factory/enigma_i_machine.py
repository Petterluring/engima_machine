"""Module for storing factory related functionality for Enigma I device."""
from ..alphabet import Alphabet
from ..machine import EnigmaMachine
from ..plugboard import Plugboard
from ..rotor import Rotor, Rotors

_REFLECTORS = {
         # WIRING
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}

_ROTORS = {
       # WIRING                      # Turnover
    1: ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    2: ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    3: ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    4: ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    5: ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}

def _validate_rotor_identifiers(tup: tuple[int, int, int]) -> None:
    if len(tup) != len(set(tup)):
        raise ValueError("Rotor numbers must be unique.")
    for i in tup:
        if not (1 <= i <= len(_ROTORS)):
            raise ValueError(f"Rotor numbers must be in the range [1, {len(_ROTORS)}")

def _validate_reflector_identifier(reflector: str) -> None:
    if len(reflector) != 1:
        raise ValueError("Reflector identifier must be one character.")
    if reflector not in _REFLECTORS:
        raise ValueError("Reflector identifier does not exist.")


def create_enigma_i_machine(
        slow_rotor_id: int = 1,
        middle_rotor_id: int = 2,
        fast_rotor_id: int = 3,
        reflector_id: str = "A"
) -> EnigmaMachine:
    """Return an EnigmaMachine instance based on the wiring in the Enigma I device.

    Use the rotor identifiers and the reflector identifier to build a certain Enigma I configuration. Rotor
    identifiers must be unique.

    Args:
        slow_rotor_id:   Valid values: [1, 5].
        middle_rotor_id: Valid values: [1, 5].
        fast_rotor_id:   Valid values: [1, 5].
        reflector_id:    Valid values: A, B, C

    Available Enigma rotors and reflectors
    (See Enigma I in https://www.cryptomuseum.com/crypto/enigma/wiring.htm#23 for more details):

    Rotors
    ------
    Rotor I (1)
        Wiring: EKMFLGDQVZNTOWYHXUSPAIBRCJ
        Turnover: Q

    Rotor II (2)
        Wiring: AJDKSIRUXBLHWTMCQGZNPYFVOE
        Turnover: E

    Rotor III (3)
        Wiring: BDFHJLCPRTXVZNYEIWGAKMUSQO
        Turnover: V

    Rotor IV (4)
        Wiring: ESOVPZJAYQUIRHXLNFTGKDCMWB
        Turnover: J

    Rotor V (5)
        Wiring: VZBRGITYUPSDNHLXAWMJQOFECK
        Turnover: Z

    Reflectors
    ----------
    UKW-A (A)
        Wiring: EJMZALYXVBWFCRQUONTSPIKHGD

    UKW-B (B)
        Wiring: YRUHQSLDPXNGOKMIEBFZCWVJAT

    UKW-C (C)
        Wiring: FVPJIAOYEDRZXWGCTKUQSBNMHL
    """
    _validate_rotor_identifiers((slow_rotor_id, middle_rotor_id, fast_rotor_id))
    _validate_reflector_identifier(reflector_id)

    slow_wiring, slow_turnover     = _ROTORS[slow_rotor_id]
    middle_wiring, middle_turnover = _ROTORS[middle_rotor_id]
    fast_wiring, fast_turnover     = _ROTORS[fast_rotor_id]
    reflector_wiring               = _REFLECTORS[reflector_id]

    return EnigmaMachine(
        Rotors(
            slow_rotor=Rotor(wiring=slow_wiring, turnover=slow_turnover),
            middle_rotor=Rotor(wiring=middle_wiring, turnover=middle_turnover),
            fast_rotor=Rotor(wiring=fast_wiring, turnover=fast_turnover),
        ),
        reflector=reflector_wiring,
        plugboard=Plugboard(alphabet=Alphabet.LATIN_ALPHABET)
    )

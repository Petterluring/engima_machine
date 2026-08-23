"""Module for testing rotor.py."""


import pytest

from enigma_machine.rotor import Rotor


def wiring_german() -> str:
    """Define a fixed wiring by defining a permutation of the german alphabet."""
          # ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ
    return "RBCDEFGHIJKLÖNOPQASTUVWXYZÄMÜẞ"

def wiring_latin() -> str:
    """Define a fixed wiring by defining a permutation of the latin alphabet."""
          # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    return "QJXRMPLVOGSIBZTEWCKUYAFNDH"

@pytest.fixture
def rotor() -> Rotor:
    """Return a predefined rotor to use throughout tests."""
    return Rotor(wiring_latin(), 1)

def test_rotor_init_default_values() -> None:
    """Test that default values are correct in initializer."""
    rotor = Rotor(wiring_latin())
    assert rotor.position == 1
    assert rotor.turnover == 1

@pytest.mark.parametrize(
        ("alphabet", "wiring", "position", "turnover"), [
            ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "BACDEFGHIJKLMNOPQRSTUVWXYZ", 24, 5),
            ("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ", "AYHQẞRCFZDWUETMGSÄIVÜJÖPKXLBON", 29, 28),
            ("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ", "LEQPSÜÖẞJCXNFVZWUDHÄYKRAOMGTBI", 27, 8)
        ]
)
def test_rotor_init_assigns_attributes_correctly(
    alphabet: str,
    wiring: str,
    position: int,
    turnover: int,
) -> None:
    """Assert that rotor initializer assigns class attribtues correctly."""
    rotoR = Rotor(wiring, position, turnover)
    assert rotoR.alphabet == alphabet
    assert rotoR.wiring == wiring
    assert rotoR.position == position
    assert rotoR.turnover == turnover

@pytest.mark.parametrize(
        ("wiring", "match_str", "lower_bound", "upper_bound"), [
            ("BACDEFGHIJKLMNOPQRSTUVWXYZ", r"range \[1, 26\]", 1, 26),
            ("AYHQẞRCFZDWUETMGSÄIVÜJÖPKXLBON", r"range \[1, 30\]", 1, 30)
        ]
)
def test_rotor_init_raises_error_invalid_position(
    wiring: str,
    match_str: str,
    lower_bound: int,
    upper_bound: int,
) -> None:
    """Test that Rotor initializer raises ValueError correctly."""
    with pytest.raises(ValueError, match=match_str):
        Rotor(wiring, lower_bound - 1)
    with pytest.raises(ValueError, match=match_str):
        Rotor(wiring, upper_bound + 1)

@pytest.mark.parametrize(
    "wiring", [
        wiring_latin(),
        wiring_german()
    ]
)
def test_rotor_turning(wiring: str) -> None:
    """Test rotation mechanism by asserting that 'turn' method increases position value correctly."""
    rotor = Rotor(wiring)
    leN = len(rotor.alphabet)
    for position in range(1, leN + 1):
        assert position == rotor.position
        rotor.turn()

    assert rotor.position == 1 # rotor makes a full turn and goes back to 1.

    assert rotor.turn(steps = 5) == 6

    assert rotor.turn(steps = leN) == 6

    assert rotor.turn(steps = -2) == 4

def test_rotor_encode_raises_incorrect_length_error(rotor: Rotor) -> None:
    """Test that encode function raises value error for input letters with more or less characters than 1."""
    with pytest.raises(ValueError, match="one character"):
        rotor.encode("AHB")
    with pytest.raises(ValueError, match="one character"):
        rotor.encode("")

@pytest.mark.parametrize(
        ("wiring", "illegal_chars"), [
            (wiring_latin(), "?=()ÄÖÜẞ"),
        ]
)
def test_encode_raises_character_not_contained_error(wiring: str, illegal_chars: str) -> None:
    """Test that map function raises value error for characters that are not contained in alphabet."""
    rotor = Rotor(wiring)
    for char in illegal_chars:
        with pytest.raises(ValueError, match="not contained"):
            rotor.encode(char)

@pytest.mark.parametrize(
        "wiring", [
            wiring_latin(),
            wiring_german()
        ]
)
def test_rotor_encoding_without_turning(wiring: str) -> None:
    """Test if rotor returns the correct encodings without any turning."""
    rotor = Rotor(wiring)
    for alph_letter, encoded_letter in zip(rotor.alphabet, wiring, strict=True):
        assert rotor.encode(alph_letter) == encoded_letter

    for alph_letter, encoded_letter in zip(rotor.alphabet, wiring, strict=True):
        assert rotor.encode(encoded_letter, reverse=True) == alph_letter

def test_rotor_encoding_with_turning(rotor: Rotor) -> None:
    """Test that a rotation steps shifts the input letters correctly."""
    input_letter = "A"
    rotor.position = 1

    assert rotor.encode(input_letter, turn=True) == "I" # MARKER
    assert rotor.encode(input_letter, turn=True) == "V"
    assert rotor.encode(input_letter, turn=True) == "O"
    """
    Encoding process of input_letter at row MARKER (rotor position = 2):

        MACHINE CONTACTS
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    ^
    |
    Input: A

        ROTOR INPUT CONTACTS
    BCDEFGHIJKLMNOPQRSTUVWXYZA
    ^
    |
    A on the machine aligns with rotor contact B.

        ROTOR WIRING
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    QJXRMPLVOGSIBZTEWCKUYAFNDH
     ^
     |
    Rotor contact B is wired to rotor contact J.

        ROTOR OUTPUT CONTACTS
    BCDEFGHIJKLMNOPQRSTUVWXYZA
            ^
            |
    Rotor output contact J is aligned with machine contact I.

        MACHINE CONTACTS
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
            ^
            |
    Output: I
    """


@pytest.mark.parametrize(
        ("wiring", "lower_bound", "upper_bound", "mult_chars", "invalid_char"), [
            (wiring_latin(), 1, 26, "AB", "ẞ"),
            (wiring_german(), 1, 30, "AB", "?")
        ]
)
def test_rotor_position_setter_raises_validation_error(
    wiring: str,
    lower_bound: int,
    upper_bound: int,
    mult_chars: str,
    invalid_char: str,
) -> None:
    """Test that the position setter raises value error for incorrect position values."""
    rotor = Rotor(wiring)
    with pytest.raises(ValueError, match="be in the range"):
        rotor.position = lower_bound - 1
    with pytest.raises(ValueError, match="be in the range"):
        rotor.position = upper_bound + 1
    with pytest.raises(ValueError, match="one character"):
        rotor.position = mult_chars
    with pytest.raises(ValueError, match="not contained"):
        rotor.position = invalid_char

@pytest.mark.parametrize(
        "wiring", [
            wiring_latin(),
            wiring_german()
        ]
)
def test_rotor_position_setter_assigns_correct_values(wiring: str) -> None:
    """Test that rotor posision setter assigns values correctly."""
    rotor = Rotor(wiring)

    for pos, pos_char in enumerate(rotor.alphabet, start=1):
        rotor.position = pos
        assert rotor.position == pos
        assert rotor.position_alph == pos_char

        rotor.position = pos_char

        assert rotor.position == pos
        assert rotor.position_alph == pos_char

@pytest.mark.parametrize(
        ("wiring", "lower_bound", "upper_bound", "mult_chars", "invalid_char"), [
            (wiring_latin(), 1, 26, "AB", "ẞ"),
            (wiring_german(), 1, 30, "AB", "?")
        ]
)
def test_rotor_turnover_setter_raises_validation_error(
    wiring: str,
    lower_bound: int,
    upper_bound: int,
    mult_chars: str,
    invalid_char: str,
) -> None:
    """Test that the turnover setter raises value error for incorrect position values."""
    rotor = Rotor(wiring)
    with pytest.raises(ValueError, match="be in the range"):
        rotor.position = lower_bound - 1
    with pytest.raises(ValueError, match="be in the range"):
        rotor.position = upper_bound + 1
    with pytest.raises(ValueError, match="one character"):
        rotor.position = mult_chars
    with pytest.raises(ValueError, match="not contained"):
        rotor.position = invalid_char

@pytest.mark.parametrize(
        "wiring", [
            wiring_latin(),
            wiring_german()
        ]
)
def test_rotor_turnover_setter_assigns_correct_values(wiring: str) -> None:
    """Test that rotor posision setter assigns values correctly."""
    rotor = Rotor(wiring)

    for pos, pos_char in enumerate(rotor.alphabet, start=1):
        rotor.turnover = pos
        assert rotor.turnover == pos
        assert rotor.turnover_alph == pos_char

        rotor.turnover = pos_char

        assert rotor.turnover == pos
        assert rotor.turnover_alph == pos_char


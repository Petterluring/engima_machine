"""Module for testing rotor.py."""


import pytest

from enigma_machine._internals.alphabet import ENGLISH_ALPHABET
from enigma_machine.rotor import Rotor


def wiring() -> str:
    """Define a fixed wiring to use throughout tests."""
          # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    return "QJXRMPLVOGSIBZTEWCKUYAFNDH"

@pytest.fixture
def rotor() -> Rotor:
    """Return a Rotor using 'wiring' as letter encoding."""
    return Rotor(wiring(), 1)

def test_rotor_init_default_values(rotor: Rotor) -> None:
    """Test that default values are correct in initializer."""
    assert rotor.position == 1
    assert rotor.turnover == 1

def test_rotor_init_assigns_attributes_correctly() -> None:
    """Assert that rotor initializer assigns class attribtues correctly."""
    wiring = "BACDEFGHIJKLMNOPQRSTUVWXYZ"
    rotoR = Rotor(wiring, 24, 5)
    assert rotoR.wiring == wiring
    assert rotoR.position == 24
    assert rotoR.turnover == 5

def test_rotor_init_raises_error_invalid_position() -> None:
    """Test that Rotor initializer raises ValueError when position is outside the bounds [1, 26]."""
    wiring = "BACDEFGHIJKLMNOPQRSTUVWXYZ"
    with pytest.raises(ValueError, match=r"range \[1, 26\]"):
        Rotor(wiring, 0)
    with pytest.raises(ValueError, match=r"range \[1, 26\]"):
        Rotor(wiring, 27)

def test_rotor_turning(rotor: Rotor) -> None:
    """Test rotation mechanism by asserting that 'turn' method increases position value correctly."""
    for position in range(1, 26 + 1):
        assert position == rotor.position
        rotor.turn()

    assert rotor.position == 1 # rotor makes a full turn and goes back to one after rotor position 26.

    assert rotor.turn(steps = 5) == 6

    assert rotor.turn(steps = 26) == 6

    assert rotor.turn(steps = -2) == 4

def test_rotor_encode_raises_incorrect_length_error(rotor: Rotor) -> None:
    """Test that map function raises value error for input letters with more or less characters than 1."""
    with pytest.raises(ValueError, match="one character"):
        rotor.encode("AHB")
    with pytest.raises(ValueError, match="one character"):
        rotor.encode("")

def test_wiring_map_raises_character_not_contained_error(rotor: Rotor) -> None:
    """Test that map function raises value error for characters that are not in the alphabet."""
    with pytest.raises(ValueError, match="not contained"):
        rotor.encode("?")
    with pytest.raises(ValueError, match="not contained"):
        rotor.encode("=")

def test_rotor_encoding_without_turning(rotor: Rotor) -> None:
    """Test if rotor returns the correct encodings without any turning."""
    wirinG = wiring()
    for alph_letter, encoded_letter in zip(ENGLISH_ALPHABET, wirinG, strict=False):
        assert rotor.encode(alph_letter) == encoded_letter

    for alph_letter, encoded_letter in zip(ENGLISH_ALPHABET, wirinG, strict=False):
        assert rotor.encode(encoded_letter, reverse=True) == alph_letter

def test_rotor_encoding_with_turning(rotor: Rotor) -> None:
    """Test that a rotation steps shifts the input letters correctly."""
    input_letter = "A"
    rotor.position = 1

    assert rotor.encode(input_letter, turn=True) == "I" # MARKER
    assert rotor.encode(input_letter, turn=True) == "V"
    assert rotor.encode(input_letter, turn=True) == "O"
    """
    Encoding process of MARKER (rotor position = 2):

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


def test_rotor_position_setter_raises_validation_error(rotor: Rotor) -> None:
    """Test that the position setter raises value error for incorrect position values."""
    with pytest.raises(ValueError, match="be in the range"):
        rotor.position = 27
    with pytest.raises(ValueError, match="be in the range"):
        rotor.position = 0
    with pytest.raises(ValueError, match="one character"):
        rotor.position = "AB" # type:ignore[assignment]
    with pytest.raises(ValueError, match="not contained"):
        rotor.position = "?" # type:ignore[assignment]

def test_rotor_position_setter_assigns_correct_values(rotor: Rotor) -> None:
    """Test that rotor posision setter assigns values correctly."""
    rotor.position = 20
    assert rotor.position == 20

    rotor.position = 1
    assert rotor.position == 1

    rotor.position = "A" # type:ignore[assignment]
    assert rotor.position == 1
    assert rotor.position_alph == "A"

    rotor.position = "C" # type:ignore[assignment]
    assert rotor.position == 3
    assert rotor.position_alph == "C"

def test_rotor_turnover_setter_raises_validation_error(rotor: Rotor) -> None:
    """Test that the turnover setter raises value error for incorrect position values."""
    with pytest.raises(ValueError, match="be in the range"):
        rotor.turnover = 27
    with pytest.raises(ValueError, match="be in the range"):
        rotor.turnover = 0
    with pytest.raises(ValueError, match="one character"):
        rotor.turnover = "AB" # type:ignore[assignment]
    with pytest.raises(ValueError, match="not contained"):
        rotor.turnover = "?" # type:ignore[assignment]

def test_rotor_turnover_setter_assigns_correct_values(rotor: Rotor) -> None:
    """Test that rotor posision setter assigns values correctly."""
    rotor.turnover = 20
    assert rotor.turnover == 20

    rotor.turnover = 1
    assert rotor.turnover == 1

    rotor.turnover = "A" # type:ignore[assignment]
    assert rotor.turnover == 1
    assert rotor.turnover_alph == "A"

    rotor.turnover = "C" # type:ignore[assignment]
    assert rotor.turnover == 3
    assert rotor.turnover_alph == "C"

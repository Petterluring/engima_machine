"""Module for testing rotor.py."""


import pytest

from enigma_machine._internals.alphabet import ENGLISH_ALPHABET
from enigma_machine.rotor import Rotor


def wiring() -> str:
    """Define a fixed wiring to use throughout tests."""
    return "BCDEFGHIJKLMNOPQRSTUVWXYZA"

@pytest.fixture
def rotor() -> Rotor:
    """Return a Rotor using 'wiring' as letter encoding."""
    return Rotor(wiring(), 0)

def test_rotor_init_default_values(rotor: Rotor) -> None:
    """Test that default values are correct in initializer."""
    assert rotor.position == 1

def test_rotor_init_assigns_attributes_correctly() -> None:
    """Assert that rotor initializer assigns class attribtues correctly."""
    wiring = "BACDEFGHIJKLMNOPQRSTUVWXYZ"
    rotoR = Rotor(wiring, 24)
    assert rotoR.wiring == wiring
    assert rotoR.position == 25

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
    alph_letter = "A"
    rotor.position = 26 # 'encode' method turns the rotor first before encoding,
                        # meaning that we start at position 26 such that the first position
                        # when calling 'encode' with turn=True becomes 1
    for _ in range(0, 26):
        assert rotor.encode(alph_letter, turn=True)

    rotor.position = 26
    encoded_letter = wiring()[0]
    for alph_letter in ENGLISH_ALPHABET:
        assert rotor.encode(encoded_letter, reverse=True, turn=True) == alph_letter

def test_rotor_position_setter_raises_validation_error(rotor: Rotor) -> None:
    """Test that the position setter raises value error for incorrect position values."""
    with pytest.raises(ValueError, match="be in the range"):
        rotor.position = 27
    with pytest.raises(ValueError, match="be in the range"):
        rotor.position = 0

def test_rotor_position_setter_assigns_correct_values(rotor: Rotor) -> None:
    """Test that rotor posision setter assigns values correctly."""
    rotor.position = 20
    assert rotor.position == 20

    rotor.position = 1
    assert rotor.position == 1

def test_rotor_position_setter_assigns_correct_values_using_strings(rotor: Rotor) -> None:
    """Test that rotor posision setter assigns values correctly."""
    rotor.position = 20
    assert rotor.position == 20

    rotor.position = 1
    assert rotor.position == 1

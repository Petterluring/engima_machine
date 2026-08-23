"""Test module for plugboard.py."""

import pytest

from enigma_machine.alphabet.alphabet import ENGLISH_ALPHABET
from enigma_machine.alphabet.errors import InternalStateError
from enigma_machine.plugboard.plugboard import Plugboard


@pytest.fixture
def plugboard() -> Plugboard:
    """Return a basic Plugboard that can be used throughout tests."""
    return Plugboard()

@pytest.fixture
def full_plugboard() -> Plugboard:
    """Return a fully occupied plugboard with 13 cords."""
    return Plugboard(
        ("A", "B"),
        ("C", "D"),
        ("E", "F"),
        ("G", "H"),
        ("I", "J"),
        ("K", "L"),
        ("M", "N"),
        ("O", "P"),
        ("Q", "R"),
        ("S", "T"),
        ("U", "V"),
        ("W", "X"),
        ("Y", "Z"),
    )

def test_plugboard_encodes_correctly_no_cords(plugboard: Plugboard) -> None:
    """Test that the plugboard encodes input letters to themselves when no cords are used."""
    for letter in ENGLISH_ALPHABET:
        assert letter == plugboard.encode(letter)

def test_plugboard_encodes_correctly(plugboard: Plugboard) -> None:
    """Test that the plugboard encodes input letters correctly when cords are used."""
    plugboard.add_cord(("A", "C"))
    plugboard.add_cord(("B", "Z"))
    plugboard.add_cord(("T", "J"))

    assert plugboard.encode("A") == "C"
    assert plugboard.encode("B") == "Z"

    assert plugboard.encode("C") == "A"
    assert plugboard.encode("Z") == "B"

    assert plugboard.encode("T") == "J"
    assert plugboard.encode("J") == "T"

    assert plugboard.encode("W") == "W"

def test_plugboard_raises_error_when_cord_letters_are_equal(plugboard: Plugboard) -> None:
    """Test that the plugboard raises a ValueError when letters are equal in the cord pair."""
    with pytest.raises(ValueError, match="different"):
        plugboard.add_cord(("A", "A"))
    with pytest.raises(ValueError, match="different"):
        plugboard.add_cord(("B", "B"))

def test_plugboard_raises_error_when_cord_already_exists(plugboard: Plugboard) -> None:
    """Test that the plugboard raises ValueError when a cord already exists."""
    plugboard.add_cord(("A", "B"))
    with pytest.raises(ValueError, match="already exists"):
        plugboard.add_cord(("A", "B"))
    with pytest.raises(ValueError, match="already exists"):
        plugboard.add_cord(("B", "A"))

    # Cords involving A or B along with other letters should raise errors.
    with pytest.raises(ValueError, match="already exists"):
        plugboard.add_cord(("B", "C"))
    with pytest.raises(ValueError, match="already exists"):
        plugboard.add_cord(("Z", "B"))
    with pytest.raises(ValueError, match="already exists"):
        plugboard.add_cord(("A", "C"))
    with pytest.raises(ValueError, match="already exists"):
        plugboard.add_cord(("T", "A"))

def test_plugboard_raises_error_when_13_cords_in_use(full_plugboard: Plugboard) -> None:
    """Test that plugboard raises an internal state error when plugboard is full."""
    assert len(full_plugboard) == 13
    with pytest.raises(InternalStateError, match="13 cords"):
        full_plugboard.add_cord(("A", "G"))

def test_plugboard_can_check_cord_existence(full_plugboard: Plugboard) -> None:
    """Test if a given cord exists in the plugboard."""
    assert full_plugboard.cord_exists(("A", "B")) is True
    assert full_plugboard.cord_exists(("B", "A")) is True

    assert full_plugboard.cord_exists(("C", "D")) is True
    assert full_plugboard.cord_exists(("D", "C")) is True


def test_plugboard_can_remove_cord(full_plugboard: Plugboard) -> None:
    """Test if plugboard can remove cords."""
    full_plugboard.remove_cord(("A", "B"))
    assert full_plugboard.cord_exists(("A", "B")) is False
    assert full_plugboard.cord_exists(("B", "A")) is False

    full_plugboard.remove_cord(("C", "D"))
    assert full_plugboard.cord_exists(("C", "D")) is False
    assert full_plugboard.cord_exists(("D", "C")) is False

    full_plugboard.remove_cord(("F", "E"))
    assert full_plugboard.cord_exists(("E", "F")) is False
    assert full_plugboard.cord_exists(("F", "E")) is False


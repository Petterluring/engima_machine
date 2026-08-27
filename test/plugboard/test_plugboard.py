"""Test module for plugboard.py."""
import pytest

from enigma_machine.alphabet import Alphabet
from enigma_machine.alphabet.errors import InternalStateError
from enigma_machine.config import PlugboardConfig
from enigma_machine.plugboard import Plugboard

__INSTANCES = {
    "latin": Alphabet.LATIN_ALPHABET,
    "german": Alphabet.GERMAN_ALPHABET
}

def _empty_plugboard(alphabet: Alphabet) -> Plugboard:
    return Plugboard(alphabet=alphabet)

@pytest.fixture
def plugboard_latin() -> Plugboard:
    """Return a basic Plugboard that can be used throughout tests."""
    return Plugboard(alphabet=Alphabet.LATIN_ALPHABET)

@pytest.fixture
def full_plugboard_latin() -> Plugboard:
    """Return a fully occupied plugboard with 13 cords using the Latin alphabet."""
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
        alphabet=Alphabet.LATIN_ALPHABET
    )

@pytest.fixture
def full_plugboard_german() -> Plugboard:
    """Return a fully occupied plugboard with 13 cords using the Latin alphabet."""
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
        ("Ä", "Ö"),
        ("Ü", "ẞ"),
        alphabet=Alphabet.GERMAN_ALPHABET
    )

@pytest.mark.parametrize(
        "alphabet",
        [
            "latin",
            "german"
        ]
)
def test_plugboard_encodes_correctly_no_cords(alphabet: str) -> None:
    """Test that the plugboard encodes input letters to themselves when no cords are used."""
    plugboard = _empty_plugboard(__INSTANCES[alphabet])
    for letter in plugboard.alphabet.value:
        assert letter == plugboard.encode(letter)

def test_plugboard_encodes_correctly() -> None:
    """Test that the plugboard_latin encodes input letters correctly when cords are used."""
    plugboard_latin = _empty_plugboard(Alphabet.LATIN_ALPHABET)
    plugboard_latin.add_cord(("A", "C"))
    plugboard_latin.add_cord(("B", "Z"))
    plugboard_latin.add_cord(("T", "J"))

    assert plugboard_latin.encode("A") == "C"
    assert plugboard_latin.encode("B") == "Z"

    assert plugboard_latin.encode("C") == "A"
    assert plugboard_latin.encode("Z") == "B"

    assert plugboard_latin.encode("T") == "J"
    assert plugboard_latin.encode("J") == "T"

    assert plugboard_latin.encode("W") == "W"
    assert plugboard_latin.encode("D") == "D"

    plugboard_german = _empty_plugboard(Alphabet.GERMAN_ALPHABET)

    plugboard_german.add_cord(("Ä", "Ö"))
    plugboard_german.add_cord(("Ü", "ẞ"))

    assert plugboard_german.encode("Ä") == "Ö"
    assert plugboard_german.encode("Ü") == "ẞ"

    assert plugboard_german.encode("Ö") == "Ä"
    assert plugboard_german.encode("ẞ") == "Ü"

def test_plugboard_raises_error_when_cord_letters_are_equal(plugboard_latin: Plugboard) -> None:
    """Test that the plugboard raises a ValueError when letters are equal in the cord pair."""
    with pytest.raises(ValueError, match="different"):
        plugboard_latin.add_cord(("A", "A"))
    with pytest.raises(ValueError, match="different"):
        plugboard_latin.add_cord(("B", "B"))

def test_plugboard_raises_error_when_letters_are_occupied(plugboard_latin: Plugboard) -> None:
    """Test if the plugboard raises ValueError when a cord already connects occupies two letters."""
    plugboard_latin.add_cord(("A", "B"))
    with pytest.raises(ValueError, match="already connected"):
        plugboard_latin.add_cord(("A", "B"))
    with pytest.raises(ValueError, match="already connected"):
        plugboard_latin.add_cord(("B", "A"))

    # Cords involving A or B along with other letters should raise errors.
    with pytest.raises(ValueError, match="already connected"):
        plugboard_latin.add_cord(("B", "C"))
    with pytest.raises(ValueError, match="already connected"):
        plugboard_latin.add_cord(("Z", "B"))
    with pytest.raises(ValueError, match="already connected"):
        plugboard_latin.add_cord(("A", "C"))
    with pytest.raises(ValueError, match="already connected"):
        plugboard_latin.add_cord(("T", "A"))

def test_plugboard_raises_error_when_13_cords_in_use(
        full_plugboard_latin: Plugboard,
        full_plugboard_german: Plugboard
) -> None:
    """Test that plugboard raises an internal state error when plugboard is full."""
    with pytest.raises(InternalStateError, match="13 cords"):
        full_plugboard_latin.add_cord(("A", "G"))
    with pytest.raises(InternalStateError, match="15 cords"):
        full_plugboard_german.add_cord(("Ä", "Ö"))

def test_plugboard_can_check_cord_existence(full_plugboard_latin: Plugboard) -> None:
    """Test if a given cord exists in the plugboard."""
    assert full_plugboard_latin.cord_exists(("A", "B")) is True
    assert full_plugboard_latin.cord_exists(("B", "A")) is True

    assert full_plugboard_latin.cord_exists(("C", "D")) is True
    assert full_plugboard_latin.cord_exists(("D", "C")) is True


def test_plugboard_can_remove_cord(full_plugboard_latin: Plugboard) -> None:
    """Test if plugboard can remove cords."""
    full_plugboard_latin.remove_cord(("A", "B"))
    assert full_plugboard_latin.cord_exists(("A", "B")) is False
    assert full_plugboard_latin.cord_exists(("B", "A")) is False

    full_plugboard_latin.remove_cord(("C", "D"))
    assert full_plugboard_latin.cord_exists(("C", "D")) is False
    assert full_plugboard_latin.cord_exists(("D", "C")) is False

    full_plugboard_latin.remove_cord(("F", "E"))
    assert full_plugboard_latin.cord_exists(("E", "F")) is False
    assert full_plugboard_latin.cord_exists(("F", "E")) is False


def test_plugboard_init_from_config() -> None:
    """Test if Plugboard can initialize from config file."""
    plugboard_config = PlugboardConfig(
        cords=[
            ("A", "C"),
            ("B", "D"),
        ],
        alphabet="LATIN_ALPHABET",
    )

    plugboard = Plugboard.from_config(plugboard_config)

    assert plugboard.cord_exists(("A", "C")) is True
    assert plugboard.cord_exists(("C", "A")) is True

    assert plugboard.cord_exists(("B", "D")) is True
    assert plugboard.cord_exists(("D", "B")) is True

    assert plugboard.alphabet == Alphabet.LATIN_ALPHABET

"""Tests for wiring.py module."""
import pytest

from enigma_machine.rotor._wiring import Wiring


@pytest.mark.parametrize(
        "permutation", [
            "ABCDEF",
            "ABCDEFGHR",
            "ADFFR",
            "AKKLRMT",
            "AKKLRMTEJRIOIFJJEIRLFJJEJFJLRRHFE",
            "AKKLRMTAKJHERIHFIEHFIOEQHJEFKJHEFEF",
        ]
)
def test_wiring_incorrect_permutation_length_error(permutation: str) -> None:
    """Test that Wiring raises value error for permutations that are too short or long."""
    with pytest.raises(ValueError, match="regex pattern"):
        Wiring(permutation)


@pytest.mark.parametrize(
    "permutation",
    [
        "ABCDEFGHIJKLMNOPQRSTUVWXYY",
        "AABCDEFGHIJKLMNOPQRSTUVWXY",
        "ABCDEFGHIJKLMNOPQRSTUVWWYZ",
    ],
)
def test_wiring_non_unique_letters_in_permutation_error(permutation: str) -> None:
    """Test that Wiring raises value error for permutations with non-unique letters."""
    with pytest.raises(ValueError, match="unique letters"):
        Wiring(permutation)

def test_wiring_converts_permutation_to_upper_case() -> None:
    """Test that Wiring class will convert a given permutation to uppercase letters."""
    lower_case_per = "abcdefghijklmnopqrstuvwxyz"
    expected = lower_case_per.upper()

    wiring = Wiring(lower_case_per)
    assert wiring.permutation == expected

@pytest.fixture
def wiring() -> Wiring:
    """Fixed Wiring instance."""
    permutation = "BCDEFGHIJKLMNOPQRSTUVWXYZA"
    return Wiring(permutation)

@pytest.mark.parametrize(
    ("letter", "expected_mapping"),
    [
        ("A", "B"),
        ("C", "D"),
        ("E", "F"),
    ],
)
def test_wiring_map_maps_letters_correctly(
    wiring: Wiring,
    letter: str,
    expected_mapping: str
) -> None:
    """Test that map method maps letters correctly."""
    mapping = wiring.encode(letter)
    assert mapping == expected_mapping

@pytest.mark.parametrize(
    ("letter", "expected_mapping"),
    [
        ("B", "A"),
        ("D", "C"),
        ("F", "E"),
    ],
)
def test_wiring_map_maps_letters_correctly_reversed(
    wiring: Wiring,
    letter: str,
    expected_mapping: str,
) -> None:
    """Test that map method maps letters correctly when reversed = True."""
    mapping = wiring.encode(letter, reverse=True)
    assert mapping == expected_mapping

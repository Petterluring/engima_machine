"""Tests for reflector.py module."""
import pytest

from enigma_machine._reflector.reflector import Reflector


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
def test_reflector_incorrect_permutation_length_error(permutation: str) -> None:
    """Test that Reflector raises value error for permutations that are too short or long."""
    with pytest.raises(ValueError, match="permutation of"):
        Reflector(permutation)

@pytest.mark.parametrize(
    "permutation",
    [
        "ABCDEFGHIJKLMNOPQRSTUVWXYY",
        "AABCDEFGHIJKLMNOPQRSTUVWXY",
        "ABCDEFGHIJKLMNOPQRSTUVWWYZ",
    ],
)
def test_reflector_non_unique_letters_in_permutation_error(permutation: str) -> None:
    """Test that Reflector raises value error for permutations with non-unique letters."""
    with pytest.raises(ValueError, match="permutation of"):
        Reflector(permutation)

def test_reflector_converts_permutation_to_upper_case() -> None:
    """Test that Reflector class will convert a given permutation to uppercase letters."""
    lower_case_per = "abcdefghijklmnopqrstuvwxyz"
    upper_case_per = lower_case_per.upper()
    expected = upper_case_per[13:26] + upper_case_per[:13]

    wiring = Reflector(lower_case_per)
    assert wiring.permutation == expected

@pytest.fixture
def reflector() -> Reflector:
    """Fixed Reflector instance."""
    first_half  = "BCDEFGHIJKLMN"
    second_half = "OPQRSTUVWXYZA"
    return Reflector(first_half + second_half)

@pytest.mark.parametrize(
    ("letter", "expected_encoding"),
    [
        ("B", "O"),
        ("O", "B"),
        ("C", "P"),
        ("P", "C"),
        ("F", "S"),
        ("S", "F"),
    ],
)
def test_reflector_encodes_letters_correctly(
    reflector: Reflector,
    letter: str,
    expected_encoding: str
) -> None:
    """Test that encode method encodes letters correctly."""
    encoding = reflector.encode(letter)
    assert encoding == expected_encoding

"""Test module for alphabet.py."""

import pytest

from enigma_machine.alphabet.alphabet import Alphabet

_LATIN_ALPHABET = "latin_alphabet"
_GERMAN_ALPHABET = "german_alphabet"

_INSTANCES = {
    _LATIN_ALPHABET: Alphabet.LATIN_ALPHABET,
    _GERMAN_ALPHABET: Alphabet.GERMAN_ALPHABET
}

@pytest.mark.parametrize(
    ("alphabet", "letter_input", "expected"),
    [
        (_LATIN_ALPHABET, "a", "A"),
        (_LATIN_ALPHABET, "b", "B"),
        (_LATIN_ALPHABET, "c", "C"),
        (_GERMAN_ALPHABET, "a", "A"),
        (_GERMAN_ALPHABET, "ä", "Ä"),
        (_GERMAN_ALPHABET, "ö", "Ö"),
        (_GERMAN_ALPHABET, "ü", "Ü"),
        (_GERMAN_ALPHABET, "ß", "ẞ")
    ]
)
def test_alphabet_normalizes_letters(
        alphabet: str,
        letter_input: str,
        expected: str,
) -> None:
    """Test that Alphabet class can normalize letters based on supported alphabets."""
    alph_instance = _INSTANCES[alphabet]
    result = alph_instance.normalize(letter_input)
    assert result == expected

@pytest.mark.parametrize(
    ("input", "match"),
    [
        ("ABC", "one character"),
        ("AHYTD", "one character"),
        ("!", "not contained"),
        ("€", "not contained"),
    ]
)
def test_alphabet_identifies_invalid_letters_during_normalization(
    input: str,
    match: str
) -> None:
    """Test if alphabet raises ValueError for invalid letter values."""
    alph_instance = Alphabet.LATIN_ALPHABET
    with pytest.raises(ValueError, match=match):
        alph_instance.normalize(input)

@pytest.mark.parametrize(
    "alphabet",
    [
        _LATIN_ALPHABET,
        _GERMAN_ALPHABET
    ]
)
def test_alphabet_index_letters_correctly(
    alphabet: str
) -> None:
    """Test if letters have correct indices."""
    alph_instance = _INSTANCES[alphabet]
    for i, letter in enumerate(alph_instance.value):
        assert i == alph_instance.index(letter)

@pytest.mark.parametrize(
    ("alphabet", "permutation", "expected"),
    [
        (_LATIN_ALPHABET, "QWERTYUIOPASDFGHJKLZXCVBNM", True),
        (_LATIN_ALPHABET, "ABCDEF", False),
        (_LATIN_ALPHABET, "ABDEFGHIJKLMNOPQRSTUVWXYZA", False),
        (_LATIN_ALPHABET, "QWERTZUIOPASDFGHJKLYXCVBNMÄÖÜẞ", False),
        (_GERMAN_ALPHABET, "QWERTZUIOPASDFGHJKLYXCVBNMÄÖÜẞ", True),
        (_GERMAN_ALPHABET, "ABCDEF", False),
        (_GERMAN_ALPHABET, "ABDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞA", False),
        (_GERMAN_ALPHABET, "ABDEFGHIJKLMNOPQRSTUVWXYZA", False),
    ]
)
def test_alphabet_validate_permutations_correctly(
    alphabet: str,
    permutation: str,
    expected: bool,
) -> None:
    """Test that alphabet validates permutations correctly."""
    alph_instance = _INSTANCES[alphabet]
    assert alph_instance.validate_permutation(permutation) is expected

@pytest.mark.parametrize(
        ("permutation", "norm_permutation", "inferred_alph"),
        [
            ("ABCDEFGHiJKLmNOPQRSTUVWXYz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", _LATIN_ALPHABET),
            ("QWERTYuIOPASDFGHJKLZXCVbnm", "QWERTYUIOPASDFGHJKLZXCVBNM", _LATIN_ALPHABET),
            ("ABCDEFGHIJKLMNOPqRSTUVWXYZäöÜẞ", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ", _GERMAN_ALPHABET),
            ("QWERTZUIOPASDFGHJKLYxCVBNMÄÖÜß", "QWERTZUIOPASDFGHJKLYXCVBNMÄÖÜẞ", _GERMAN_ALPHABET),
        ]
)
def test_alphabet_normalizes_permutations_and_infers_alphabets(
        permutation: str,
        norm_permutation: str,
        inferred_alph: str,
) -> None:
    """Test if alphabet normalizes a permutation and infers the alphabet it originates from."""
    alphabet, permutatioN = Alphabet.infer_alphabet_and_normalize(permutation)
    assert permutatioN == norm_permutation
    assert alphabet == _INSTANCES[inferred_alph]

@pytest.mark.parametrize(
        ("permutation", "match"),
        [
            ("ABC", "one permutation of"),
            ("093iohjefw", "one permutation of")
        ]
)
def test_alphabet_raises_error_when_infered_alphabet_is_not_found(
    permutation: str,
    match: str,
) -> None:
    """Test if alphabet raises ValueError when it cannot find the originating alphabet for an invalid permutation."""
    with pytest.raises(ValueError, match=match):
        Alphabet.infer_alphabet_and_normalize(permutation)

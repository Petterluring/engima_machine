"""Tests regex.py file."""
from enigma_machine.utils.regex import build_regex_pattern


def test_returned_regex_function() -> None:
    """Test that the returned function from build_regex_pattern matches input strings correctly."""
    matches = build_regex_pattern("ABC")
    assert matches("ABC")  is True
    assert matches("ABCD") is False
    assert matches("AB")   is False


def test_returned_regex_function_using_uppercase_alphabet() -> None:
    """Test that the returned function from build_regex_pattern can match [A-Z] patterns."""
    matches = build_regex_pattern("[A-Z]{5}")
    assert matches("ABCDE")  is True
    assert matches("ABCDF")  is True
    assert matches("ABCDG")  is True
    assert matches("ZBCDG")  is True
    assert matches("ZBCDGT") is False
    assert matches("ZBCeG")  is False

"""Module for regex utilities."""

from collections.abc import Callable
from re import compile


def build_regex_pattern(reg_pattern: str) -> Callable[[str], bool]:
    """Return a function that checks if a string matches the given regex pattern.

    Args:
        reg_pattern (str): The regex pattern to compile.

    Returns:
        Callable[[str], bool]: A function that takes a string and returns True if it matches the regex pattern,
                               False otherwise.
    """
    pattern = compile(reg_pattern)

    def matches(input: str) -> bool:
        return bool(pattern.fullmatch(input))

    return matches

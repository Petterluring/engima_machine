"""Module containing validation logic for alphabet permutations."""

from collections.abc import Callable
from dataclasses import dataclass
from re import compile


def _build_regex_pattern(reg_pattern: str) -> Callable[[str], bool]:
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

_REGEX_PATTERN = f"[A-Z]{{{26}}}"
_REGEX_MATCHER = _build_regex_pattern(_REGEX_PATTERN)


@dataclass(frozen=True, slots=True)
class Permutation:
    """Validates a permutation of the alphabet by ensuring it contains 26 unique letters."""

    value: str

    def __post_init__(self) -> None:
        """Validate the permutation and convert it to uppercase."""
        value = self.value.strip().upper()

        # Require value to only include alphabetic letters of length 26
        if not _REGEX_MATCHER(value):
            raise ValueError(f"{value} must match {_REGEX_PATTERN} regex pattern.")

        # Require the letters in value to be unique
        if not len(value) == len(set(value)):
            raise ValueError(f"{value} must have unique letters.")

        object.__setattr__(self, "value", value)

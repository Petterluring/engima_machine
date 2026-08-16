"""Module containing validation logic for alphabet permutations."""

from re import compile

from .keyboard import Keyboard

_REGEX_PATTERNS = {
    Keyboard.LATIN_ALPHABET: r"[A-Z]{26}",
    Keyboard.GERMAN_ALPHABET: r"[A-ZÄÖÜß]{26}"
}

def validate_alph_permutation(value: str) -> tuple[str, str]:
    """Validate a permutation against a predefined keyboard layout and return the layout and permutation in uppercase.

    Args:
        value: str - The permutation to validate.

    Returns:
        tuple[str, str] - (keyboard layout, permutation)
    """
    value_upper = value.strip().upper()

    for keyboard in Keyboard:
        regex_pattern = _REGEX_PATTERNS[keyboard]
        pattern = compile(regex_pattern)

        if bool(pattern.fullmatch(value_upper)):
            if len(keyboard.layout) != len(set(value_upper)):
                break
            return (keyboard.layout, value_upper)

    raise ValueError(
        f"{value_upper} must be a permutation of one of the following layouts: "
        ", ".join([keyboard.layout for keyboard in Keyboard])
    )

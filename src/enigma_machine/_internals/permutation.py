"""Module containing validation logic for alphabet permutations."""

from re import compile

from ..keyboard.keyboard import Keyboard

_REGEX_PATTERNS = {
    Keyboard.LATIN_ALPHABET: r"[A-Z]{26}",
    Keyboard.SWEDISH_ALPHABET: r"[A-ZÅÄÖ]{29}",
    Keyboard.GERMAN_ALPHABET: r"[A-ZÄÖÜß]{26}"
}

def validate_alph_permutation(value: str, alphabet: Keyboard = Keyboard.LATIN_ALPHABET) -> str:
    """Validate a permutation of an alphabet by ensuring it contains len(alphabet) unique letters.

    Args:
        value: str - The permutation of the alphabet to validate.
        alphabet: Alphabet - Alphabet to validate against.

    Returns:
        str - Permutation in uppercase letters.
    """
    value_upper = value.strip().upper()

    # Require value to contain alphabetic letters of length 26
    regex_pattern = _REGEX_PATTERNS[alphabet]
    pattern = compile(regex_pattern)
    if not bool(pattern.fullmatch(value_upper)):
        raise ValueError(f"{value_upper} must match {regex_pattern} regex pattern.")

    # Require the letters in value to be unique
    if not len(value) == len(set(value_upper)):
        raise ValueError(f"{value_upper} must have unique letters.")

    return value_upper

"""Module containing validation logic for alphabet permutations."""

from re import compile

from .alphabet import Alphabet, upper

_REGEX_PATTERNS = {
    Alphabet.LATIN_ALPHABET: r"[A-Z]{26}",
    Alphabet.GERMAN_ALPHABET: r"[A-ZÄÖÜß]{30}"
}

def validate_alph_permutation(value: str) -> tuple[str, str]:
    """Validate a permutation against a predefined alphabet and return that alphabet and the permutation in uppercase.

    Args:
        value: str - The permutation to validate.

    Returns:
        tuple[str, str] - (alphabet, permutation)
    """
    value_upper = upper(value)

    for alphabet in Alphabet:
        regex_pattern = _REGEX_PATTERNS[alphabet]
        pattern = compile(regex_pattern)

        if bool(pattern.fullmatch(value_upper)):
            if len(alphabet.value) != len(set(value_upper)):
                break
            return (alphabet.value, value_upper)

    raise ValueError(
        f"{value_upper} must be a permutation of one of the following alphabets: " +
        ", ".join([alphabet.value for alphabet in Alphabet])
    )

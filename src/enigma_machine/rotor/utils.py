"""Utils module for shared functionality in rotor package."""
from enigma_machine.utils.constants import ENGLISH_ALPHABET as ALPHABET


def _normalize_letter(alph_letter: str) -> str:
    """Normalize letter by converting it to uppercase and require it to be one character in the alphabet."""
    if len(alph_letter) != 1:
        raise ValueError('alph_letter should be one character.')

    alph_letter_upper = alph_letter.upper()
    if alph_letter_upper not in ALPHABET:
        raise ValueError('alph_letter is not contained in the alphabet [A-Z]')

    return alph_letter_upper

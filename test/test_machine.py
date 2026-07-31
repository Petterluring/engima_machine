"""Test module for enigma.py."""

import pytest

from enigma_machine.machine import Machine
from enigma_machine.plugboard import Plugboard
from enigma_machine.rotor import Rotor, Rotors


@pytest.fixture
def enigma_machine_no_cords() -> Machine:
    """Return an enigma machine without cords that can be used throughout tests."""
    rotors = Rotors(
        fast_rotor=Rotor("QJXRMPLVOGSIBZTEWCKUYAFNDH"),
        middle_rotor=Rotor("HFQATKXPNYVCLIZRSEUGMBWODJ"),
        slow_rotor=Rotor("WBOSQNZJHEAMFYKTRUIDCGXLVP"),
    )
    return Machine(
        rotors=rotors,
        reflector_wiring="LCYUGRWPAZFVDJQIXSOBETNMHK"
    )

@pytest.fixture
def enigma_machine_with_cords() -> Machine:
    """Return an enigma machine without cords that can be used throughout tests."""
    rotors = Rotors(
            fast_rotor=Rotor("QJXRMPLVOGSIBZTEWCKUYAFNDH"),
            middle_rotor=Rotor("HFQATKXPNYVCLIZRSEUGMBWODJ"),
            slow_rotor=Rotor("WBOSQNZJHEAMFYKTRUIDCGXLVP"),
        )
    return Machine(
        rotors=rotors,
        reflector_wiring="LCYUGRWPAZFVDJQIXSOBETNMHK",
        plugboard=Plugboard(
        ("A", "D"),
        ("B", "Q"),
        ("C", "M"),
        ("E", "Z"),
        ("F", "L"),
        ("G", "X"),
        ("H", "P"),
        ("I", "T"),
        ("J", "N"),
        ("K", "W"),
    )
)



@pytest.mark.parametrize(
    ("msg, config, decoded_msg"),
    [
        ("Oh captain my captain", (4, 2, 3), "OHCAPTAINMYCAPTAIN"),
        ("Hello, World!", (1, 2, 3), "HELLOWORLD"),
        ("The quick brown fox jumps over the lazy dog.", (5, 3, 1), "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"),
        ("Python3.14", (2, 4, 1), "PYTHON"),
        ("1234567890", (3, 1, 2), ""),
        ("     ", (2, 3, 4), ""),
        ("", (1, 2, 3), ""),
        ("!@#$%^&*()", (4, 5, 1), ""),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (1, 3, 5), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("abcdefghijklmnopqrstuvwxyz", (5, 4, 3), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("MiXeD CaSe", (2, 5, 4), "MIXEDCASE"),
        ("One\tTwo\nThree", (3, 2, 5), "ONETWOTHREE"),
        ("   Leading and trailing   ", (1, 5, 2), "LEADINGANDTRAILING"),
        ("A", (2, 1, 4), "A"),
        ("ZZZZZZ", (5, 2, 1), "ZZZZZZ"),
        ("Repeated repeated repeated", (4, 3, 2), "REPEATEDREPEATEDREPEATED"),
        ("Can you read this?", (2, 3, 1), "CANYOUREADTHIS"),
        ("No-dashes_or_underscores.", (5, 1, 4), "NODASHESORUNDERSCORES"),
        ("Enigma Machine 1942", (3, 5, 2), "ENIGMAMACHINE"),
        ("ÅÄÖéèêñ", (1, 4, 5), ""),
        ("Lorem ipsum dolor sit amet.", (2, 1, 5), "LOREMIPSUMDOLORSITAMET"),
    ]
)
def test_enigma_decoding_no_cords(
    enigma_machine_no_cords: Machine,
    msg: str,
    config: tuple[int, int, int],
    decoded_msg: str,
) -> None:
    """Test if the enigma machine decodes letters correctly."""
    fast_rotor_conf, middle_rotor_conf, slow_rotor_conf = config
    enigma_machine_no_cords.rotor_setting = (fast_rotor_conf, middle_rotor_conf, slow_rotor_conf)

    encoded_message = enigma_machine_no_cords.encode_message(msg)

    enigma_machine_no_cords.rotor_setting = (fast_rotor_conf, middle_rotor_conf, slow_rotor_conf)
    assert decoded_msg == enigma_machine_no_cords.encode_message(encoded_message)

    # encoded letter and original letter should always be different.
    for encoded_letter, decoded_letter in zip(encoded_message, decoded_msg, strict=True):
        assert encoded_letter != decoded_letter

@pytest.mark.parametrize(
    ("msg, config, decoded_msg"),
    [
        ("Oh captain my captain", (4, 2, 3), "OHCAPTAINMYCAPTAIN"),
        ("Hello, World!", (1, 2, 3), "HELLOWORLD"),
        ("The quick brown fox jumps over the lazy dog.", (5, 3, 1), "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"),
        ("Python3.14", (2, 4, 1), "PYTHON"),
        ("1234567890", (3, 1, 2), ""),
        ("     ", (2, 3, 4), ""),
        ("", (1, 2, 3), ""),
        ("!@#$%^&*()", (4, 5, 1), ""),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (1, 3, 5), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("abcdefghijklmnopqrstuvwxyz", (5, 4, 3), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("MiXeD CaSe", (2, 5, 4), "MIXEDCASE"),
        ("One\tTwo\nThree", (3, 2, 5), "ONETWOTHREE"),
        ("   Leading and trailing   ", (1, 5, 2), "LEADINGANDTRAILING"),
        ("A", (2, 1, 4), "A"),
        ("ZZZZZZ", (5, 2, 1), "ZZZZZZ"),
        ("Repeated repeated repeated", (4, 3, 2), "REPEATEDREPEATEDREPEATED"),
        ("Can you read this?", (2, 3, 1), "CANYOUREADTHIS"),
        ("No-dashes_or_underscores.", (5, 1, 4), "NODASHESORUNDERSCORES"),
        ("Enigma Machine 1942", (3, 5, 2), "ENIGMAMACHINE"),
        ("ÅÄÖéèêñ", (1, 4, 5), ""),
        ("Lorem ipsum dolor sit amet.", (2, 1, 5), "LOREMIPSUMDOLORSITAMET"),
    ]
)
def test_enigma_decoding_with_cords(
    enigma_machine_with_cords: Machine,
    msg: str,
    config: tuple[int, int, int],
    decoded_msg: str,
    ) -> None:
    """Test if enigma decodes correctly using the plugboard."""
    fast_rotor_conf, middle_rotor_conf, slow_rotor_conf = config
    enigma_machine_with_cords.rotor_setting = (fast_rotor_conf, middle_rotor_conf, slow_rotor_conf)

    encoded_message = enigma_machine_with_cords.encode_message(msg)

    enigma_machine_with_cords.rotor_setting = (fast_rotor_conf, middle_rotor_conf, slow_rotor_conf)
    assert decoded_msg == enigma_machine_with_cords.encode_message(encoded_message)

    # encoded letter and original letter should always be different.
    for encoded_letter, decoded_letter in zip(encoded_message, decoded_msg, strict=True):
        assert encoded_letter != decoded_letter

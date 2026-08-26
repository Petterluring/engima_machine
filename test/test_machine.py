"""Test module for enigma.py."""

import pytest

from enigma_machine.alphabet import Alphabet
from enigma_machine.config import EnigmaMachineConfig, PlugboardConfig, RotorConfig, RotorsConfig
from enigma_machine.machine import EnigmaMachine
from enigma_machine.plugboard import Plugboard
from enigma_machine.rotor import Rotor, Rotors


@pytest.fixture
def enigma_machine_no_cords() -> EnigmaMachine:
    """Return an enigma machine without cords that can be used throughout tests."""
    rotors = Rotors(
        fast_rotor=Rotor("QJXRMPLVOGSIBZTEWCKUYAFNDH"),
        middle_rotor=Rotor("HFQATKXPNYVCLIZRSEUGMBWODJ"),
        slow_rotor=Rotor("WBOSQNZJHEAMFYKTRUIDCGXLVP"),
    )
    return EnigmaMachine(
        rotors=rotors,
        reflector="LCYUGRWPAZFVDJQIXSOBETNMHK"
    )

@pytest.fixture
def enigma_machine_with_cords() -> EnigmaMachine:
    """Return an enigma machine with a german layout with cords."""
    rotors = Rotors(
            fast_rotor=Rotor("QJXRMPLVOGSIBZTEWCKUYAFNDH"),
            middle_rotor=Rotor("HFQATKXPNYVCLIZRSEUGMBWODJ"),
            slow_rotor=Rotor("WBOSQNZJHEAMFYKTRUIDCGXLVP"),
        )
    return EnigmaMachine(
        rotors=rotors,
        reflector="LCYUGRWPAZFVDJQIXSOBETNMHK",
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
        alphabet=Alphabet.LATIN_ALPHABET
    )
)

@pytest.fixture
def enigma_machine_with_cords_german() -> EnigmaMachine:
    """Return an enigma machine without cords that can be used throughout tests."""
    rotors = Rotors(
            fast_rotor   = Rotor("QJXRMPLVOGSIBÄÖÜẞZTEWCKUYAFNDH"),
            middle_rotor = Rotor("HFQATKXPNYVCLIZRSEUGÄÖÜẞMBWODJ"),
            slow_rotor   = Rotor("ÄÖÜẞWBOSQNZJHEAMFYKTRUIDCGXLVP"),
        )
    return EnigmaMachine(
        rotors=rotors,
        reflector="LCYUGRWPAZFVDJQÄÖÜẞIXSOBETNMHK",
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
        alphabet=Alphabet.GERMAN_ALPHABET
    )
)

def test_enigma_raises_error_when_different_alpahbets() -> None:
    """Test if enigma machine raises ValueError when the encryption components use different alphabets."""
    with pytest.raises(ValueError, match="same alphabet"):
        EnigmaMachine(
            rotors=(
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
             "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ",
            ),
            reflector="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            plugboard=Plugboard(alphabet=Alphabet.GERMAN_ALPHABET)
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
    enigma_machine_no_cords: EnigmaMachine,
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
    enigma_machine_with_cords: EnigmaMachine,
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


@pytest.mark.parametrize(
    ("msg, config, turnover_config, decoded_msg"),
    [
        ("Oh captain my captain", (17, 5, 24), (3, 14, 25), "OHCAPTAINMYCAPTAIN"),
        ("Hello, World!", (8, 20, 11), (19, 2, 16), "HELLOWORLD"),
        ("The quick brown fox jumps over the lazy dog.", (25, 13, 7), (10, 22, 5),
        "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"),
        ("Python3.14", (2, 18, 9), (26, 8, 13), "PYTHON"),
        ("1234567890", (14, 6, 21), (12, 24, 4), ""),
        ("     ", (5, 26, 16), (7, 18, 23), ""),
        ("", (19, 1, 10), (15, 6, 20), ""),
        ("!@#$%^&*()", (12, 23, 3), (1, 17, 11), ""),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (7, 15, 26), (9, 21, 2), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("abcdefghijklmnopqrstuvwxyz", (22, 4, 18), (5, 25, 14), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("MiXeD CaSe", (10, 16, 1), (18, 12, 6), "MIXEDCASE"),
        ("One\tTwo\nThree", (24, 9, 13), (4, 20, 26), "ONETWOTHREE"),
        ("   Leading and trailing   ", (3, 21, 8), (11, 7, 19), "LEADINGANDTRAILING"),
        ("A", (26, 11, 2), (24, 15, 8), "A"),
        ("ZZZZZZ", (15, 7, 20), (13, 1, 22), "ZZZZZZ"),
        ("Repeated repeated repeated", (6, 25, 12), (16, 10, 3), "REPEATEDREPEATEDREPEATED"),
        ("Can you read this?", (13, 17, 4), (2, 23, 9), "CANYOUREADTHIS"),
        ("No-dashes_or_underscores.", (9, 14, 23), (21, 5, 17), "NODASHESORUNDERSCORES"),
        ("Enigma Machine 1942", (20, 3, 15), (8, 26, 12), "ENIGMAMACHINE"),
        ("ÅÄÖéèêñ", (11, 24, 5), (14, 19, 1), ""),
        ("Lorem ipsum dolor sit amet.", (18, 12, 22), (25, 13, 7), "LOREMIPSUMDOLORSITAMET"),
    ]
)
def test_enigma_decoding_with_cords_and_different_turnovers(
    enigma_machine_with_cords: EnigmaMachine,
    msg: str,
    config: tuple[int, int, int],
    turnover_config: tuple[int, int, int],
    decoded_msg: str,
    ) -> None:
    """Test if enigma decodes correctly using the plugboard and different turnovers."""
    fast_rotor_conf, middle_rotor_conf, slow_rotor_conf = config
    enigma_machine_with_cords.rotor_setting = (fast_rotor_conf, middle_rotor_conf, slow_rotor_conf)
    enigma_machine_with_cords.rotor_turnover_setting = (turnover_config[0], turnover_config[1], turnover_config[2])

    encoded_message = enigma_machine_with_cords.encode_message(msg)

    enigma_machine_with_cords.rotor_setting = (fast_rotor_conf, middle_rotor_conf, slow_rotor_conf)
    assert decoded_msg == enigma_machine_with_cords.encode_message(encoded_message)

    # encoded letter and original letter should always be different.
    for encoded_letter, decoded_letter in zip(encoded_message, decoded_msg, strict=True):
        assert encoded_letter != decoded_letter

@pytest.mark.parametrize(
    ("msg, config, decoded_msg"),
    [
        ("Der Kapitän steht auf der Brücke", (4, 2, 3), "DERKAPITÄNSTEHTAUFDERBRÜCKE"),
        ("Hallo, Welt!", (1, 2, 3), "HALLOWELT"),
        ("Der schnelle braune Fuchs springt über den faulen Hund.", (5, 3, 1),
        "DERSCHNELLEBRAUNEFUCHSSPRINGTÜBERDENFAULENHUND"),
        ("Python3.14", (2, 4, 1), "PYTHON"),
        ("1234567890", (3, 1, 2), ""),
        ("     ", (2, 3, 4), ""),
        ("", (1, 2, 3), ""),
        ("!@#$%^&*()", (4, 5, 1), ""),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß", (1, 3, 5), "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ"),
        ("abcdefghijklmnopqrstuvwxyzäöüß", (5, 4, 3), "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ"),
        ("GeMiScHtE ScHrEiBuNg", (2, 5, 4), "GEMISCHTESCHREIBUNG"),
        ("Ein\tZwei\nDrei", (3, 2, 5), "EINZWEIDREI"),
        ("   Führend und abschließend   ", (1, 5, 2), "FÜHRENDUNDABSCHLIEẞEND"),
        ("Ä", (2, 1, 4), "Ä"),
        ("ÖÖÖÖÖÖ", (5, 2, 1), "ÖÖÖÖÖÖ"),
        ("Wiederholt wiederholt wiederholt", (4, 3, 2), "WIEDERHOLTWIEDERHOLTWIEDERHOLT"),
        ("Kannst du diesen Text lesen?", (2, 3, 1), "KANNSTDUDIESENTEXTLESEN"),
        ("Keine-Bindestriche_oder_Unterstriche.", (5, 1, 4), "KEINEBINDESTRICHEODERUNTERSTRICHE"),
        ("Enigma Maschine 1942", (3, 5, 2), "ENIGMAMASCHINE"),
        ("Das schöne Wetter ist heute großartig.", (2, 1, 5), "DASSCHÖNEWETTERISTHEUTEGROẞARTIG"),
    ]
)
def test_enigma_decoding_with_cords_german(
    enigma_machine_with_cords_german: EnigmaMachine,
    msg: str,
    config: tuple[int, int, int],
    decoded_msg: str,
    ) -> None:
    """Test if enigma decodes correctly using the plugboard."""
    fast_rotor_conf, middle_rotor_conf, slow_rotor_conf = config
    enigma_machine_with_cords_german.rotor_setting = (fast_rotor_conf, middle_rotor_conf, slow_rotor_conf)

    encoded_message = enigma_machine_with_cords_german.encode_message(msg)

    enigma_machine_with_cords_german.rotor_setting = (fast_rotor_conf, middle_rotor_conf, slow_rotor_conf)
    assert decoded_msg == enigma_machine_with_cords_german.encode_message(encoded_message)

    # encoded letter and original letter should always be different.
    for encoded_letter, decoded_letter in zip(encoded_message, decoded_msg, strict=True):
        assert encoded_letter != decoded_letter

def test_enigma_init_from_config() -> None:
    """Test if EnimgaMachine can initialize from config."""
    slow_rotor = RotorConfig(
        wiring="DEFGHIJKLMNOPQRSTUVWXYZABC",
        position=1,
        turnover=2,
    )
    middle_rotor = RotorConfig(
            wiring="BCDEFGHIJKLMNOPQRSTUVWXYZA",
            position=4,
            turnover=5,
        )
    fast_rotor = RotorConfig(
            wiring="WBOSQNZJHEAMFYKTRUIDCGXLVP",
            position=6,
            turnover=7,
        )
    rotors_config = RotorsConfig(
        slow_rotor=slow_rotor,
        middle_rotor=middle_rotor,
        fast_rotor=fast_rotor,
    )

    plugboard_config = PlugboardConfig(
            cords=[
                ("A", "C"),
                ("B", "D"),
            ],
            alphabet="LATIN_ALPHABET",
        )

    machine_config = EnigmaMachineConfig(
        rotors=rotors_config,
        reflector="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        plugboard=plugboard_config,
    )

    machine = EnigmaMachine.from_config(machine_config)

    assert machine.reflector_wiring == "NOPQRSTUVWXYZABCDEFGHIJKLM"
    assert machine.rotors is not None
    assert machine.plugboard is not None

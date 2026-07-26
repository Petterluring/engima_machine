"""Test module for enigma.py."""

import pytest

from enigma_machine.enigma.enigma import EnigmaMachine
from enigma_machine.rotor.rotor import Rotor


@pytest.fixture
def enigma_machine() -> EnigmaMachine:
    """Return an enigma machine that can be used throughout tests."""
    return EnigmaMachine(
        fast_rotor=Rotor("QJXRMPLVOGSIBZTEWCKUYAFNDH"),
        middle_rotor=Rotor("HFQATKXPNYVCLIZRSEUGMBWODJ"),
        slow_rotor=Rotor("WBOSQNZJHEAMFYKTRUIDCGXLVP"),
        reflector="LCYUGRWPAZFVDJQIXSOBETNMHK"
    )

def test_enigma_rotors_default_rotor_position_values(enigma_machine: EnigmaMachine) -> None:
    """Test if enigma machine returns the correct default values of the rotor positions."""
    assert enigma_machine.rotor_config == (1, 1, 1)
    assert enigma_machine.rotor_config_letters == ("A", "A", "A")

def test_enigma_rotor_turning(enigma_machine: EnigmaMachine) -> None:
    """Test if enigma machine turns the rotors correctly."""
    enigma_machine.set_rotor_config(
        slow_rotor_pos=26,
        middle_rotor_pos=26,
        fast_rotor_pos=26,
    ) # next encoding will set all three rotor positions (1, 1, 1)

    for slow_rotor_pos in range(1, 26 + 1):
        for middle_rotor_pos in range(1, 26 + 1):
            for fast_rotor_pos in range(1, 26 + 1):
                enigma_machine.encode("A") # Random encoding to trigger rotoring.
                assert enigma_machine.rotor_config == (slow_rotor_pos, middle_rotor_pos, fast_rotor_pos)

    enigma_machine.encode("A")
    assert enigma_machine.rotor_config == (1, 1, 1) # ensure that rotors goes back to (1, 1, 1) after (26, 26, 26)

def test_enigma_sets_correct_rotor_configurations(enigma_machine: EnigmaMachine) -> None:
    """Test if enigma machine can sets its rotor config correctly."""
    enigma_machine.set_rotor_config(1, 2, 3)
    assert enigma_machine.rotor_config == (1, 2, 3)

    for _ in range(26 - (3 - 1)):
        enigma_machine.encode("A") # Random encoding to trigger rotoring
    assert enigma_machine.rotor_config == (1, 3, 1)
    assert enigma_machine.rotor_config_letters == ("A", "C", "A")

def test_enigma_encodings(enigma_machine: EnigmaMachine) -> None:
    """Test if the enigma machine encodes letters correctly.

    fast_rotor_wiring:   QJXRMPLVOGSIBZTEWCKUYAFNDH
    middle_rotor_wiring: HFQATKXPNYVCLIZRSEUGMBWODJ
    slow_rotor_wiring:   WBOSQNZJHEAMFYKTRUIDCGXLVP
    reflector_wiring:    LCYUGRWPAZFVDJQIXSOBETNMHK
    """
    # TODO: implement test once plugboard is implemented
    pass

def test_enigma_decoding(enigma_machine: EnigmaMachine) -> None:
    """Test if the enigma machine decodes letters correctly."""
    # TODO: implement test once plugboard is implemented
    pass

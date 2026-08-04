"""Test module for enigma_I_device.py."""


import pytest

from enigma_machine.factory.enigma_I_device import create_enigma_I_device as factory_func
from enigma_machine.machine import EnigmaDevice


def test_factory_function_raises_error_for_invalid_rotor_identifiers() -> None:
    """Test that the factory method raises ValueErrors for enumerated errors below.

    - Duplicate identifiers.
    - Non-existing identifiers.
    - invalid formats.
    """
    # DUPLICATE IDENTIFIERS
    with pytest.raises(ValueError, match="must be unique"):
        factory_func(1, 1, 2, "A")
    with pytest.raises(ValueError, match="must be unique"):
        factory_func(1, 2, 2, "A")
    with pytest.raises(ValueError, match="must be unique"):
        factory_func(3, 4, 3, "A")

    # NON-EXISTING IDENTIFIERS
    with pytest.raises(ValueError, match="in the range"):
        factory_func(1, 2, 1000, "A")
    with pytest.raises(ValueError, match="in the range"):
        factory_func(1, 1000, 2, "A")
    with pytest.raises(ValueError, match="in the range"):
        factory_func(1000, 1, 2, "A")
    with pytest.raises(ValueError, match="does not exist"):
        factory_func(1, 2, 3, "Z")

    # INVALID FORMATS
    with pytest.raises(ValueError, match="one character"):
        factory_func(1, 2, 3, "ZZ")

def test_factory_function_builds_enigma_device_correctly() -> None:
    """Test that the factory function builds the Enigma I device correctly."""
    device: EnigmaDevice = factory_func(1, 2, 3, "A")
    assert device.rotors.slow_rotor.wiring == "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    assert device.rotors.middle_rotor.wiring == "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    assert device.rotors.fast_rotor.wiring == "BDFHJLCPRTXVZNYEIWGAKMUSQO"

    device = factory_func(5, 1, 4, "A")
    assert device.rotors.slow_rotor.wiring == "VZBRGITYUPSDNHLXAWMJQOFECK"
    assert device.rotors.middle_rotor.wiring == "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    assert device.rotors.fast_rotor.wiring == "ESOVPZJAYQUIRHXLNFTGKDCMWB"

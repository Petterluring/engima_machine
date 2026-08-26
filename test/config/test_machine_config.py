"""Module for testing machine.py."""
from pathlib import Path

import pytest

from enigma_machine.config import EnigmaMachineConfig


@pytest.fixture
def _enigma_yaml() -> str:
    return """
rotors:
  slow_rotor:
    wiring: EKMFLGDQVZNTOWYHXUSPAIBRCJ
    position: 1
    turnover: A
  middle_rotor:
    wiring: AJDKSIRUXBLHWTMCQGZNPYFVOE
    position: 1
    turnover: 3
  fast_rotor:
    wiring: BDFHJLCPRTXVZNYEIWGAKMUSQO
    position: 1
    turnover: 4

reflector: EJMZALYXVBWFCRQUONTSPIKHGD

plugboard:
  cords:
    - [A, B]
    - [C, D]
    - [E, F]
  alphabet: LATIN_ALPHABET

"""

def test_enigma_config_loads_from_yaml(_enigma_yaml: str, tmp_path: Path) -> None:
    """Test if EnigmaMachineConfig can load config from yaml file."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(_enigma_yaml)

    config = EnigmaMachineConfig.from_yaml(config_file)

    assert config.rotors.slow_rotor.wiring == "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    assert config.rotors.slow_rotor.position == 1
    assert config.rotors.slow_rotor.turnover == "A"

    assert config.rotors.middle_rotor.wiring == "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    assert config.rotors.middle_rotor.position == 1
    assert config.rotors.middle_rotor.turnover == 3

    assert config.rotors.fast_rotor.wiring == "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    assert config.rotors.fast_rotor.position == 1
    assert config.rotors.fast_rotor.turnover == 4

    assert config.reflector == "EJMZALYXVBWFCRQUONTSPIKHGD"
    assert config.plugboard.cords == [("A", "B"), ("C", "D"), ("E", "F")]
    assert config.plugboard.alphabet == "LATIN_ALPHABET"

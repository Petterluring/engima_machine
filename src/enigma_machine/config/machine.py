"""Module containing EnigmaMachineConfig model."""


from pathlib import Path

from pydantic import BaseModel

from ..files import load_yaml
from .plugboard import PlugboardConfig
from .rotor import RotorsConfig


class EnigmaMachineConfig(BaseModel):
    """Config model for EnigmaMachine class.

    Attributes:
        reflector_wiring: str - A permutation of an instance in the Alphabet enum.
    """
    rotors: RotorsConfig
    reflector_wiring: str
    plugboard: PlugboardConfig

    @classmethod
    def from_yaml(cls, path: str | Path) -> EnigmaMachineConfig:
        """Load a configuration from a yaml file."""
        content = load_yaml(path)
        return EnigmaMachineConfig.model_validate(content)

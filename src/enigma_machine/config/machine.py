"""Module containing EnigmaMachineConfig."""


from pathlib import Path

from pydantic import BaseModel

from .plugboard import PlugboardConfig
from .rotor import RotorsConfig


class EnigmaMachineConfig(BaseModel):
    """Pydantic model for EnigmaMachine class.

    Attributes:
        rotors: RotorsConfig       - Rotor set to use.
        reflector: str             - See Reflector class in reflector package.
        plugboard: PlugboardConfig - Plugboard to use.
    """
    rotors: RotorsConfig
    reflector: str
    plugboard: PlugboardConfig

    @classmethod
    def from_yaml(cls, path: str | Path) -> None:
        """Load configuration from a yaml file."""
        pass

"""Module containing RotorConfig."""

from pydantic import BaseModel


class RotorConfig(BaseModel):
    """Pydantic model for Rotor class.

    See Rotor class in rotor package for attribute documentation.
    """
    wiring: str
    position: int
    turnover: int | str


class RotorsConfig(BaseModel):
    """Pydantic model for Rotors class.

    See Rotors class in rotor package for attribute documentation.
    """
    fast_rotor: RotorConfig
    middle_rotor: RotorConfig
    slow_rotor: RotorConfig

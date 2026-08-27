"""Module containing RotorConfig."""

from pydantic import BaseModel


class RotorConfig(BaseModel):
    """Configuration model for Rotor class.

    Attributes:
        wiring:   A permutation of an instance in the Alphabet enum.
        position: Initial position of the rotor. Valid range is [1, len(alphabet enum instance)].
        turnover: Defines when the rotor makes a full turn in terms of a position.
        Valid range is [1, len(alphabet instance)] for integers, and [A-LAST_LETTER_ALPHABET_INSTANCE] for strings.
    """
    wiring: str
    position: int
    turnover: int | str


class RotorsConfig(BaseModel):
    """Configuration model for Rotors class."""
    fast_rotor: RotorConfig
    middle_rotor: RotorConfig
    slow_rotor: RotorConfig

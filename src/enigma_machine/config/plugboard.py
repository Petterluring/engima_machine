"""Module containing PlugboardConfig."""

from pydantic import BaseModel


class PlugboardConfig(BaseModel):
    """Configuration model for Plugboard class.

    Attributes:
        cords:    Pairs of letters connected by the plugboard.
        alphabet: Name of an instance in the Alphabet enum.
    """
    cords: list[tuple[str, str]]
    alphabet: str

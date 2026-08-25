"""Module containing PlugboardConfig."""

from pydantic import BaseModel


class PlugboardConfig(BaseModel):
    """Pydantic model for Plugboard class.

    Attributes:
        cords: list[tuple[str, str]] - See Plugboard class in plugboard.py.
        alphabet: str                - Name of some instance in Alphabet enum (alphabet.py).

    See Plugboard class in plugboard package for attribute documentation of cords.
    """
    cords: list[tuple[str, str]]
    alphabet: str

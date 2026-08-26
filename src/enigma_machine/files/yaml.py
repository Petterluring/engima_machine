"""Module for yaml related functionality."""

from pathlib import Path
from typing import Any

from yaml import YAMLError, safe_load

_LEGAL_SUFFIXES = {".yaml", ".yml"}

def load_yaml(path: str | Path) -> dict[Any, Any]:
    """Load yaml file as a python dictionary."""
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Path {path} does not exist.")
    if not path.is_file():
        raise FileNotFoundError(f"Path {path} does not point to a file.")
    if path.suffix not in _LEGAL_SUFFIXES:
        raise ValueError(f"Path must point to a yaml file. Legal suffixes: {_LEGAL_SUFFIXES}")

    try:
        with open(path) as file:
            content = safe_load(file)
    except YAMLError as e:
        raise ValueError(f"Invalid YAML file: {e}") from e

    if not isinstance(content, dict):
        raise TypeError("YAML content is expected to be parsed as a python dictionary.")

    return content

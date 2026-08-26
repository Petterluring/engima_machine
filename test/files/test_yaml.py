"""Test module for yaml.py."""

from pathlib import Path

import pytest

from enigma_machine.files import load_yaml


def test_yaml_loader_raises_error_when_file_not_found(tmp_path: Path) -> None:
    """Test if load_yaml raises ValueError when file not found."""
    non_existent_file = tmp_path / "config.yaml"
    with pytest.raises(FileNotFoundError, match="not exist"):
        load_yaml(non_existent_file)

def test_yaml_loader_raises_error_when_path_not_file(tmp_path: Path) -> None:
    """Test if load_yaml raises ValueError when path does not point to a file."""
    directory = tmp_path / "dummy_dir"
    directory.mkdir()
    with pytest.raises(FileNotFoundError, match="a file"):
        load_yaml(directory)

def test_yaml_loaded_raises_error_when_incorrect_suffix(tmp_path: Path) -> None:
    """Test if load_yaml raises ValueError when file is not yaml file."""
    file_path = tmp_path / "config.txt"
    file_path.write_text("Hello there")
    with pytest.raises(ValueError, match="point to a yaml file"):
        load_yaml(file_path)

def test_yaml_loader_raises_error_when_invalid_yaml(tmp_path: Path) -> None:
    """Test if load_yaml raises ValueError when YAML file is invalid."""
    yaml_file = tmp_path / "config.yaml"
    yaml_file.write_text("[")
    with pytest.raises(ValueError, match="Invalid YAML file"):
        load_yaml(yaml_file)

def test_yaml_loarder_raises_error_when_not_dict(tmp_path: Path) -> None:
    """Test if load_yaml raises TypeError if content is parsed as a list."""
    yaml_file = tmp_path / "config.yaml"
    yaml_file.write_text("- apple\n- banana\n- orange")
    with pytest.raises(TypeError, match="python dictionary"):
        load_yaml(yaml_file)


@pytest.fixture
def valid_yaml_content() -> str:
    """Random content in yaml format."""
    return """
name: "Project Aurora"
version: 1.4
active: true

tags:
  - python
  - yaml
  - testing

settings:
  timeout: 30
  debug: false

database:
  host: "localhost"
  port: 5432

features:
  logging: true
  caching: false
  experimental: null
"""

def test_yaml_loader_returns_dct_from_valid_yaml_file(tmp_path: Path, valid_yaml_content: str) -> None:
    """Test if load_yaml returns a dictionary from a valid yaml file and validate the content."""
    yaml_file = tmp_path / "config.yaml"
    yaml_file.write_text(valid_yaml_content)

    content = load_yaml(yaml_file)

    assert content["name"] == "Project Aurora"
    assert content["version"] == 1.4
    assert content["active"] is True

    assert content["tags"] == ["python", "yaml", "testing"]

    settings = content["settings"]
    assert settings["timeout"] == 30
    assert settings["debug"] is False

    database = content["database"]
    assert database["host"] == "localhost"
    assert database["port"] == 5432

    features = content["features"]
    assert features["logging"] is True
    assert features["caching"] is False
    assert features["experimental"] is None

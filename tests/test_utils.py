import json
import os
import tempfile

from src.utils import load_operations


def test_load_operations_valid_file():
    """Читает валидный JSON-файл."""
    data = [{"id": 1, "amount": 100}]
    with (tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8")
          as f):
        json.dump(data, f)
        temp_path = f.name

    try:
        result = load_operations(temp_path)
        assert result == data
    finally:
        os.unlink(temp_path)


def test_load_operations_file_not_found():
    """Несуществующий файл → []."""
    result = load_operations("nonexistent.json")
    assert result == []


def test_load_operations_empty_file():
    """Пустой файл → []."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = f.name

    try:
        result = load_operations(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_operations_not_list():
    """В файле не список → []."""
    with (tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8")
          as f):
        json.dump({"key": "value"}, f)
        temp_path = f.name

    try:
        result = load_operations(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)

import os
import pytest
from src.decorators import log


# --- Тесты для вывода в консоль ---

def test_log_success_to_console(capsys):
    @log()  # Не передаем filename, значит вывод в консоль
    def add(a, b):
        return a + b

    assert add(5, 3) == 8

    captured = capsys.readouterr()
    # Проверяем упрощенный вывод из ТЗ
    assert "add ok" in captured.out.strip()


def test_log_error_to_console(capsys):
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    # Проверяем, что сообщение об ошибке содержит имя функции и тип ошибки
    assert "divide error: ZeroDivisionError" in captured.out.strip()
    assert "Inputs: (10, 0)" in captured.out.strip()


# --- Тесты для вывода в файл ---
@pytest.fixture
def temp_log_file(tmp_path):
    """Фикстура для создания временного файла лога."""
    return tmp_path / "temp.log"


def test_log_success_to_file(temp_log_file):
    @log(filename=str(temp_log_file))
    def multiply(a, b):
        return a * b

    assert multiply(4, 5) == 20

    with open(temp_log_file, 'r') as f:
        content = f.read()

    assert "multiply ok" in content


def test_log_error_to_file(temp_log_file):
    @log(filename=str(temp_log_file))
    def get_item(lst, index):
        return lst[index]

    with pytest.raises(IndexError):
        get_item([1, 2, 3], 10)

    with open(temp_log_file, 'r') as f:
        content = f.read()

    assert "get_item error: IndexError" in content
    assert "Inputs: ([1, 2, 3], 10)" in content

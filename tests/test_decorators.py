import pytest

from src.decorators import log


@log()
def add(a, b):
    return a + b


@log()
def fail_func(x):
    raise ValueError("Something went wrong")


@log(filename="test_log.txt")
def multiply(a, b):
    return a * b


@log(filename="test_log.txt")
def fail_file(x):
    raise KeyError("Missing key")


def test_success_console_log(capsys):
    result = add(2, 3)
    captured = capsys.readouterr()
    assert result == 5
    assert "add ok" in captured.out


def test_error_console_log(capsys):
    with pytest.raises(ValueError):
        fail_func(10)
    captured = capsys.readouterr()
    assert "fail_func error: ValueError" in captured.out


def test_error_file_log(tmp_path):
    log_file = tmp_path / "file_error.log"

    @log(filename=log_file)
    def error_func(x):
        raise RuntimeError("Fail")

    # Первый вызов — ожидаем ошибку
    with pytest.raises(RuntimeError):
        error_func(123)

    # Второй вызов — снова ожидаем ошибку
    with pytest.raises(RuntimeError):
        error_func(123)

    with open(log_file, encoding="utf-8") as f:
        content = f.read()

    # Проверки
    assert content.count("error_func error: RuntimeError") == 2
    assert content.count("(123,)") == 2
    assert content.count("{}") == 2

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


def test_success_file_log(tmp_path):
    log_file = tmp_path / "file.log"

    @log(filename=log_file)
    def test_func():
        return 42

    result = test_func()
    assert result == 42

    with open(log_file, encoding="utf-8") as f:
        content = f.read()
    assert "test_func ok" in content


def test_error_file_log(tmp_path):
    log_file = tmp_path / "file_error.log"

    @log(filename=log_file)
    def error_func(x):
        raise RuntimeError("Fail")

    with pytest.raises(RuntimeError):
        error_func(123)

    with open(log_file, encoding="utf-8") as f:
        content = f.read()

    assert "error_func error: RuntimeError. Inputs: (123)," in content

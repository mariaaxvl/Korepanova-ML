"""Общие типы и вспомогательные функции команд эмулятора."""
from collections import namedtuple

Result = namedtuple("Result", "out ok exit code")

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_NOT_FOUND = 127


def success(out=""):
    """Результат успешной команды."""
    return Result(out, True, False, EXIT_OK)


def failure(message, code=EXIT_ERROR):
    """Результат команды, завершившейся ошибкой."""
    return Result(message, False, False, code)


def quit_result(code):
    """Результат команды exit: сеанс нужно завершить."""
    return Result("", True, True, code)


def stub_text(name, args):
    """Текст заглушки: имя команды и её аргументы."""
    return " ".join([name, *args])

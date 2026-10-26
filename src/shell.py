"""Интерпретатор команд эмулятора."""
from cmdparser import ParseError, parse
from commands import COMMANDS
from common import EXIT_NOT_FOUND, failure, success


class Shell:
    """Состояние сеанса и выполнение введённых строк."""

    def __init__(self, vfs=None):
        self.vfs = vfs
        self.cwd = []
        self.commands = COMMANDS

    def prompt(self):
        """Приглашение к вводу с текущим каталогом."""
        path = "/".join(self.cwd)
        return f"vfs:/{path}$ "

    def execute(self, line):
        """Выполняет одну строку и возвращает Result."""
        try:
            words = parse(line)
        except ParseError as err:
            return failure(f"parse error: {err}")
        if not words:
            return success()
        handler = self.commands.get(words[0])
        if handler is None:
            message = f"{words[0]}: command not found"
            return failure(message, EXIT_NOT_FOUND)
        return handler(self, words[1:])

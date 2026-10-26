"""Команды эмулятора (этап 1: заглушки)."""
from common import failure, quit_result, stub_text, success


def cmd_ls(shell, args):
    """Заглушка ls: печатает имя и аргументы."""
    return success(stub_text("ls", args))


def cmd_cd(shell, args):
    """Заглушка cd: печатает имя и аргументы."""
    return success(stub_text("cd", args))


def cmd_exit(shell, args):
    """Завершает сеанс; необязательный аргумент - код возврата."""
    code = 0
    if args:
        try:
            code = int(args[0])
        except ValueError:
            return failure(f"exit: {args[0]}: numeric argument required")
    return quit_result(code)


COMMANDS = {"ls": cmd_ls, "cd": cmd_cd, "exit": cmd_exit}

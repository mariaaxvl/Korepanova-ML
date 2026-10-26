"""Команды эмулятора."""
from common import failure, quit_result, stub_text, success
from vfs import VFSError

ROOT = "/"
CURRENT = "."
DIR_MARK = "/"
MAX_PATH_ARGS = 1


def list_names(node):
    """Имена потомков по алфавиту; у каталогов добавляется '/'."""
    return [name + (DIR_MARK if child.is_dir else "")
            for name, child in sorted(node.children.items())]


def cmd_ls(shell, args):
    """ls [путь]: содержимое каталога (заглушка без VFS)."""
    if shell.vfs is None:
        return success(stub_text("ls", args))
    if len(args) > MAX_PATH_ARGS:
        return failure("ls: too many arguments")
    target = args[0] if args else CURRENT
    try:
        node, _ = shell.vfs.lookup(target, shell.cwd)
    except VFSError as err:
        return failure(f"ls: cannot access '{target}': {err}")
    if not node.is_dir:
        return success(target)
    return success("\n".join(list_names(node)))


def cmd_cd(shell, args):
    """cd [путь]: смена каталога (без аргумента - корень)."""
    if shell.vfs is None:
        return success(stub_text("cd", args))
    if len(args) > MAX_PATH_ARGS:
        return failure("cd: too many arguments")
    target = args[0] if args else ROOT
    try:
        node, parts = shell.vfs.lookup(target, shell.cwd)
    except VFSError as err:
        return failure(f"cd: {target}: {err}")
    if not node.is_dir:
        return failure(f"cd: {target}: Not a directory")
    shell.cwd = parts
    return success()


def cmd_pwd(shell, args):
    """pwd: путь текущего каталога."""
    return success(ROOT + ROOT.join(shell.cwd))


def cmd_exit(shell, args):
    """exit [код]: завершает сеанс."""
    code = 0
    if args:
        try:
            code = int(args[0])
        except ValueError:
            return failure(f"exit: {args[0]}: numeric argument required")
    return quit_result(code)


COMMANDS = {"ls": cmd_ls, "cd": cmd_cd, "pwd": cmd_pwd, "exit": cmd_exit}

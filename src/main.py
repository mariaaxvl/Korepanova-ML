"""Точка входа эмулятора (этап 2: параметры командной строки)."""
import argparse
import os
import sys

from common import EXIT_OK
from script import run_script
from shell import Shell

TITLE = "VFS"


def parse_args(argv=None):
    """Разбирает параметры командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор командной строки с виртуальной ФС")
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    parser.add_argument(
        "--headless", action="store_true",
        help="консольный режим без окна (для автоматических тестов)")
    return parser.parse_args(argv)


def debug_params(args):
    """Отладочный вывод всех заданных параметров."""
    lines = ["[debug] параметры запуска:"]
    for name, value in vars(args).items():
        lines.append(f"[debug]   {name} = {value}")
    return "\n".join(lines) + "\n"


def window_title(args):
    """Заголовок окна: имя VFS и (если задан) файл VFS."""
    if args.vfs:
        return f"{TITLE} [{os.path.basename(args.vfs)}]"
    return TITLE


def load_shell(args):
    """Создаёт Shell; возвращает (shell, текст ошибки)."""
    return Shell(), ""


def repl(shell):
    """Консольный цикл ввода-вывода; возвращает код завершения."""
    while True:
        try:
            line = input(shell.prompt())
        except EOFError:
            return EXIT_OK
        result = shell.execute(line)
        if result.out:
            print(result.out)
        if result.exit:
            return result.code


def run_headless(args):
    """Консольный режим."""
    shell, error = load_shell(args)
    sys.stdout.write(debug_params(args) + error)
    if args.script:
        result = run_script(shell, args.script, sys.stdout.write)
        if result and result.exit:
            return result.code
    return repl(shell)


def run_gui(args):
    """Графический режим."""
    import tkinter as tk
    from gui import Terminal

    shell, error = load_shell(args)
    root = tk.Tk()
    banner = debug_params(args) + error
    Terminal(root, shell, window_title(args), banner, args.script)
    root.mainloop()
    return EXIT_OK


def main():
    """Запускает эмулятор в выбранном режиме."""
    args = parse_args()
    code = run_headless(args) if args.headless else run_gui(args)
    sys.exit(code)


if __name__ == "__main__":
    main()

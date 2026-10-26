"""Точка входа эмулятора (этап 1: REPL)."""
import tkinter as tk

from gui import Terminal
from shell import Shell

TITLE = "VFS"


def main():
    """Запускает окно эмулятора."""
    root = tk.Tk()
    Terminal(root, Shell(), TITLE)
    root.mainloop()


if __name__ == "__main__":
    main()

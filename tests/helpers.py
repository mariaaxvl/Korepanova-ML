"""Вспомогательные функции тестов: создание временных ZIP-архивов."""
import os
import tempfile
import zipfile

from vfs import VFS


def make_zip(entries):
    """Создаёт временный ZIP из словаря {путь: содержимое}."""
    handle, path = tempfile.mkstemp(suffix=".zip")
    os.close(handle)
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
    return path


def make_vfs(entries, test):
    """Создаёт VFS из словаря; архив удаляется по окончании теста."""
    path = make_zip(entries)
    test.addCleanup(os.remove, path)
    return VFS(path)

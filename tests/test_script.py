"""Тесты выполнения стартовых скриптов."""
import os
import tempfile
import unittest

from script import run_script
from shell import Shell


def write_script(text):
    """Создаёт временный скрипт и возвращает путь к нему."""
    handle, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        stream.write(text)
    return path


class ScriptTest(unittest.TestCase):
    """Проверки имитации диалога и остановки на ошибке."""

    def run_text(self, text):
        """Выполняет скрипт; возвращает (вывод, результат)."""
        path = write_script(text)
        self.addCleanup(os.remove, path)
        chunks = []
        result = run_script(Shell(), path, chunks.append)
        return "".join(chunks), result

    def test_shows_input_and_output(self):
        """На экран выводятся и ввод, и вывод."""
        out, _ = self.run_text("ls -l\n")
        self.assertEqual(out, "vfs:/$ ls -l\nls -l\n")

    def test_comments_and_blanks(self):
        """Комментарии и пустые строки пропускаются."""
        out, _ = self.run_text("# c\n\nls\n")
        self.assertEqual(out, "vfs:/$ ls\nls\n")

    def test_stops_on_error(self):
        """После первой ошибки остальные строки не выполняются."""
        out, result = self.run_text("ls\nfoo\nls a\n")
        self.assertFalse(result.ok)
        self.assertNotIn("ls a", out)
        self.assertIn("строке 2", out)

    def test_exit_stops_script(self):
        """exit завершает выполнение скрипта."""
        out, result = self.run_text("exit 4\nls\n")
        self.assertEqual((result.exit, result.code), (True, 4))
        self.assertNotIn("ls", out.replace("exit", ""))

    def test_missing_file(self):
        """Отсутствующий скрипт - сообщение об ошибке."""
        chunks = []
        result = run_script(Shell(), "/no/such/script", chunks.append)
        self.assertFalse(result.ok)
        self.assertIn("не удалось открыть", chunks[0])

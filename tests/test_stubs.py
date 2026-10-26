"""Тесты команд-заглушек и exit."""
import unittest

from shell import Shell


class StubTest(unittest.TestCase):
    """Проверки поведения Shell без подключённой VFS."""

    def setUp(self):
        self.shell = Shell()

    def test_ls_stub(self):
        """ls печатает своё имя и аргументы."""
        result = self.shell.execute("ls -l /tmp")
        self.assertEqual((result.out, result.ok), ("ls -l /tmp", True))

    def test_cd_stub(self):
        """cd печатает своё имя и аргументы."""
        self.assertEqual(self.shell.execute("cd /usr").out, "cd /usr")

    def test_exit(self):
        """exit завершает сеанс с заданным кодом."""
        result = self.shell.execute("exit 3")
        self.assertEqual((result.exit, result.code), (True, 3))

    def test_exit_bad_code(self):
        """Нечисловой код - ошибка, сеанс продолжается."""
        result = self.shell.execute("exit abc")
        self.assertEqual((result.ok, result.exit), (False, False))

    def test_unknown_command(self):
        """Неизвестная команда даёт ошибку 127."""
        result = self.shell.execute("foo")
        self.assertEqual((result.ok, result.code), (False, 127))

    def test_parse_error(self):
        """Ошибка разбора возвращается как ошибка команды."""
        self.assertFalse(self.shell.execute('ls "x').ok)

    def test_empty_line(self):
        """Пустая строка ничего не делает."""
        self.assertEqual(self.shell.execute("   ").out, "")

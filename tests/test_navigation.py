"""Тесты ls, cd и pwd на VFS."""
import unittest

from helpers import make_vfs
from shell import Shell

TREE = {
    "root.txt": "корень",
    "a/a.txt": "1",
    "a/b/b.txt": "22",
    "a/b/c/c.txt": "333",
}


class NavigationTest(unittest.TestCase):
    """Проверки навигации по VFS."""

    def setUp(self):
        self.shell = Shell(make_vfs(TREE, self))

    def out(self, line):
        """Выполняет строку и возвращает её вывод."""
        return self.shell.execute(line).out

    def test_ls_root(self):
        """ls показывает каталоги со знаком '/'."""
        self.assertEqual(self.out("ls"), "a/\nroot.txt")

    def test_ls_path(self):
        """ls с путём показывает содержимое каталога."""
        self.assertEqual(self.out("ls a/b"), "b.txt\nc/")

    def test_ls_file(self):
        """ls для файла печатает его имя."""
        self.assertEqual(self.out("ls root.txt"), "root.txt")

    def test_ls_missing(self):
        """ls для отсутствующего пути - ошибка."""
        result = self.shell.execute("ls nope")
        self.assertFalse(result.ok)
        self.assertIn("No such file", result.out)

    def test_cd_and_pwd(self):
        """cd меняет каталог, pwd его показывает."""
        self.shell.execute("cd a/b/c")
        self.assertEqual(self.out("pwd"), "/a/b/c")
        self.assertEqual(self.shell.prompt(), "vfs:/a/b/c$ ")

    def test_cd_parent_and_root(self):
        """cd .. поднимается выше, cd без аргумента - в корень."""
        self.shell.execute("cd a/b")
        self.shell.execute("cd ../..")
        self.assertEqual(self.out("pwd"), "/")
        self.shell.execute("cd a")
        self.shell.execute("cd")
        self.assertEqual(self.out("pwd"), "/")

    def test_cd_errors(self):
        """cd в файл и в отсутствующий путь - ошибки."""
        self.assertIn("Not a directory", self.out("cd root.txt"))
        self.assertIn("No such file", self.out("cd nope"))
        self.assertFalse(self.shell.execute("cd a b").ok)

    def test_failed_cd_keeps_directory(self):
        """Неудачный cd не меняет текущий каталог."""
        self.shell.execute("cd a")
        self.shell.execute("cd nope")
        self.assertEqual(self.out("pwd"), "/a")

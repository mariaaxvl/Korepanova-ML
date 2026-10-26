"""Тесты виртуальной файловой системы."""
import os
import unittest

from helpers import make_vfs, make_zip
from vfs import VFS, VFSError

TREE = {
    "root.txt": "корень",
    "a/": "",
    "a/b/c/deep.txt": "глубоко",
    "bin.dat": bytes([0, 255]),
}


class VfsTest(unittest.TestCase):
    """Проверки загрузки архива и поиска узлов."""

    def setUp(self):
        self.vfs = make_vfs(TREE, self)

    def test_root_children(self):
        """Корень содержит файлы и каталоги архива."""
        self.assertEqual(sorted(self.vfs.root.children),
                         ["a", "bin.dat", "root.txt"])

    def test_implicit_directories(self):
        """Каталоги без явных записей создаются автоматически."""
        node, _ = self.vfs.lookup("/a/b/c", [])
        self.assertTrue(node.is_dir)

    def test_file_data(self):
        """Данные файла доступны в памяти."""
        node, _ = self.vfs.lookup("root.txt", [])
        self.assertEqual(node.data.decode("utf-8"), "корень")

    def test_relative_and_parent(self):
        """Поддерживаются относительные пути, '.' и '..'."""
        self.assertEqual(self.vfs.split("../x/./y", ["a", "b"]),
                         ["a", "x", "y"])

    def test_parent_of_root(self):
        """'..' в корне остаётся в корне."""
        self.assertEqual(self.vfs.split("../..", []), [])

    def test_not_found(self):
        """Отсутствующий путь - VFSError."""
        with self.assertRaises(VFSError):
            self.vfs.lookup("nope", [])

    def test_through_file(self):
        """Путь через файл - ошибка 'Not a directory'."""
        with self.assertRaises(VFSError) as ctx:
            self.vfs.lookup("root.txt/x", [])
        self.assertIn("Not a directory", str(ctx.exception))

    def test_total_size(self):
        """Размер каталога - сумма размеров файлов."""
        self.assertEqual(self.vfs.root.total_size(), 12 + 14 + 2)

    def test_missing_archive(self):
        """Отсутствующий архив - VFSError."""
        with self.assertRaises(VFSError):
            VFS("/no/such/archive.zip")

    def test_not_a_zip(self):
        """Файл, не являющийся ZIP, - VFSError."""
        path = make_zip({})
        with open(path, "wb") as handle:
            handle.write(b"not a zip")
        self.addCleanup(os.remove, path)
        with self.assertRaises(VFSError):
            VFS(path)

"""Виртуальная файловая система в памяти; источник - ZIP-архив."""
import io
import zipfile

ROOT = "/"
PARENT = ".."
SKIPPED_PARTS = ("", ".")
NOT_FOUND = "No such file or directory"
NOT_A_DIR = "Not a directory"
IS_A_DIR = "Is a directory"


class VFSError(Exception):
    """Ошибка работы с виртуальной файловой системой."""


class Node:
    """Узел дерева: файл (с данными) или каталог (с потомками)."""

    def __init__(self, name, is_dir, data=b""):
        self.name = name
        self.is_dir = is_dir
        self.data = data
        self.children = {}

    def child_dir(self, name):
        """Возвращает подкаталог, создавая его при необходимости."""
        return self.children.setdefault(name, Node(name, True))

    def total_size(self):
        """Размер файла или суммарный размер всех файлов каталога."""
        if not self.is_dir:
            return len(self.data)
        return sum(child.total_size() for child in self.children.values())


class VFS:
    """Дерево каталогов, построенное из ZIP-архива целиком в памяти."""

    def __init__(self, zip_path):
        self.path = zip_path
        self.root = Node("", True)
        self._load(zip_path)

    def _load(self, zip_path):
        """Читает архив в память и строит дерево (на диск не пишет)."""
        try:
            with open(zip_path, "rb") as handle:
                raw = handle.read()
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                for info in archive.infolist():
                    self._add(info.filename, info.is_dir(),
                              archive.read(info))
        except FileNotFoundError:
            raise VFSError(f"файл VFS не найден: {zip_path}") from None
        except zipfile.BadZipFile:
            raise VFSError(f"не ZIP-архив: {zip_path}") from None
        except OSError as err:
            raise VFSError(f"не удалось прочитать VFS: {err}") from None

    def _add(self, name, is_dir, data):
        """Добавляет в дерево запись архива."""
        parts = [p for p in name.split(ROOT) if p not in SKIPPED_PARTS]
        if not parts:
            return
        node = self.root
        for part in parts[:-1]:
            node = node.child_dir(part)
        leaf = parts[-1]
        if leaf not in node.children:
            node.children[leaf] = Node(leaf, is_dir, b"" if is_dir else data)

    @staticmethod
    def split(path, cwd):
        """Нормализует путь относительно cwd в список компонентов."""
        parts = [] if path.startswith(ROOT) else list(cwd)
        for part in path.split(ROOT):
            if part in SKIPPED_PARTS:
                continue
            if part == PARENT:
                parts = parts[:-1]
            else:
                parts.append(part)
        return parts

    def walk(self, parts):
        """Находит узел по списку компонентов пути."""
        node = self.root
        for part in parts:
            if not node.is_dir:
                raise VFSError(NOT_A_DIR)
            if part not in node.children:
                raise VFSError(NOT_FOUND)
            node = node.children[part]
        return node

    def lookup(self, path, cwd):
        """Возвращает (узел, компоненты пути) для заданного пути."""
        parts = self.split(path, cwd)
        return self.walk(parts), parts

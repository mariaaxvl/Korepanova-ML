"""Создаёт тестовые ZIP-архивы VFS в каталоге tests/vfs."""
import os
import zipfile

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vfs")
BINARY = bytes([0, 1, 2, 255, 254, 128, 7])
BIG_FILE_SIZE = 3000

ARCHIVES = {
    "minimal": {"hello.txt": "Hello, VFS!\n"},
    "several": {
        "readme.txt": "Это README\n",
        "notes.txt": "заметка 1\nзаметка 2\n",
        "docs/": "",
        "docs/guide.txt": "Руководство\n",
        "image.bin": BINARY,
        "big.txt": "x" * BIG_FILE_SIZE,
    },
    "deep": {
        "root.txt": "корень\n",
        "a/a.txt": "уровень 1\n",
        "a/b/b.txt": "уровень 2\n",
        "a/b/c/c.txt": "уровень 3\n",
        "a/b/c/d/deep.txt": "уровень 4\n",
        "etc/config/app.conf": "key=value\n",
    },
}


def build(name, entries):
    """Записывает один архив из словаря {путь: содержимое}."""
    path = os.path.join(OUT_DIR, f"{name}.zip")
    with zipfile.ZipFile(path, "w") as archive:
        for entry, content in entries.items():
            archive.writestr(entry, content)


def main():
    """Создаёт все тестовые архивы."""
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, entries in ARCHIVES.items():
        build(name, entries)
    print(f"VFS-архивы созданы в {OUT_DIR}")


if __name__ == "__main__":
    main()

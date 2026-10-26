#!/usr/bin/env bash
# Этап 3: разные варианты VFS и обработка ошибок.
# Для запуска без окон: EMU_FLAGS=--headless ./tests/stage3.sh
cd "$(dirname "$0")/.." || exit 1
FLAGS="${EMU_FLAGS:-}"
EMU="python3 src/main.py $FLAGS"
python3 tests/make_vfs.py

emu_lines() {
    local archive="$1"
    shift
    $EMU --vfs "tests/vfs/$archive.zip" --script <(printf '%s\n' "$@")
}

echo "== minimal ==";  $EMU --vfs tests/vfs/minimal.zip \
    --script tests/data/vfs_minimal.txt
echo "== several ==";  $EMU --vfs tests/vfs/several.zip \
    --script tests/data/vfs_several.txt
echo "== deep ==";     $EMU --vfs tests/vfs/deep.zip \
    --script tests/data/vfs_deep.txt
echo "== все команды этапов 1-3 =="
$EMU --vfs tests/vfs/deep.zip --script tests/data/stage3_full.txt </dev/null
echo "== ошибка: cd в файл =="
emu_lines deep "cd root.txt" </dev/null
echo "== ошибка: ls отсутствующего пути =="
emu_lines deep "ls /no/such" </dev/null
echo "== ошибка: слишком много аргументов =="
emu_lines deep "cd a b" </dev/null
echo "== ошибка: VFS не найдена =="
echo exit | $EMU --vfs tests/vfs/missing.zip
echo "== ошибка: файл не является ZIP =="
echo exit | $EMU --vfs src/main.py

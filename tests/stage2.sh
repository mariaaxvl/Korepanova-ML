#!/usr/bin/env bash
# Этап 2: проверка параметров командной строки.
# Для запуска без окон: EMU_FLAGS=--headless ./tests/stage2.sh
cd "$(dirname "$0")/.." || exit 1
FLAGS="${EMU_FLAGS:-}"
EMU="python3 src/main.py $FLAGS"

echo "== 1. Без параметров =="
echo exit | $EMU
echo "== 2. Только --script =="
$EMU --script tests/data/stage1_demo.txt
echo "== 3. --script с комментариями =="
$EMU --script tests/data/stage2_demo.txt
echo "== 4. Остановка скрипта на ошибке =="
$EMU --script tests/data/stop_on_error.txt < /dev/null
echo "== 5. Только --vfs =="
echo exit | $EMU --vfs some/path/vfs.zip
echo "== 6. Оба параметра =="
$EMU --vfs some/path/vfs.zip --script tests/data/stage2_demo.txt
echo "== 7. Несуществующий скрипт =="
echo exit | $EMU --script no_such_script.txt

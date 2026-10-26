"""Выполнение стартовых скриптов эмулятора."""
from common import failure

COMMENT = "#"
FIRST_LINE = 1


def read_lines(path):
    """Читает строки скрипта из файла."""
    with open(path, encoding="utf-8") as handle:
        return handle.read().splitlines()


def is_skipped(line):
    """Пустые строки и строки-комментарии пропускаются."""
    stripped = line.strip()
    return not stripped or stripped.startswith(COMMENT)


def run_line(shell, line, write):
    """Показывает ввод, выполняет строку и показывает вывод."""
    write(shell.prompt() + line + "\n")
    result = shell.execute(line)
    if result.out:
        write(result.out + "\n")
    return result


def run_script(shell, path, write):
    """Выполняет скрипт, имитируя диалог; останавливается при ошибке.

    Возвращает Result последней выполненной команды (None, если не было).
    """
    try:
        lines = read_lines(path)
    except OSError as err:
        write(f"[script] не удалось открыть скрипт: {err}\n")
        return failure(str(err))
    last = None
    for number, line in enumerate(lines, FIRST_LINE):
        if is_skipped(line):
            continue
        last = run_line(shell, line, write)
        if last.exit:
            break
        if not last.ok:
            write(f"[script] остановлено: ошибка в строке {number}\n")
            break
    return last

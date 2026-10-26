"""Разбор строки команды с раскрытием переменных окружения."""
import os
import re

VAR_RE = re.compile(r"\$(\w+)|\$\{(\w+)\}")
BLANKS = " \t"
QUOTES = "'\""
ESCAPABLE = '"\\$'


class ParseError(Exception):
    """Строку команды невозможно разобрать."""


class Tokenizer:
    """Делит строку на слова: кавычки, экранирование, $VAR и ${VAR}."""

    def __init__(self, line):
        self.line = line
        self.pos = 0
        self.quote = None
        self.words = []
        self.current = ""
        self.started = False

    def run(self):
        """Возвращает список слов или выбрасывает ParseError."""
        while self.pos < len(self.line):
            char = self.line[self.pos]
            if self.quote:
                self._in_quotes(char)
            else:
                self._outside_quotes(char)
            self.pos += 1
        if self.quote:
            raise ParseError("незакрытая кавычка")
        self._flush()
        return self.words

    def _flush(self):
        """Завершает текущее слово, если оно начато."""
        if self.started:
            self.words.append(self.current)
        self.current = ""
        self.started = False

    def _peek(self):
        """Следующий символ строки или пустая строка."""
        return self.line[self.pos + 1:self.pos + 2]

    def _variable(self):
        """Значение переменной в позиции курсора ('$' при её отсутствии)."""
        match = VAR_RE.match(self.line, self.pos)
        if not match:
            return "$"
        self.pos = match.end() - 1
        return os.environ.get(match.group(1) or match.group(2), "")

    def _escaped(self):
        """Пропускает '\\' и возвращает экранированный символ."""
        self.pos += 1
        return self.line[self.pos]

    def _in_quotes(self, char):
        """Обрабатывает символ внутри кавычек."""
        if char == self.quote:
            self.quote = None
        elif self.quote == "'":
            self.current += char
        elif char == "\\" and self._peek() and self._peek() in ESCAPABLE:
            self.current += self._escaped()
        elif char == "$":
            self.current += self._variable()
        else:
            self.current += char

    def _outside_quotes(self, char):
        """Обрабатывает символ вне кавычек."""
        if char in BLANKS:
            self._flush()
            return
        if char in QUOTES:
            self.quote = char
            self.started = True
        elif char == "\\" and self._peek():
            self.current += self._escaped()
            self.started = True
        elif char == "$":
            value = self._variable()
            self.current += value
            self.started = self.started or bool(value)
        else:
            self.current += char
            self.started = True


def parse(line):
    """Разбирает строку на слова с раскрытием переменных окружения."""
    return Tokenizer(line).run()

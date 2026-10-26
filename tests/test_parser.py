"""Тесты парсера командной строки."""
import os
import unittest

from cmdparser import ParseError, parse


class ParseTest(unittest.TestCase):
    """Проверки разбора слов, кавычек и переменных окружения."""

    def setUp(self):
        os.environ["EMU_TEST"] = "value"
        os.environ.pop("EMU_UNSET", None)

    def test_split_by_blanks(self):
        """Слова разделяются пробелами."""
        self.assertEqual(parse("ls -l  /tmp"), ["ls", "-l", "/tmp"])

    def test_env_expansion(self):
        """Раскрываются $VAR и ${VAR}."""
        self.assertEqual(parse("echo $EMU_TEST ${EMU_TEST}x"),
                         ["echo", "value", "valuex"])

    def test_unset_variable_disappears(self):
        """Неопределённая переменная даёт пустую строку."""
        self.assertEqual(parse("a $EMU_UNSET b"), ["a", "b"])

    def test_single_quotes_keep_dollar(self):
        """В одинарных кавычках переменные не раскрываются."""
        self.assertEqual(parse("echo '$EMU_TEST x'"), ["echo", "$EMU_TEST x"])

    def test_double_quotes_expand(self):
        """В двойных кавычках переменные раскрываются."""
        self.assertEqual(parse('echo "a $EMU_TEST"'), ["echo", "a value"])

    def test_escape(self):
        """Обратная косая черта экранирует символ."""
        self.assertEqual(parse(r"echo a\ b \$EMU_TEST"),
                         ["echo", "a b", "$EMU_TEST"])

    def test_empty_argument(self):
        """Пустые кавычки дают пустой аргумент."""
        self.assertEqual(parse('a ""'), ["a", ""])

    def test_lone_dollar(self):
        """Одиночный $ остаётся символом."""
        self.assertEqual(parse("echo $"), ["echo", "$"])

    def test_unclosed_quote(self):
        """Незакрытая кавычка - ошибка разбора."""
        with self.assertRaises(ParseError):
            parse('echo "abc')

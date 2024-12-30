import abc
import re

import sqlparse
from sqlparse.sql import Values, Parenthesis
from sqlparse.tokens import DML

from caasm_tool.parsers.base import CaasmBaseFileParser


class SqlFileParser(CaasmBaseFileParser, abc.ABC):
    """
    SQL 文件解析
    """

    _re_flags = [
        (re.compile("[Nn][uU][Ll][Ll]\)"), "None)"),
        (re.compile("[Nn][uU][Ll][Ll],"), "None,"),
    ]
    _value_prefix = "("
    _insert_flag = "INSERT"

    def parse(self, file_content):
        yield from self._parse_sql(file_content)

    def _parse_sql(self, file_content):
        file_parse = sqlparse.parse(file_content.strip())
        for value in file_parse:
            detail = None
            tokens = value.tokens

            for token in tokens:
                if token.ttype is DML and token.value.upper() == self._insert_flag:
                    detail = value
                    break

            if not detail:
                continue

            for token in tokens:
                if isinstance(token, Values):
                    index = 1

                    while True:
                        value_define: Parenthesis = token.token_next(index)[1]
                        if not value_define:
                            break
                        index += 1
                        value = value_define.value
                        if not self._check_value(value):
                            continue

                        cleand_value = self._clean(value)
                        yield cleand_value

    @classmethod
    def _clean(cls, value):
        for _re_flag in cls._re_flags:
            value = _re_flag[0].sub(_re_flag[1], value)
        return eval(value)

    @classmethod
    def _check_value(cls, value):
        return True if value.startswith(cls._value_prefix) else False

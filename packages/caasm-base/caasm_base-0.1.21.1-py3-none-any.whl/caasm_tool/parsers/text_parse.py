import abc
import logging
from typing import Any


from caasm_tool.parsers.base import CaasmBaseFileParser

log = logging.getLogger()


class TEXTFileParser(CaasmBaseFileParser, abc.ABC):
    INVALID_ROW_INDEXES = []
    VALID_SHEET_INDEXES = []
    INVALID_SHEET_INDEXES = []

    def check_sheet_index(self, sheet_index):
        if self.VALID_SHEET_INDEXES and sheet_index not in self.VALID_SHEET_INDEXES:
            return False
        if self.INVALID_SHEET_INDEXES and sheet_index in self.INVALID_SHEET_INDEXES:
            return False
        return True

    def parse(self, file_content) -> Any:
        file_data = file_content.decode()
        data = file_data.split("\n")
        for row in data:
            try:
                yield self.convert_row(row)
            except Exception as e:
                log.error(f"{e}  convert row fail! row detail is {row}")

    def convert_row(self, row):
        raise NotImplementedError

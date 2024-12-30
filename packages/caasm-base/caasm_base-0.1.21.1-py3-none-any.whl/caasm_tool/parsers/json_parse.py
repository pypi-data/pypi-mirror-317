import abc
import json
import logging
from typing import Any


from caasm_tool.parsers.base import CaasmBaseFileParser

log = logging.getLogger()


class JsonFileParser(CaasmBaseFileParser, abc.ABC):
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
        json_data = None
        try:
            json_data = json.loads(file_content)
        except Exception as e:
            log.error(f"{e} the file isn't a json file! ")
        if json_data and isinstance(json_data, dict):
            json_data = [json_data]
        if json_data and isinstance(json_data, list):
            for row_index in range(len(json_data)):
                row = json_data[row_index]
                if not isinstance(row, dict):
                    log.error(f"row data type fail! right data type is dict but it is {type(row)}")
                    continue
                try:
                    yield self.convert_row(row)
                except Exception as e:
                    log.error(f"{e}  convert row fail! row detail is {row}")

    def convert_row(self, row):
        raise NotImplementedError

import abc
import logging
import traceback
from typing import Any

import xlrd

from caasm_tool.parsers.base import CaasmBaseFileParser, ConvertMixIn

log = logging.getLogger()


class XlsxFileParser(CaasmBaseFileParser, abc.ABC):
    INVALID_ROW_INDEXES = []
    VALID_SHEET_INDEXES = []
    INVALID_SHEET_INDEXES = []

    def check_sheet_index(self, sheet_index):
        if self.VALID_SHEET_INDEXES and sheet_index not in self.VALID_SHEET_INDEXES:
            return False
        if self.INVALID_SHEET_INDEXES and sheet_index in self.INVALID_SHEET_INDEXES:
            return False
        return True

    def open_excel(self, file_content):
        return xlrd.open_workbook(file_contents=file_content)

    def parse(self, file_content) -> Any:
        workbook = self.open_excel(file_content)
        sheet_names = workbook.sheet_names()
        for sheet in workbook.sheets():
            sheet_name = sheet.name
            sheet_index = sheet_names.index(sheet_name)
            if not self.check_sheet_index(sheet_index):
                continue
            for row_index in range(sheet.nrows):
                row = sheet.row_values(row_index)
                try:
                    ignore_res = self.ignore_row(row_index, row)
                except Exception as e:
                    log.error(f"ignore row_index({row_index}), row error({e}), detail is {traceback.format_exc()}")
                    continue
                else:
                    if ignore_res:
                        continue
                try:
                    yield self.convert_row(row)
                except Exception as e:
                    log.error(f"convert row error({e}), detail is ({traceback.format_exc()}), row detail is {row}")

    def ignore_row(self, row_index, row) -> bool:
        return row_index in self.INVALID_ROW_INDEXES

    def convert_row(self, row):
        raise NotImplementedError


class XlsxFileParserV1(XlsxFileParser, ConvertMixIn, abc.ABC):
    def convert_row(self, row):
        return self.execute_convert_row(row)

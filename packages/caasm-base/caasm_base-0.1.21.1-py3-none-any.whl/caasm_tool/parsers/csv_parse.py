import abc
import csv
import logging

from caasm_tool.parsers.base import CaasmBaseFileParser, ConvertMixIn

log = logging.getLogger()


class CsvFileParser(CaasmBaseFileParser, abc.ABC):
    INVALID_ROW_INDEXES = []

    def __init__(self, *args, **kwargs):
        super(CsvFileParser, self).__init__(*args, **kwargs)
        self.use_fd = True

    def parse(self, file_fd):
        file_fd = self.clean_file_fd(file_fd)
        contents = csv.reader(file_fd)

        index = 0
        for row in contents:
            try:
                if index in self.INVALID_ROW_INDEXES:
                    continue
                yield self.convert_row(row)
            finally:
                index += 1

    def convert_row(self, row):
        raise NotImplementedError

    def clean_file_fd(self, file_fd):
        return file_fd


class CsvFileParserV1(CsvFileParser, ConvertMixIn, abc.ABC):
    def convert_row(self, row):
        return self.execute_convert_row(row)

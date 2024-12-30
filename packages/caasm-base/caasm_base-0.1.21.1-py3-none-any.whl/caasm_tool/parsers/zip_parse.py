import abc
import logging
import zipfile

from caasm_tool.parsers.base import CaasmBaseFileParser

log = logging.getLogger()


class ZipFileParser(CaasmBaseFileParser, abc.ABC):
    INVALID_NAMES = []

    def __init__(self, *args, **kwargs):
        super(ZipFileParser, self).__init__(use_fd=True)

    def parse(self, file_content):
        z_file = zipfile.ZipFile(file_content, "r")

        for z_name in z_file.namelist():
            if not self.judging_name_legitimacy(z_name):
                continue
            try:
                f_info = z_file.read(z_name)
                yield self.convert(z_name, f_info)
            except Exception as e:
                log.error(f"read {z_name}  or convert {z_name} fail! please check it!")
        z_file.close()

    def convert(self, name, row):
        return row.decode()

    def judging_name_legitimacy(self, name):
        if name in self.INVALID_NAMES:
            return False
        return True

from __future__ import absolute_import

from cStringIO import StringIO
from openpyxl.worksheet import flatten
from openpyxl.reader.excel import load_workbook
from .xls import BaseXLSParser

class Parser(BaseXLSParser):
    def open_workbook(self):
        # Unfortunate memory-hogging hack to work around zipfile not being
        # able to open urllib streams directly.
        return load_workbook(StringIO(self.stream.read()))

    def get_sheet_by_index(self, workbook, index):
        return workbook.worksheets[index]

    def get_sheet_by_name(self, workbook, name):
        return workbook.get_sheet_by_name(name)

    def extract_data(self, worksheet):
        return flatten(worksheet.rows)

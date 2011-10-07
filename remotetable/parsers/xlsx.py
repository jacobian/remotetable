from cStringIO import StringIO
from openpyxl.worksheet import flatten
from openpyxl.reader.excel import load_workbook

class Parser(object):

    def __init__(self, stream, **options):
        self.stream = stream
        self.options = options

    def read(self):
        # Unfortunate memory-hogging hack to work around zipfile not being
        # able to open urllib streams directly.
        stream = StringIO(self.stream.read())
        workbook = load_workbook(stream)

        if 'worksheet' in self.options:
            worksheet = workbook.get_sheet_by_name(self.options['worksheet'])
        else:
            worksheet = workbook.worksheets[0]

        data = flatten(worksheet.rows)
        data = data[self.options.get('skip', 0):]

        headers = self.options.get('headers', True)
        if headers is True:
            headers, data = data[0], data[1:]
        if headers:
            return [dict(zip(headers, row)) for row in data]
        else:
            return data

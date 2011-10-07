import xlrd

class Parser(object):

    def __init__(self, stream, **options):
        self.stream = stream
        self.options = options

    def read(self):
        # Gross: xlrd can't read streams.
        workbook = xlrd.open_workbook(file_contents=self.stream.read())

        if 'sheet' in self.options:
            worksheet = workbook.sheet_by_name(self.options['sheet'])
        else:
            worksheet = workbook.sheet_by_index(0)

        data = [worksheet.row_values(i) for i in range(worksheet.nrows)]
        data = data[self.options.get('skip', 0):]

        headers = self.options.get('headers', True)
        if headers is True:
            headers, data = data[0], data[1:]
        if headers:
            return [dict(zip(headers, row)) for row in data]
        else:
            return data

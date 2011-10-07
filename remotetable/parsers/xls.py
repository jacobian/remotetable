import xlrd

class BaseXLSParser(object):
    def __init__(self, stream, **options):
        self.stream = stream
        self.options = options

    def read(self):
        workbook = self.open_workbook()
        worksheet = self.get_worksheet(workbook)

        data = self.extract_data(worksheet)
        data = data[self.options.get('skip', 0):]

        headers = self.options.get('headers', True)
        if headers is True:
            headers, data = data[0], data[1:]
        if headers:
            return [dict(zip(headers, row)) for row in data]
        else:
            return data

    def get_worksheet(self, workbook):
        sheet_name = self.options.get('sheet', 0)
        try:
            worksheet = self.get_sheet_by_index(workbook, int(sheet_name))
        except ValueError:
            worksheet = self.get_sheet_by_name(workbook, sheet_name)
        return worksheet

class Parser(BaseXLSParser):
    def open_workbook(self):
        # Gross: xlrd can't read streams.
        return xlrd.open_workbook(file_contents=self.stream.read())

    def get_sheet_by_index(self, workbook, index):
        return workbook.sheet_by_index(index)

    def get_sheet_by_name(self, workbook, name):
        return workbook.sheet_by_name(name)

    def extract_data(self, worksheet):
        return [worksheet.row_values(i) for i in range(worksheet.nrows)]

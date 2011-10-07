import lxml.html

class Parser(object):

    def __init__(self, stream, **options):
        self.stream = stream
        self.options = options

    def read(self):
        doc = lxml.html.parse(self.stream).getroot()

        # Find rows
        if 'row_xpath' in self.options:
            rows = doc.xpath(self.options['row_xpath'])
        elif 'row_css' in self.options:
            rows = doc.cssselect(self.options['row_css'])
        else:
            rows = doc.xpath('//tr')

        # Now find columns.
        data = []
        for row in rows:
            if 'column_xpath' in self.options:
                columns = row.xpath(self.options['column_xpath'])
            elif 'column_css' in self.options:
                columns = row.cssselect(self.options['column_css'])
            else:
                columns = row.xpath('td')

            data.append([col.text_content().strip() for col in columns])

        # Now that we have data we can process `skip` and `headers`
        data = data[self.options.get('skip', 0):]

        headers = self.options.get('headers', True)
        if headers is True:
            headers, data = data[0], data[1:]
        if headers:
            return [dict(zip(headers, row)) for row in data]
        else:
            return data

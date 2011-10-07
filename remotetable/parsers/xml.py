import lxml.etree
import lxml.cssselect

to_string = lxml.etree.XPath("string()")

class Parser(object):

    def __init__(self, stream, **options):
        self.xmlparser = options.get('xmlparser', lxml.etree.parse)
        self.stream = stream
        self.options = options

    def read(self):
        doc = self.xmlparser(self.stream).getroot()

        # Create Xpath/CSS selectors for rows and columns.
        if 'row_css' in self.options:
            row_sel = lxml.cssselect.CSSSelector(self.options['row_css'])
        else:
            row_sel = lxml.etree.XPath(self.options.get('row_xpath', '//tr'))

        if 'column_css' in self.options:
            col_sel = lxml.cssselect.CSSSelector(self.options['column_css'])
        else:
            col_sel = lxml.etree.XPath(self.options.get('column_xpath', 'td'))

        data = []
        for row in row_sel(doc):
            data.append([to_string(col).strip() for col in col_sel(row)])

        # Now that we have data we can process `skip` and `headers`
        data = data[self.options.get('skip', 0):]

        headers = self.options.get('headers', True)
        if headers is True:
            headers, data = data[0], data[1:]
        if headers:
            return [dict(zip(headers, row)) for row in data]
        else:
            return data

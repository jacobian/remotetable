import unittest2
import remotetable

class RemoteTableTests(unittest2.TestCase):
    def test_open_csv(self):
        t = remotetable.open('http://www.ntsb.gov/data/datafiles/table2.csv', skip=4)
        self.assertEqual(t[0]['Year'], '1983')

    def test_open_xslx(self):
        t = remotetable.open('http://www.customerreferenceprogram.org/uploads/CRP_RFP_template.xlsx')
        self.assertEqual(
            t[2]["Requirements"],
            "Web Deployment"
        )

    def test_google_doc(self):
        t = remotetable.open('http://spreadsheets.google.com/pub?key=tObVAGyqOkCBtGid0tJUZrw')
        self.assertEqual(t[5]['name'], "Ian Hough")

    def test_csv_custom_headers(self):
        t = remotetable.open('http://spreadsheets.google.com/pub?key=tObVAGyqOkCBtGid0tJUZrw',
                             headers=['col1', 'col2', 'col3'])
        self.assertEqual(t[0]['col2'], 'name')
        self.assertEqual(t[1]['col2'], 'Seamus Abshere')

    def test_select_callback(self):
        t = remotetable.open(
            url = 'http://spreadsheets.google.com/pub?key=tObVAGyqOkCBtGid0tJUZrw',
            select = lambda row: row["name"] == "Seamus Abshere"
        )
        assert all(row["name"] == "Seamus Abshere" for row in t)

    def test_html_xpath(self):
        t = remotetable.open(
            url = 'http://police.lawrenceks.org/sites/default/files/files/stats/2011UCR.htm',
            row_xpath = '//table//table/tr',
            column_xpath = 'td|th',
            select = lambda row: bool(row['UCR Classification'])
        )
        self.assertEqual(t[0]['UCR Classification'], '100 - Kidnapping / Abduction')

    def test_html_css(self):
        t = remotetable.open(
            url = 'http://police.lawrenceks.org/sites/default/files/files/stats/2011UCR.htm',
            row_css = 'table table tr',
            column_css = 'td, th',
            select = lambda row: bool(row['UCR Classification'])
        )
        self.assertEqual(t[0]['UCR Classification'], '100 - Kidnapping / Abduction')

    def test_xml_xpath(self):
        # FIXME: it would be *great* if we could translate field@name into a dicts.
        t = remotetable.open('http://data.brighterplanet.com/airports.xml',
            row_xpath = '//row',
            column_xpath = 'field',
            headers = False
        )
        self.assertEqual(t[0][1], "Jefferson County International")

    def test_xml_css(self):
        t = remotetable.open('http://data.brighterplanet.com/airports.xml',
            row_css = 'row',
            column_css = 'field',
            headers = False
        )
        self.assertEqual(t[0][1], "Jefferson County International")

    # This short URL for the next couple tests points to the Lawrence PD crime
    # remote from the test_html_* methods above.

    def test_failed_parser_guessing(self):
        with self.assertRaises(ValueError) as cm:
            remotetable.open('http://bit.ly/qhMkBl')
        self.assertEqual(str(cm.exception), "Can't guess a parser for URL 'http://bit.ly/qhMkBl'")

    def test_named_parser(self):
        t = remotetable.open('http://bit.ly/qhMkBl',
            parser = 'html',
            row_css = 'table table tr',
            column_css = 'td, th',
            select = lambda row: bool(row['UCR Classification'])
        )
        self.assertEqual(t[0]['UCR Classification'], '100 - Kidnapping / Abduction')

    def test_invalid_named_parser(self):
        with self.assertRaises(ValueError) as cm:
            remotetable.open('http://bit.ly/qhMkBl', parser='flahflarg')
        self.assertEqual(
            str(cm.exception),
            "Can't find or load a parser named 'flahflarg': No module named flahflarg"
        )

    def test_xls(self):
        t = remotetable.open('http://cloud.github.com/downloads/seamusabshere/remote_table/remote_table_row_hash_test.alternate_order.xls')
        self.assertEqual(t[0]['header2'], 'value2')

    def test_open_csv_inside_zipfile(self):
        t = remotetable.open('http://www.epa.gov/climatechange/emissions/downloads10/2010-Inventory-Annex-Tables.zip',
            filename = 'Annex Tables/Annex 3/Table A-93.csv',
            skip = 1,
            select = lambda row: row['Vehicle Age'].strip().isdigit()
        )
        self.assertEqual(t[0]['LDGV'], '9.09%')

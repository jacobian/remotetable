import remotetable
from nose.tools import assert_equal

def test_open_csv():
    t = remotetable.open('http://www.ntsb.gov/data/datafiles/table2.csv', skip=4)
    assert_equal(t[0]['Year'], '1983')

def test_open_xslx():
    t = remotetable.open('http://www.customerreferenceprogram.org/uploads/CRP_RFP_template.xlsx')
    assert_equal(
        t[2]["Requirements"],
        "Web Deployment"
    )

def test_google_doc():
    t = remotetable.open('http://spreadsheets.google.com/pub?key=tObVAGyqOkCBtGid0tJUZrw')
    assert_equal(t[5]['name'], "Ian Hough")

def test_csv_custom_headers():
    t = remotetable.open('http://spreadsheets.google.com/pub?key=tObVAGyqOkCBtGid0tJUZrw',
                         headers=['col1', 'col2', 'col3'])
    assert_equal(t[0]['col2'], 'name')
    assert_equal(t[1]['col2'], 'Seamus Abshere')

def test_select_callback():
    t = remotetable.open(
        url = 'http://spreadsheets.google.com/pub?key=tObVAGyqOkCBtGid0tJUZrw',
        select = lambda row: row["name"] == "Seamus Abshere"
    )
    assert all(row["name"] == "Seamus Abshere" for row in t)

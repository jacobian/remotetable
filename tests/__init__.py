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

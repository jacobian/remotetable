import remotetable
from nose.tools import assert_equal

def test_open_csv():
    t = remotetable.open('http://www.ntsb.gov/data/datafiles/table2.csv', skip=5)
    assert_equal(
        t[0],
        ['1983', '4', '2', '9', '8', '7.299', '0.548', '0.274', '1.233', '1.096']
    )

def test_open_xslx():
    t = remotetable.open('http://www.customerreferenceprogram.org/uploads/CRP_RFP_template.xlsx', headers=True)
    assert_equal(
        t[2]["Requirements"],
        "Web Deployment"
    )

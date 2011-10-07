from __future__ import absolute_import

import cgi
import requests
import urlparse
import urllib
from . import parsers

def open(url, **kwargs):
    """
    Open a remote table.
    """
    # Possibly transform the URL.
    url = apply_transforms(url)

    # Figure out which parser to use.
    parser = kwargs.pop('parser', None)
    if callable(parser):
        pass
    elif parser is None:
        parser = parsers.guess_parser(url)
    else:
        parser = parsers.get_parser(parser)

    # Grab the data
    # FIXME: request params.
    # FIXME: response._resp is the only way to get a file-like obj!?
    # FIXME: option to use iterators
    response = requests.get(url)
    return parser(response._resp, **kwargs).read()

def apply_transforms(url):
    """
    Apply special-case transforms to the URL.
    """
    parsed = urlparse.urlparse(url)

    # Google spreadsheets: force CSV download.
    if parsed.netloc == 'spreadsheets.google.com':
        query = dict(cgi.parse_qsl(parsed.query))
        query['output'] = 'csv'
        parsed = parsed._replace(query=urllib.urlencode(query))

    return urlparse.urlunparse(parsed)

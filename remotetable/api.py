from __future__ import absolute_import

import requests
from . import parsers

def open(url, **kwargs):
    """
    Open a remote table.
    """
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

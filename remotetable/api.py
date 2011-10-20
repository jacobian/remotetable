from __future__ import absolute_import

import cgi
import requests
import urlparse
import urllib
import inspect
import itertools
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

    # Pull all the kwargs that might apply to the request out of kwargs so that
    # we can pass them onto `requests.request()`. To avoid clashes with parser
    # kwargs these are named `request_*` in the kwargs to open(). That is,
    # `request_method` translates to the `method` argument to
    # `requests.request()`.
    #
    # We'll pop the kwargs out of the dict here so that the remaining kwargs can
    # be passed safely to the parser.
    request_kwargs = {}
    for k in inspect.getargspec(requests.request).args:
        if ('request_%s' % k) in kwargs:
            request_kwargs[k] = kwargs.pop('request_%s' % k)

    # The two requirement arguments to request.
    request_kwargs['url'] = url
    request_kwargs.setdefault('method', 'get')

    # A couple of other defaults that more closely match my expectations.
    request_kwargs.setdefault('allow_redirects', True)

    # Save `select` and `omit` arguments for later.
    select_func = kwargs.pop('select', None)
    omit_func = kwargs.pop('omit', None)

    # Grab the data.
    with requests.settings(accept_gzip=False):
        response = requests.request(**request_kwargs)
    results = parser(response.raw, **kwargs).read()

    # Process select/omit.
    if select_func:
        results = itertools.ifilter(select_func, results)
    if omit_func:
        results = itertools.ifilter(lambda item: not omit_func(item), results)
    return list(results)

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

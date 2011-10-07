import os
import urlparse
import importlib

def guess_parser(url):
    """
    Guess a parser based on the URL.
    """
    parsed = urlparse.urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lstrip('.')
    if ext == 'csv' or parsed.netloc == 'spreadsheets.google.com':
        return get_parser('csv')
    elif ext in ("xlsx", "excelx"):
        return get_parser('xlsx')
    elif ext in ('htm', 'html'):
        return get_parser('html')
    else:
        raise ValueError("Can't guess a parser for URL %r" % url)

def get_parser(name):
    """
    Look up and load a parser named `name`.
    """
    try:
        return importlib.import_module('.%s' % name, package=__name__).Parser
    except ImportError, e:
        raise ValueError("Can't find or load a parser named %r: %s" % (name, e))

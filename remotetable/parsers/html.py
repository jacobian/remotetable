from __future__ import absolute_import

import lxml.html
from . import xml

class Parser(xml.Parser):
    def __init__(self, stream, **options):
        super(Parser, self).__init__(stream, xmlparser=lxml.html.parse, **options)

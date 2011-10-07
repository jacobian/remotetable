from __future__ import absolute_import
import csv

class Parser(object):

    def __init__(self, stream, **options):
        self.stream = iter(stream)
        self.options = options

    def read(self):
        for i in range(self.options.get('skip', 0)):
            self.stream.next()

        reader = csv.reader(self.stream)
        headers = self.options.get('headers', True)
        if headers is True:
            headers = reader.next()
        if headers:
            reader = csv.DictReader(self.stream, fieldnames=headers)

        return list(reader)

remotetable
===========

Open remote tables, be they CSV, XLSX, HTML, XML, ...

Heavily inspired by Seamus Abshere's remote_table_ gem: a lot of the APIs and
even some of the tests are cribbed from there. Thanks, Seamus.

.. _remote_table: https://github.com/seamusabshere/remote_table

**WARNING**: This is *very* rough right now -- more a proof of concept than a
working project. But I'd like to see it grow, so please feel free to submit
pull requests!

Usage
-----

Full docs will come before I consider this done, but they don't exist yet.
For a taste, though::

    >>> t = remotetable.open('https://raw.github.com/gist/1111189/unruly_passengers.txt', parser='csv')
    >>> for row in t:
    ...     print row['Year'], row['Total']
    ...
    1995 146
    1996 184
    1997 235
    1998 200
    1999 226
    2000 251
    2001 299
    2002 273
    2003 281
    2004 304
    2005 203
    2006 136
    2007 150
    2008 123
    2009 135
    2010 121

    >>> t = remotetable.open(
    ...     url = 'http://police.lawrenceks.org/sites/default/files/files/stats/2011UCR.htm',
    ...     row_xpath = '//table//table/tr',
    ...     column_xpath = 'td|th',
    ...     select = lambda row: row['UCR Classification'] != ''
    ... )
    >>> sum(int(row['Total']) for row in t)
    5167

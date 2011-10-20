import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "remotetable",
    version = "0.1",
    description = "FIXME",
    long_description = read('README.rst'),
    url = 'http://remotetable.rtfd.org/',
    license = 'BSD',
    author = 'Jacob Kaplan-Moss',
    author_email = 'jacob@jacobian.org',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        "Development Status :: 3 - Alpha"
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = ["requests >= 0.6.6, < 0.7", "unipath"],
    tests_require = ["nose", "mock", "unittest2"],
    test_suite = "nose.collector",
)

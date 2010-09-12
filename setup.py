#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open


with open('README.rst', encoding='utf-8') as stream:
    long_description = stream.read()


setup(
    name='pastemacs',
    version='0.2.1',
    url='http://pypi.python.org/pypi/pastemacs/',
    author='Sebastian Wiesner',
    author_email='lunaryorn@googlemail.com',
    description='Lodgeit integration for emacs',
    long_description=long_description,
    license='GPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Environment :: Plugins',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Topic :: Text Editors :: Emacs'
        ],
    py_modules=['pastemacs'],
    install_requires=['lodgeitlib>=0.5'],
    )

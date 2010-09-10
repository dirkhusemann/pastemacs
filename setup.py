#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
pastemacs
---------

Provides lodgeit integration for emacs through pymacs.

To use it, add the following line to your ``~/.emacs``::

    (pymacs-load "pastemacs" "paste-")

To enable the menu, add the following line after the above::

    (paste-menu)
"""


from setuptools import setup


setup(
    name='pastemacs',
    version='0.1.2',
    url='http://pypi.python.org/pypi/pastemacs/',
    author='Sebastian Wiesner',
    author_email='lunaryorn@googlemail.com',
    description='Lodgeit integration for emacs',
    long_description=__doc__,
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
    install_requires=['lodgeitlib'],
    )

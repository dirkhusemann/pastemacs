#########
pastemacs
#########

http://pypi.python.org/pypi/pastemacs/

**pastemacs** allows to create and retrieve pastes from
http://paste.pocoo.org directly from Emacs_.  It is available under the
terms of the `GNU GPL 2`_ (see ``COPYING``).

.. _Emacs: http://www.gnu.org/software/emacs/emacs.html
.. _`GNU GPL 2`: http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt


Installation
============

You will need at least Python 2.6 (earlier versions may work, but are not
tested, Python 3 is *not* supported).  pastemacs itself is available in the
`Python package index`_ and can simply be installed using ``pip`` or
``easy_install``::

   pip install pastemacs
   # or
   easy_install pastemacs

This installs pastemacs and its dependency lodgeitlib_. Alternatively you
can just clone the Git_ repository and install manually::

   git clone git://github.com/lunaryorn/pastemacs.git
   cd pastemacs
   python setup.py install

In this case you need to manually install lodgeitlib_ before.

Moreover you need a working installation of Pymacs_.  This should be
available in the package repositories of your distribution.  If not, or if
you are on Windows, refer to the `Pymacs documentation`_ for installation
instructions.

.. _`Python package index`: http://pypi.python.org/pypi/pastemacs
.. _lodgeitlib: http://packages.python.org/lodgeitlib
.. _git: http://git-scm.com/
.. _pymacs: http://pymacs.progiciels-bpi.ca/
.. _`Pymacs documentation`: http://pymacs.progiciels-bpi.ca/pymacs.html


Usage
=====

In order to use pastemacs, just add the following two lines to your Emacs
configuration file::

   (pymacs-load "pastemacs" "paste-")
   (paste-menu)

The second line only enables the GUI menu to create and fetch pastes, and is
not strictly required.  Now all pastemacs commands are available.  You can
use them either through the menu (if enabled) or by executing them directly
using ``M-x``.  pastemacs does not register any shortcuts for its commands,
so if you want some, you have to register them for yourself (e.g. by using
``global-set-key``).

Take a look at the configuration_, the author of pastemacs uses, if you want
to see an example.

.. _configuration: https://github.com/lunaryorn/dotemacsd/blob/master/site-start.d/50pasting.el


Creating pastes
---------------

The command ``paste-new`` creates a new paste.  If transient mark mode is
enabled and the mark is active, it pastes the contents of the region,
otherwise it pastes the complete buffer contents.

The command prompts for a (programming) language, in which the paste is
written.  This is used for syntax highlighting in the pastebin web
interface.  The list of available languages is fetched from the server, once
you create your first paste, and available as completion list for the
language prompt.  You cannot enter a language, which isn't supported, so if
the language isn't available, choose the default "text".

.. note::

   pastemacs tries to derive a language from the name of the major mode and
   sets it as default while prompting for a language, but this isn't really
   clever, and will often fail.  So be sure to check the language, if you
   want syntax highlighting for your paste.

By default the URL of the new paste will only be displayed in the minibuffer
and in the ``*Messages*`` buffer.  To automatically put the url into the
kill ring, set the variable ``paste-kill-url`` to a non-nil value in your
emacs configuration.

Alternatively new pastes can automatically be opened in your favourite web
browser by setting ``paste-show-in-browser`` to a non-nil value in your
emacs configuration.

Both variables are available in customization.


Retrieving pastes
-----------------

To retrieve a paste, use ``paste-fetch``.  It fetches a paste and inserts
its contents at the point in the current buffer.

The commands prompts for a paste to retrieve.  You can either enter a
complete paste URL, or just a paste ID.  Empty input is also allowed, and
stands for the last paste.


Configuration
-------------

Simply visit the customization group ``pastebin``.


Issues, Feedback and Development
================================

All development happens on Github_.

Please report issues, proposals or enhancements to the `issue tracker`_.
Please provide as much information as possible when reporting issues.

Feel free to clone the repository, add you own modifications and send a pull
requests.  Enhancements and new features are always appreciated :)

.. _github: https://github.com/lunaryorn/pastemacs
.. _`issue tracker`: https://github.com/lunaryorn/pastemacs/issues

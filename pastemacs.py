# -*- coding: utf-8 -*-
# allows pasting the current buffer on paste.pocoo.org
# Copyright (c) 2007-2010 Sebastian Wiesner <lunaryorn@googlemail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


"""
    pastemacs
    =========

    This pymacs module provides a handful of function for convenient access
    to the pastebin at `http://paste.pocoo.org`.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from Pymacs import lisp

from lodgeitlib import lodgeit


# necessary references
lisp.require(lisp['easymenu'])
lisp.require(lisp['browse-url'])


# customisation group
lisp("""
(defgroup pastebin nil
  "Access to the pastebin on paste.pocoo.org"
  :group 'convenience)

(defcustom paste-kill-url nil
  "*If non-nil, put the url of a new paste into kill ring"
  :group 'pastebin
  :type 'boolean)

(defcustom paste-show-in-browser nil
  "*If non-nil, invoke the browser with the paste url after
  pasting a new snippet"
  :group 'pastebin
  :type 'boolean)
""")


def languages():
    """Returns a list of supported languages."""
    if not lodgeit.has_languages:
        lisp.message('Fetching list of supported languages from server')
    return lodgeit.languages.keys()


def read_language():
    """Reads a paste language from minibuffer. Provides completion based on
    the list ov available languages"""
    # guess language from major mode
    major_mode = lisp.major_mode.value().text
    def_language = major_mode[:-5]
    if def_language not in languages():
        def_language = 'text'
    msg = 'Language of paste snippet ({0}): '.format(def_language)
    language = (lisp.completing_read(msg, languages()).strip()
                or def_language)
    return language


def read_paste_id():
    """
    Read and return a paste id from the minibuffer.

    A paste id is either an empty string, which stands for the last paste,
    or a number.
    """
    while True:
        paste_id = lisp.read_no_blanks_input(
            'A paste id [default: last paste]: ')
        if not paste_id or paste_id.isdigit():
            return paste_id
        else:
            lisp.error('Please enter a number or '
                       'leave the minibuffer empty')


def fetch(paste_id=None):
    """
    Fetch a paste and insert its content at point.

    If ``paste_id`` is given, fetch the paste with the given id, otherwise
    fetch the last paste.

    When called interactively, prompt for a paste id.  Empty input stands
    for the last paste, and numeric input for the paste with the given id.
    """
    if paste_id:
        paste = lodgeit.get_paste_by_id(paste_id)
    else:
        paste = lodgeit.get_last_paste()
    if paste:
        lisp.insert(paste.code)
    else:
        lisp.error('There is no paste with id {0}'.format(paste_id))
fetch.interaction = lambda: [read_paste_id()]


def new(language, region_start=None, region_end=None):
    """
    Create a new paste.  Use the given (programming) ``language`` for server
    side highlighting.

    If ``region_start`` and ``region_end`` are given, create a paste with
    the contents of this region.

    When called interactively with transient mark mode enabled and an active
    mark, create a paste with the contents of the region.  Otherwise create
    a paste with the contents of the whole buffer.
    """
    mark_active = lisp.mark_active.value()
    transient_mark_mode = lisp.transient_mark_mode.value()
    if lisp.interactive and  transient_mark_mode and mark_active:
        # use a region, if we have one
        region_start = lisp.region_beginning()
        region_end = lisp.region_end()
    elif region_start:
        # otherwise use the given arguments
        region_start = min(region_start, region_end)
        region_end = man(region_start, region_end)
    else:
        # as last resort, paste the whole buffer
        region_start = lisp.point_min_marker()
        region_end = lisp.point_max_marker()

    code = unicode(lisp.buffer_substring(region_start, region_end))
    filename = lisp.buffer_file_name()

    lisp.message('Transferring paste to server...')
    id = lodgeit.new_paste(code, language, filename=filename)
    paste = lodgeit.get_paste_by_id(id)
    lisp.message(
        'New paste with id {0.id} created. Refer to {0.url}'.format(paste))
    if lisp.paste_kill_url.value():
        lisp.kill_new(paste.url)
    if lisp.paste_show_in_browser.value():
        lisp.browse_url(paste.url)
new.interaction = lambda: [read_language()]


def menu():
    """Creates a global menu to access the pastebin functionality"""
    lisp.easy_menu_add_item(
        lisp.current_global_map(),
        ['menu-bar'],
        ['Pastebin',
         ('Fetch...', lisp.paste_fetch),
         '---',
         ('New...', lisp.paste_new),
         ])
menu.interaction = ''

# -*- coding: utf-8 -*-
# allows pasting the current buffer on paste.pocoo.org

# Copyright (c) 2007 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


from Pymacs import lisp
from xmlrpclib import ServerProxy


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
     

class UnsupportedLanguageException(Exception):
    def __init__(self, language):
        self.language = language

    def __str__(self):
        return 'Unsupported language: %s' % self.language


class Pastes(object):
    """Represents the pocoo paste bin"""
    def __init__(self):
        self._languages = None
        self._proxy = ServerProxy('http://paste.pocoo.org/xmlrpc',
                                  allow_none=True)

    @property
    def languages(self):
        """Returns a list of supported languages"""
        if not self._languages:
            lisp.message('Fetching list of supported languages from server')
            langs = self._proxy.pastes.getLanguages()
            self._languages = list(zip(*langs)[0])
        return self._languages

    def new_paste(self, code, language, filename):
        """Creates a new paste from `code` with `language`"""
        if not language:
            language = None
            lisp.message('No language given. The server will guess the '
                         'language from buffer filename')
        if language not in self.languages:
            raise UnsupportedLanguageException()

        lisp.message('Transferring paste to server...')
        paste_id = self._proxy.pastes.newPaste(language, code, None,
                                               filename)
        url = 'http://paste.pocoo.org/show/%s' % paste_id
        
        lisp.message('New paste with id %s created. Refer to %s',
                     paste_id, url)
        if lisp.paste_kill_url.value():
            lisp.kill_new(url)
        ## if lisp.paste_show_in_browser.value():
        ##     lisp.message('Would invoke http://paste.pocoo.org/show/%s in '
        ##                  'webbrowser', paste_id)
        return paste_id

    def get_paste(self, paste_id):
        """Returns the paste with `paste_id`"""
        return self._proxy.pastes.getPaste(paste_id)

    def get_last_paste(self):
        """Returns the last paste"""
        return self._proxy.pastes.getLast()


# global paste bin object
paste_bin = Pastes()


## NON-INTERACTIVE FUNCTIONS
# interactive argument completion
def read_language():
    """Reads a language from minibuffer with completion"""
    # guess language from major mode
    major_mode = lisp.major_mode.value().text
    def_language = major_mode[:-5]
    if def_language not in paste_bin.languages:
        def_language = 'text'
    msg = 'Language of paste snippet (%s): ' % def_language
    language = (lisp.completing_read(msg, paste_bin.languages).strip() or
                def_language)

    if language not in paste_bin.languages:
        raise UnsupportedLanguageException(language)

    return language

def get_new_from_region_args():
    """Gets args for new_from_region"""
    lang = read_language()
    start, end = lisp.region_beginning(), lisp.region_end()
    return [start, end, lang]

def get_new_from_buffer_args():
    """Gets args for new_from_buffer"""
    buff = lisp.read_buffer('Buffer to paste: ',
                            lisp.current_buffer(), True)
    lang = read_language()
    return [buff, lang]


def new_buffer_from_paste(paste):
    """Creates a new buffer from `paste`"""
    lisp.switch_to_buffer('paste %(paste_id)s' % paste)
    lisp.erase_buffer()
    lisp.insert(paste['code'])
    # simple guessing of the buffer mode
    # XXX: is there a better way?
    mode = lisp['%(language)s-mode' % paste]
    mode()


## INTERACTIVE FUNCTIONS
# to fetch pastes
def fetch_by_id(paste_id):
    """Fetches paste with `paste_id` and inserts it into a new buffer"""
    paste = paste_bin.get_paste(paste_id)
    if paste:
        new_buffer_from_paste(paste)
    else:
        lisp.error('There is no paste with id %s', paste_id)
fetch_by_id.interaction = ('nThe paste id: ')

def insert_by_id(paste_id):
    """Fetches paste with `paste_id` and inserts it into current buffer"""
    paste = paste_bin.get_paste(paste_id)
    if paste:
        lisp.insert(paste['code'])
    else:
        lisp.error('There is no paste with id %s', paste_id)
insert_by_id.interaction = ('*nThe paste id: ')

def fetch_last():
    """Fetches last paste and inserts it into a new buffer"""
    paste = paste_bin.get_last_paste()
    new_buffer_from_paste(paste)
fetch_last.interaction = ''

def insert_last():
    """Inserts the last paste into current buffer"""
    paste = paste_bin.get_last_paste()
    lisp.insert(paste['code'])
insert_last.interaction = '*'


# to create new pastes
def new_from_region(start, end, language):
    """Pastes the current selection"""
    code = lisp.buffer_substring(start, end)
    filename = lisp.buffer_file_name()
    paste_bin.new_paste(code, language, filename)
new_from_region.interaction = get_new_from_region_args
        
def new_from_buffer(buffer, language):
    """Pastes the contents of buffer"""
    lisp.set_buffer(buffer)
    # XXX: this freezes emacs on larger buffers like one containing this file
    # code = lisp.buffer_string()
    # strangely enough this works, however
    code = lisp.buffer_substring(lisp.point_min(), lisp.point_max())
    filename = lisp.buffer_file_name()
    paste_bin.new_paste(code, language, filename)
new_from_buffer.interaction = get_new_from_buffer_args


def menu():
    lisp.easy_menu_add_item(
        lisp.current_global_map(),
        ['menu-bar'],
        ["Pastebin",
         ("Fetch last", lisp.paste_fetch_last),
         ("Insert last", lisp.paste_insert_last),
         ("Fetch by id", lisp.paste_fetch_by_id),
         ("Insert by id", lisp.paste_insert_by_id),
         "---",
         ("New from buffer", lisp.paste_new_from_buffer),
         ("New from region", lisp.paste_new_from_region)
         ])
menu.interaction = ''

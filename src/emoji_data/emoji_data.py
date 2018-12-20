# -*- coding: utf-8 -*-

from __future__ import absolute_import

import codecs
import os.path
import re

import six
from pkg_resources import Requirement, resource_stream
from six.moves.urllib.parse import urlparse
from six.moves.urllib.request import urlopen

from . import version

__all__ = ['EmojiData', 'EMOJI_DATA_URL']


EMOJI_DATA_URL = 'https://unicode.org/Public/emoji/11.0/emoji-data.txt'


PACKAGE = '.'.join(version.__name__.split('.')[:-1])


class _EmojiDataMeta(type):
    def __new__(cls, name, bases, atts):
        cls._data = {}
        return super(_EmojiDataMeta, cls).__new__(cls, name, bases, atts)

    def __setitem__(self, key, value):  # pylint: disable=C0203
        self._data[key] = value

    def __delitem__(self, key):  # pylint: disable=C0203
        del self._data[key]

    def __getitem__(self, key):  # pylint: disable=C0203
        return self._data[key]

    def __contains__(self, key):  # pylint: disable=C0203
        return key in self._data

    def __iter__(self):  # pylint: disable=bad-mcs-method-argument
        for k, v in self._data.items():  # pylint: disable=invalid-name
            yield k, v

    def __len__(self):  # pylint: disable=C0203
        return len(self._data)


class EmojiData(six.with_metaclass(_EmojiDataMeta)):

    _ignore_codes = [
        0x0023,  # 1.1  [1] (#️)       number sign
        0x002A,  # 1.1  [1] (*️)       asterisk
    ] + list(range(0x0030, 0x0039 + 1))  # 1.1 [10] (0️..9️)    digit zero..digit nine

    _regex_pattern = None

    def __init__(self, code, property_, comments):  # type (int, str, str) -> object
        self._code = code
        self._property = property_
        self._comments = comments
        if code < 0xffff:
            self._regex = r'\u{:04X}'.format(code)
        else:
            self._regex = r'\U{:08X}'.format(code)

    def __str__(self):
        return self.char

    def __repr__(self):
        return '<{} hex={} char={!r} property={!r} comments={!r}>'.format(
            self.__class__.__name__,
            self.hex,
            self.char,
            self.property_,
            self.comments
        )

    @classmethod
    def initial(cls, url=None, compile_regex_pattern=True):
        if url is None:
            paths = PACKAGE.split('.') + ['data', 'emoji-data.txt']
            resource_name = os.path.join(*paths)
            data_file = resource_stream(
                Requirement.parse(PACKAGE), resource_name)
        else:
            parsed_url = urlparse(url)
            if parsed_url.scheme:
                data_file = urlopen(url)
            else:
                data_file = codecs.open(url, encoding='UTF-8')
        for line in data_file:
            if isinstance(line, bytes):
                line = codecs.decode(line, 'UTF-8')
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            if line.startswith(';'):
                continue

            pos = line.find(';')
            codepoints = [int(s, 16) for s in line[:pos].split('..')]
            code_range = range(codepoints[0], codepoints[-1]+1)
            line = line[pos+1:]

            pos = line.find('#')
            if pos >= 0:
                property_ = line[:pos].strip()
                line = line[pos+1:]
                comments = line.strip()
            else:
                property_ = None
                comments = None

            for code in code_range:
                if code not in cls._ignore_codes:
                    cls[code] = cls(code, property_, comments)

        if compile_regex_pattern:
            cls.compile_regex_pattern()

    @property
    def code(self):
        return self._code

    @property
    def property_(self):
        return self._property

    @property
    def comments(self):
        return self._comments

    @property
    def regex(self):
        return self._regex

    @property
    def hex(self):
        return hex(self._code)

    @property
    def char(self):
        return six.unichr(self._code)

    @classmethod
    def from_int(cls, val):
        return cls[val]

    @classmethod
    def from_char(cls, val):
        return cls[ord(val)]

    @classmethod
    def from_hex(cls, val):
        return cls[int(val, 16)]

    @classmethod
    def compile_regex_pattern(cls):
        pat = r'[{}]+'.format(r'|'.join(m.regex for _, m in cls))
        cls._regex_pattern = re.compile(pat)
        return cls._regex_pattern

    @classmethod
    def get_regex_pattern(cls):
        return cls._regex_pattern

# -*- coding: utf-8 -*-

from __future__ import absolute_import

import codecs
import os.path
import re

import six
from six.moves.urllib.parse import urlparse
from six.moves.urllib.request import urlopen

from pkg_resources import Requirement, resource_stream

from . import version

__all__ = ['EMOJI_DATA_URL', 'EmojiData', 'EmojiDataFileFormatError']


EMOJI_DATA_URL = 'https://unicode.org/Public/emoji/11.0/emoji-data.txt'
PACKAGE = '.'.join(version.__name__.split('.')[:-1])
ENCODING = 'utf-8'


class EmojiDataFileFormatError(Exception):
    pass


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
    """A Class stores and represents Emoji Characters
    """

    _ignore_codes = [
        0x0023,  # 1.1  [1] (#️)       number sign
        0x002A,  # 1.1  [1] (*️)       asterisk
    ] + list(range(0x0030, 0x0039 + 1))  # 1.1 [10] (0️..9️)    digit zero..digit nine

    _regex_text = None
    _regex_pattern = None

    def __init__(self, code, property_, comments):  # type: (int,str,str)->EmojiData
        """
        Parameters
        ----------
        code : int
            Interger value of the Emoji Unicode.
        property_ : str
            property of the Emoji.
        comments: str
            comments of the Emoji.
        """

        self._code = code
        self._property = property_
        self._comments = comments
        if code > 0xffff:
            self._regex = r'\U{:08X}'.format(code)
        else:
            self._regex = r'\u{:04X}'.format(code)

    def __str__(self):
        return self.char

    def __repr__(self):
        return '<{} hex={} char={!r} property={!r}>'.format(
            type(self).__name__,
            self.hex,
            self.char,
            self.property_
        )

    @classmethod
    def initial(cls, url=None, compile_regex_pattern=True):  # type: (str,bool)->None
        """Initial from a Emoji data file

        .. Important::
            **MUST** be called before other methods

        .. Tip::
            Currently, the default emoji data file inside the package was downloaded from <https://unicode.org/Public/emoji/11.0/emoji-data.txt>

        Parameters
        ----------
        url : str

            * default: ``None`` - Using default emoji data file inside the package

            URL or File Path of Emoji data file

        compile_regex_pattern : bool

            * default: ``True``

            Whether to compile a RegEx with all Emoji when loaded

        Raises
        ------
        EmojiDataFileFormatError
            Invalid format for specified Emoji data file.
        """

        # pylint:disable=too-many-branches

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
                data_file = codecs.open(url, encoding=ENCODING)

        for line in data_file:
            if not line:
                continue
            if isinstance(line, bytes):
                line = codecs.decode(line, ENCODING)  # type: str
            line = line.strip()
            if not line:
                continue
            if line[0] in ('#', ';'):
                continue

            pos = line.find(';')
            if pos < 0:
                raise EmojiDataFileFormatError()
            codepoints = [int(s, 16) for s in line[:pos].split('..', 1)]
            code_range = range(codepoints[0], codepoints[-1]+1)

            line = line[pos+1:]

            pos = line.find('#')
            if pos >= 0:
                property_ = line[:pos].strip()
                comments = line[pos+1:].strip()
            else:
                property_ = line.strip()
                comments = None

            for code in code_range:
                if code not in cls._ignore_codes:
                    cls[code] = cls(code, property_, comments)

        if compile_regex_pattern:
            cls.compile_regex_pattern()

    @property
    def code(self):  # type: ()->int
        """
        Returns
        -------
        int
            Unicode integer value of the Emoji
        """

        return self._code

    @property
    def property_(self):  # type: ()->str
        """
        Returns
        -------
        str
            Property description text of the Emoji
        """

        return self._property

    @property
    def comments(self):  # type: ()->str
        """
        Returns
        -------
        str
            Comments of the Emoji
        """

        return self._comments

    @property
    def regex(self):
        """
        Returns
        -------
        str
            Regular express for the Emoji
        """

        return self._regex

    @property
    def hex(self):  # type: ()->str
        """
        Returns
        -------
        str
            Hex style text of the Emoji's Unicode
        """

        return hex(self._code)

    @property
    def char(self):  # type: ()->str
        """
        Returns
        -------
        str
            Emoji character
        """

        return six.unichr(self._code)

    @classmethod
    def from_int(cls, val):  # type: (int)->EmojiData
        """Return a :class:`EmojiData` object by Emoji Unicode's integer value

        Parameters
        ----------
        val : int
            Integer value of the Emoji's Unicode

        Returns
        -------
        EmojiData
            Object returned

        Raises
        ------
        KeyError
            When integer code not found
        """

        return cls[val]

    @classmethod
    def from_char(cls, val):  # type: (str)->EmojiData
        """Return a :class:`EmojiData` object by Emoji Unicode character

        Parameters
        ----------
        val : str
            Emoji character

        Returns
        -------
        EmojiData
            Object returned

        Raises
        ------
        KeyError
            When Charactor code not found
        """

        return cls[ord(val)]

    @classmethod
    def from_hex(cls, val):  # type: (str)->EmojiData
        """Return a :class:`EmojiData` object by Emoji Unicode's HEX text

        Parameters
        ----------
        val : str
            Emoji Unicode's HEX

        Returns
        -------
        EmojiData
            Object returned

        Raises
        ------
        KeyError
            When Charactor code not found
        """

        return cls[int(val, 16)]

    @classmethod
    def compile_regex_pattern(cls):
        """compile then return a RegEx pattern object with all Emoji.
        """

        cls._regex_text = r'[{}]+'.format(r'|'.join(m.regex for _, m in cls))
        cls._regex_pattern = re.compile(cls._regex_text)
        return cls._regex_pattern

    @classmethod
    def get_regex_text(cls):  # type: ()->str
        """Regular express text with all Emoji
        """

        return cls._regex_text

    @classmethod
    def get_regex_pattern(cls):
        """Return a RegEx pattern object with all Emoji
        """

        return cls._regex_pattern

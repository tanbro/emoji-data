import os
from enum import Enum
from typing import Union, List, Iterable

from pkg_resources import Requirement, resource_stream

from . import version
from .types import BaseDictContainer
from .utils import read_data_file_iterable

__all__ = ['EmojiCharProperty', 'EmojiCharacter', 'TEXT_PRESENTATION_SELECTOR', 'EMOJI_PRESENTATION_SELECTOR',
           'EMOJI_KEYCAP']

PACKAGE = '.'.join(version.__name__.split('.')[:-1])
DATAFILE_STREAM = resource_stream(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-data.txt']))
)

TEXT_PRESENTATION_SELECTOR = 0xFE0E
EMOJI_PRESENTATION_SELECTOR = 0xFE0F
EMOJI_KEYCAP = 0x20E3

IGNORE_CODES = [
                   0x0023,  # 1.1  [1] (#️)       number sign
                   0x002A,  # 1.1  [1] (*️)       asterisk
               ] + list(range(0x0030, 0x0039 + 1))  # 1.1 [10] (0️..9️)    digit zero..digit nine


class EmojiCharProperty(Enum):
    """Emoji Character Properties

    see: http://www.unicode.org/reports/tr51/#Emoji_Properties
    """
    EMOJI = 'Emoji'
    EPRES = 'Emoji_Presentation'
    EMOD = 'Emoji_Modifier'
    EBASE = 'Emoji_Modifier_Base'
    ECOMP = 'Emoji_Component'
    EXTPICT = 'Extended_Pictographic'


class _MetaClass(BaseDictContainer):
    pass


class EmojiCharacter(metaclass=_MetaClass):
    """emoji character — A character that has the Emoji property. These characters are recommended for use as emoji.

    see: http://www.unicode.org/reports/tr51/#Emoji_Characters
    """

    def __init__(self,
                 code_point: int,
                 properties: Union[List[EmojiCharProperty], EmojiCharProperty] = None,
                 comments: Union[List[str], str] = None,
                 ):
        self._code_point = code_point
        if code_point > 0xffff:
            self._regex = r'\U{:08X}'.format(code_point)
        else:
            self._regex = r'\u{:04X}'.format(code_point)
        #
        self._properties = list()  # type: List[EmojiCharProperty]
        if properties is not None:
            if isinstance(properties, Iterable):
                self._properties = list(properties)
            else:
                self._properties = [properties]
        #
        self._comments = list()  # type: List[EmojiCharProperty]
        if comments is not None:
            if isinstance(comments, Iterable):
                self._comments = list(comments)
            else:
                self._comments = [comments]

    def __str__(self):
        return self.string

    def __repr__(self):
        return '<{} hex={} char={!r}>'.format(
            type(self).__name__,
            self.hex,
            self.string,
        )

    _initial = False

    @classmethod
    def initial(cls):
        """Initial the class

        Load Emoji Characters and there properties from package data file into class internal dictionary

        .. note:: **MUST** call this before other operations on the class
        """
        if cls._initial:
            return
        for content, comment in read_data_file_iterable(DATAFILE_STREAM):
            if not content:
                continue
            cps, property_text = (part.strip() for part in content.split(';', 1))
            cps_parts = cps.split('..', 1)
            property_ = EmojiCharProperty(property_text)
            for cp in range(int(cps_parts[0], 16), 1 + int(cps_parts[-1], 16)):  # pylint:disable=invalid-name
                try:
                    inst = cls[cp]  # type: EmojiCharacter
                except KeyError:
                    cls[cp] = cls(cp, property_, comment)  # type: EmojiCharacter
                else:
                    inst.add_property(property_)
                    inst.add_comment(comment)
        for cp in TEXT_PRESENTATION_SELECTOR, EMOJI_PRESENTATION_SELECTOR, EMOJI_KEYCAP:  # pylint:disable=invalid-name
            if cp not in cls:
                cls[cp] = cls(cp)
        cls._initial = True

    @classmethod
    def is_emoji_character(cls, val: Union[str, int]) -> bool:
        """Check if a **single** character belong to Emoji characters

        :param str val: character to check. Could be a single string, hex string, or integer
        :return: Whether if emoji character
        :rtype: bool
        """
        if isinstance(val, str):
            val = val.strip()
            if len(val) < 2:
                cp = ord(val)
            else:
                cp = int(val, 16)
        else:
            cp = int(val)
        return cp not in IGNORE_CODES and cp in cls

    def add_property(self, val: EmojiCharProperty):
        if val not in self._properties:
            self._properties.append(val)

    def add_comment(self, val: str):
        if val not in self._properties:
            self._comments.append(val)

    @property
    def code_point(self) -> int:
        """Unicode integer value of the Emoji

        :type: int
        """
        return self._code_point

    @property
    def properties(self) -> List[EmojiCharProperty]:
        """Property description text of the Emoji

        :type: List[EmojiCharProperty]
        """
        return self._properties

    @property
    def comments(self) -> List[str]:
        """Comments of the Emoji

        :type: List[str]
        """
        return self._comments

    @property
    def regex(self) -> str:
        """Regular express for the Emoji

        :type: str
        """
        return self._regex

    @property
    def hex(self) -> str:
        """Hex style text of the Emoji's Unicode

        :type: str
        """
        return hex(self._code_point)

    @property
    def string(self) -> str:
        """Emoji character string

        :type: string
        """
        return chr(self._code_point)

    @classmethod
    def from_single_string(cls, value):  # type: (str)->EmojiCharacter
        """Get an :class:`EmojiCharacter` instance by Emoji Unicode character

        :param value: Emoji character
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiCharacter
        :raises KeyError: When character not found in the class' internal dictionary
        """
        return cls[ord(value)]

    @classmethod
    def from_hex(cls, value):  # type: (Union[int, str])->EmojiCharacter
        """Get an :class:`EmojiCharacter` instance by Emoji Unicode integer value or it's hex string

        :param value: Emoji Unicode, either integer value or hex string
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiCharacter
        :raises KeyError: When code not found in the class' internal dictionary
        """
        if isinstance(value, int):
            return cls[value]
        else:
            return cls[int(value, 16)]

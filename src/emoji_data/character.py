import os
from enum import Enum
from typing import Union, List, Iterable

from pkg_resources import Requirement, resource_stream

from . import version
from .utils import BaseDictContainer, read_data_file_stream_iterable

__all__ = ['EmojiCharProperty', 'EmojiCharacter', 'TEXT_PRESENTATION_SELECTOR', 'EMOJI_PRESENTATION_SELECTOR']

PACKAGE = '.'.join(version.__name__.split('.')[:-1])
DATAFILE_STREAM = resource_stream(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-data.txt']))
)

TEXT_PRESENTATION_SELECTOR = 0xFE0E
EMOJI_PRESENTATION_SELECTOR = 0xFE0F


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

    def __init__(self, codepoint: int, properties: Union[List[EmojiCharProperty], EmojiCharProperty] = None):
        self._codepoint = codepoint
        if codepoint > 0xffff:
            self._regex = r'\U{:08X}'.format(codepoint)
        else:
            self._regex = r'\u{:04X}'.format(codepoint)
        self._properties = list()  # type: List[EmojiCharProperty]
        if properties is not None:
            if isinstance(properties, Iterable):
                self._properties = list(properties)
            else:
                self._properties = [properties]

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
        for line in read_data_file_stream_iterable(DATAFILE_STREAM):  # type: str
            if not line:
                continue
            cps, property_text = (part.strip() for part in line.split(';', 1))
            cps_parts = cps.split('..', 1)
            property_ = EmojiCharProperty(property_text)
            for cp in range(int(cps_parts[0], 16), 1 + int(cps_parts[-1], 16)):  # pylint:disable=invalid-name
                try:
                    inst = cls[cp]  # type: EmojiCharacter
                except KeyError:
                    cls[cp] = cls(cp, property_)  # type: EmojiCharacter
                else:
                    inst.add_property(property_)
        for cp in TEXT_PRESENTATION_SELECTOR, EMOJI_PRESENTATION_SELECTOR:  # pylint:disable=invalid-name
            if cp not in cls:
                cls[cp] = cls(cp)
        cls._initial = True

    @classmethod
    def is_emoji_char(cls, c: str) -> bool:
        """Check if emoji character

        :param str c: character to check
        :return: Whether if emoji character
        :rtype: bool
        """
        if len(c) != 1:
            raise ValueError('Length of char string should be 1')
        code = ord(c)
        return code not in IGNORE_CODES and code in cls

    @classmethod
    def is_emoji_code(cls, code: int) -> bool:
        """Check if an unicode integer value emoji character

        :param int code: code to check
        :return: Whether if emoji character
        :rtype: bool
        """
        return code not in IGNORE_CODES and code in cls

    @classmethod
    def is_emoji_hex(cls, hex_str: str) -> bool:
        """Check if an unicode integer hex express emoji character

        :param str hex_str: hex code to check
        :return: Whether if emoji character
        :rtype: bool
        """
        code = int(hex_str, 16)
        return code not in IGNORE_CODES and code in cls

    def add_property(self, val: EmojiCharProperty):
        if val not in self._properties:
            self._properties.append(val)

    @property
    def codepoint(self) -> int:
        """Unicode integer value of the Emoji

        :type: int
        """
        return self._codepoint

    @property
    def properties(self) -> List[EmojiCharProperty]:
        """Property description text of the Emoji

        :type: List[EmojiCharProperty]
        """
        return self._properties

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
        return hex(self._codepoint)

    @property
    def string(self) -> str:
        """Emoji character string

        :type: string
        """
        return chr(self._codepoint)

    @classmethod
    def from_codepoint(cls, val):  # type: (int)->EmojiCharacter
        """Get an :class:`EmojiCharacter` instance by Emoji Unicode's integer value

        :param int val: Integer value of the Emoji's Unicode
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiCharacter
        :raises KeyError: When integer code not found in the class' internal dictionary
        """
        return cls[val]

    @classmethod
    def from_char(cls, val):  # type: (str)->EmojiCharacter
        """Get an :class:`EmojiCharacter` instance by Emoji Unicode character

        :param val: Emoji character
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiCharacter
        :raises KeyError: When character not found in the class' internal dictionary
        """
        return cls[ord(val)]

    @classmethod
    def from_hex(cls, val):  # type: (str)->EmojiCharacter
        """Get an :class:`EmojiCharacter` instance by Emoji Unicode's HEX string

        :param val: Emoji Unicode's HEX
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiCharacter
        :raises KeyError: When code not found in the class' internal dictionary
        """
        return cls[int(val, 16)]

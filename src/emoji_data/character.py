import os
from enum import Enum
from typing import Iterable, List, Union

from pkg_resources import Requirement, resource_filename

from . import version
from .types import BaseDictContainer
from .utils import code_point_to_regex, read_data_file_iterable

__all__ = ['EmojiCharProperty', 'EmojiCharacter', 'TEXT_PRESENTATION_SELECTOR', 'EMOJI_PRESENTATION_SELECTOR',
           'EMOJI_KEYCAP', 'REGIONAL_INDICATORS', 'TAGS', 'ZWJ']

PACKAGE = '.'.join(version.__name__.split('.')[:-1])

DATA_FILE = resource_filename(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-data.txt']))
)

TEXT_PRESENTATION_SELECTOR = 0xFE0E
EMOJI_PRESENTATION_SELECTOR = 0xFE0F
EMOJI_KEYCAP = 0x20E3
ZWJ = 0x200D
REGIONAL_INDICATORS = list(range(0x1F1E6, 0x1F1FF + 1))
TAGS = list(range(0xE0020, 0xE007F + 1))


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
        self._string = chr(self._code_point)
        self._regex = code_point_to_regex(code_point)
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
        return self._string

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

        Load Emoji Characters and it's properties from package data file into class internal dictionary
        """
        if cls._initial:
            return
        with open(DATA_FILE, encoding='utf-8') as fp:
            for content, comment in read_data_file_iterable(fp):
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
        # OK!
        cls._initial = True

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

        :type: str
        """
        return self._string

    @classmethod
    def from_string(cls, value):  # type: (str)->EmojiCharacter
        """Get an :class:`EmojiCharacter` instance by Emoji Unicode character

        :param str value: Emoji character
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiCharacter
        :raises KeyError: When character not found in the class' internal dictionary
        """
        return cls[ord(value)]

    @classmethod
    def from_hex(cls, value):  # type: (Union[int, str])->EmojiCharacter
        """Get an :class:`EmojiCharacter` instance by Emoji Unicode integer value or it's hex string

        :param Union[int, str] value: Emoji Unicode, either integer value or hex string
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiCharacter
        :raises KeyError: When code not found in the class' internal dictionary
        """
        if isinstance(value, str):
            return cls[int(value, 16)]
        return cls[int(value)]


EmojiCharacter.initial()

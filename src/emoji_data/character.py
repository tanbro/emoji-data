"""Characters properties for Emoji
"""
import os
import typing as t
from enum import Enum

from pkg_resources import Requirement, resource_stream

from . import version

__all__ = ['EmojiCharProperty', 'EmojiCharacter']

PACKAGE = '.'.join(version.__name__.split('.')[:-1])
DATAFILE_STREAM = resource_stream(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-data.txt']))
)

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


class _MetaClass(type):
    def __new__(cls, name, bases, atts):
        cls._data = {}
        return super().__new__(cls, name, bases, atts)

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


class EmojiCharacter(metaclass=_MetaClass):
    def __init__(self, code: int, properties: t.Union[t.List[EmojiCharProperty], EmojiCharProperty] = None):
        """Emoji character with properties listed in the Emoji Character Properties table

        :param code: Integer value(code-point) of the Emoji Unicode.
        :param properties: Properties of the Emoji Character.
        """
        self._code = code
        if code > 0xffff:
            self._regex = r'\U{:08X}'.format(code)
        else:
            self._regex = r'\u{:04X}'.format(code)
        if properties is None:
            self._properties = list()
        elif isinstance(properties, EmojiCharProperty):
            self._properties = [EmojiCharProperty]
        elif isinstance(properties, t.Iterable):
            self._properties = list(properties)

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
        if cls._initial:
            return
        for byte_string in DATAFILE_STREAM:  # type: bytes
            byte_string = byte_string.strip()
            if not byte_string:
                continue
            if byte_string[0] in b'#;':
                continue
            line = byte_string.decode('utf-8')  # type: str
            line = line.split('#', 1)[0].strip()
            code_points_text, property_text = (part.strip() for part in line.split(';', 1))
            code_points_parts = code_points_text.split('..', 1)
            property_ = EmojiCharProperty(property_text)
            for code in range(int(code_points_parts[0], 16), 1 + int(code_points_parts[-1], 16)):
                try:
                    obj = cls[code]  # type: EmojiCharacter
                except KeyError:
                    cls[code] = cls(code, property_)  # type: EmojiCharacter
                else:
                    obj.add_property(property_)
        cls._initial = True

    @classmethod
    def is_emoji_char(cls, char: str) -> bool:
        if len(char) != 1:
            raise ValueError('Length of char string should be 1')
        code = ord(char)
        return code not in IGNORE_CODES and code in cls

    @classmethod
    def is_emoji_code(cls, code: int) -> bool:
        return code not in IGNORE_CODES and code in cls

    @classmethod
    def is_emoji_hex(cls, hex_str: str) -> bool:
        code = int(hex_str, 16)
        return code not in IGNORE_CODES and code in cls

    def add_property(self, val: EmojiCharProperty):
        if val not in self._properties:
            self._properties.append(val)

    @property
    def code(self) -> int:
        """
        Returns
        -------
        int
            Unicode integer value of the Emoji
        """
        return self._code

    @property
    def properties(self) -> t.List[EmojiCharProperty]:
        """
        Returns
        -------
        str
            Property description text of the Emoji
        """
        return self._properties

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
    def hex(self) -> str:
        """
        Returns
        -------
        str
            Hex style text of the Emoji's Unicode
        """
        return hex(self._code)

    @property
    def string(self) -> str:
        """
        Returns
        -------
        str
            Emoji character
        """
        return chr(self._code)

    @classmethod
    def from_code(cls, val):  # type: (int)->EmojiCharacter
        """Return a :class:`EmojiChar` object by Emoji Unicode's integer value

        Parameters
        ----------
        val : int
            Integer value of the Emoji's Unicode

        Returns
        -------
        EmojiCharacter
            Object returned

        Raises
        ------
        KeyError
            When integer code not found
        """
        return cls[val]

    @classmethod
    def from_char(cls, val):  # type: (str)->EmojiCharacter
        """Return a :class:`EmojiChar` object by Emoji Unicode character

        Parameters
        ----------
        val : str
            Emoji character

        Returns
        -------
        EmojiCharacter
            Object returned

        Raises
        ------
        KeyError
            When Charactor code not found
        """
        return cls[ord(val)]

    @classmethod
    def from_hex(cls, val):  # type: (str)->EmojiCharacter
        """Return a :class:`EmojiChar` object by Emoji Unicode's HEX text

        Parameters
        ----------
        val : str
            Emoji Unicode's HEX

        Returns
        -------
        EmojiCharacter
            Object returned

        Raises
        ------
        KeyError
            When Charactor code not found
        """
        return cls[int(val, 16)]

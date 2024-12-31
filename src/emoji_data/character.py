from __future__ import annotations

import re
from enum import Enum
from typing import Iterable, Iterator, MutableSequence, Optional, Sequence, Tuple, Union, final

from .container import BaseDictContainer
from .utils import code_point_to_regex, emoji_data_lines

__all__ = [
    "EmojiCharProperty",
    "EmojiCharacter",
    "TEXT_PRESENTATION_SELECTOR",
    "EMOJI_PRESENTATION_SELECTOR",
    "EMOJI_KEYCAP",
    "REGIONAL_INDICATORS",
    "TAGS",
    "ZWJ",
]


TEXT_PRESENTATION_SELECTOR = 0xFE0E
"""The character U+FE0E VARIATION SELECTOR-15 (VS15), used to request a text presentation for an emoji character.
(Also known as text variation selector in prior versions of this specification.)
"""

EMOJI_PRESENTATION_SELECTOR = 0xFE0F
"""The character U+FE0F VARIATION SELECTOR-16 (VS16), used to request an emoji presentation for an emoji character.
(Also known as emoji variation selector in prior versions of this specification.)
"""

EMOJI_KEYCAP = 0x20E3
"""A sequence of the following form::

    emoji_keycap_sequence := [0-9#*] \\x{FE0F 20E3}

- These sequences are in the `emoji-sequences.txt` file listed under the type_field ``Emoji_Keycap_Sequence``
"""

ZWJ = 0x200D
"""An emoji sequence with at least one joiner character.
"""

REGIONAL_INDICATORS = list(range(0x1F1E6, 0x1F1FF + 1))
"""regional indicators"""

TAGS = list(range(0xE0020, 0xE007F + 1))
"""tags"""


class EmojiCharProperty(Enum):
    """Emoji Character Properties

    character properties are available for emoji characters.

    See also:
        http://www.unicode.org/reports/tr51/#Emoji_Properties
    """

    EMOJI = "Emoji"
    """for characters that are emoji"""

    EPRES = "Emoji_Presentation"
    """ for characters that have emoji presentation by default"""

    EMOD = "Emoji_Modifier"
    """for characters that are emoji modifiers"""

    EBASE = "Emoji_Modifier_Base"
    """for characters that can serve as a base for emoji modifiers"""

    ECOMP = "Emoji_Component"
    """for characters used in emoji sequences that normally do not appear on emoji keyboards as separate choices, such as keycap base characters or Regional_Indicator characters.

    All characters in emoji sequences are either Emoji or Emoji_Component.
    Implementations must not, however, assume that all Emoji_Component characters are also Emoji.
    There are some non-emoji characters that are used in various emoji sequences, such as tag characters and ZWJ.
    """

    EXTPICT = "Extended_Pictographic"
    """for characters that are used to future-proof segmentation.

    The Extended_Pictographic characters contain all the Emoji characters except for some Emoji_Component characters.
    """


class MetaClass(BaseDictContainer[int, "EmojiCharacter"]):
    pass


@final
class EmojiCharacter(metaclass=MetaClass):  # pyright: ignore[reportGeneralTypeIssues]
    """emoji character — A character that has the Emoji property.

    These characters are recommended for use as emoji.

    See also:
        http://www.unicode.org/reports/tr51/#Emoji_Characters
    """

    def __init__(
        self,
        code_point: int,
        properties: Union[EmojiCharProperty, Iterable[EmojiCharProperty], None] = None,
        version: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self._code_point = code_point
        self._string = chr(self._code_point)
        self._regex = code_point_to_regex(code_point)
        #
        self._properties: MutableSequence[EmojiCharProperty]
        if properties is None:
            self._properties = []
        elif isinstance(properties, EmojiCharProperty):
            self._properties = [properties]
        elif isinstance(properties, Iterable):
            if not all(isinstance(x, EmojiCharacter) for x in properties):
                raise TypeError("not all elements of `properties` are `EmojiCharacter`")
            self._properties = list(properties)
        else:
            raise TypeError(f"{type(properties)}")
        #
        self._version = version or ""
        self._description = description or ""

    def __str__(self):
        return self._string

    def __repr__(self):
        return "<{} code_point={} char={!r} version={!r} description={!r}>".format(
            type(self).__name__, self.code_point_string, self.string, self.version, self.description
        )

    _comment_split_regex = re.compile(r"\[\d+\]\s*\(.*\)")

    @classmethod
    def initial(cls):
        """Initial the class

        Load emoji characters and their properties from the package data file into the class's internal dictionary.
        """
        if cls.__data_dict__:
            return
        for content, comment in emoji_data_lines("emoji-data.txt"):
            cps, property_text = (part.strip() for part in content.split(";", 1))
            cps_parts = cps.split("..", 1)
            property_ = EmojiCharProperty(property_text)
            version, description = (s.strip() for s in cls._comment_split_regex.split(comment, maxsplit=1))
            for cp in range(int(cps_parts[0], 16), 1 + int(cps_parts[-1], 16)):
                try:
                    inst = cls[cp]
                except KeyError:
                    cls[cp] = cls(cp, property_, version, description)
                else:
                    inst._add_property(property_)
        for cp in (TEXT_PRESENTATION_SELECTOR, EMOJI_PRESENTATION_SELECTOR, EMOJI_KEYCAP):
            if cp not in cls:
                cls[cp] = cls(cp, [])

    @classmethod
    def release(cls):
        cls.__data_dict__.clear()

    @classmethod
    def items(cls) -> Iterator[Tuple[int, EmojiCharacter]]:
        """Return an iterator over all (code point, emoji character) pairs in the class.

        Yields:
            : A tuple containing a code point and its corresponding emoji character.
        """
        return ((k, cls[k]) for k in cls)

    @classmethod
    def keys(cls) -> Iterator[int]:
        """Return an iterator over all code points of emoji characters in the class.

        Yields:
            : The code point of an emoji character.
        """
        yield from cls

    @classmethod
    def values(cls) -> Iterator[EmojiCharacter]:
        """Return an iterator over all emoji characters in the class.

        Yields:
            : An emoji character instance.
        """
        return (cls[k] for k in cls)

    def _add_property(self, val: EmojiCharProperty):
        if val not in self._properties:
            self._properties.append(val)

    @property
    def code_point(self) -> int:
        """Unicode integer value of the emoji-characters"""
        return self._code_point

    @property
    def code_point_string(self) -> str:
        """Unicode style hex string of the emoji-characters's code-point

        Example:
            ``"25FB"``
        """
        return f"{self._code_point:04X}"

    @property
    def properties(self) -> Sequence[EmojiCharProperty]:
        """Property description text of the emoji-characters"""
        return list(self._properties)

    @property
    def version(self) -> str:
        """Version of the Emoji.

        Example:
            ``E0.0``, ``E0.6``, ``E11.0``
        """
        return self._version

    @property
    def description(self) -> str:
        """Description comment of the Emoji"""
        return self._description

    @property
    def regex(self) -> str:
        """Regular express for the emoji-characters"""
        return self._regex

    @property
    def hex(self) -> str:
        """Python style hex string of the emoji-characters's code-pint

        Example:
            ``"0x25fb"``
        """
        return hex(self._code_point)

    @property
    def string(self) -> str:
        """Emoji character string"""
        return self._string

    @classmethod
    def from_character(cls, c: str) -> "EmojiCharacter":
        """Get an :class:`EmojiCharacter` instance from a single Unicode emoji character.

        Args:
            c (str): A single Unicode emoji character.

                Note:
                    ``c`` should be a **single** Unicode character, i.e., ``len(c) == 1``.

        Returns:
            An instance retrieved from the class's internal dictionary.

        Raises:
            KeyError: If the character is not found in the class's internal dictionary.
        """
        return cls[ord(c)]

    @classmethod
    def from_hex(cls, value: Union[int, str]) -> EmojiCharacter:
        """Get an :class:`EmojiCharacter` instance by Emoji Unicode integer value or its hex string.

        Args:
            value (Union[int, str]): Emoji Unicode, either an integer value or a hex string.

        Returns:
            An instance retrieved from the class's internal dictionary.

        Raises:
            KeyError: If the code is not found in the class's internal dictionary.
        """
        if isinstance(value, str):
            return cls[int(value, 16)]
        return cls[int(value)]

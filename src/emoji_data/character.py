from __future__ import annotations

from enum import Enum
from typing import Iterable, Iterator, MutableSequence, Sequence, Tuple, Union, final

from .types import BaseDictContainer
from .utils import code_point_to_regex, read_data_file_iterable

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
        properties: Union[Iterable[EmojiCharProperty], EmojiCharProperty, None] = None,
        comments: Union[Iterable[str], str, None] = None,
    ):
        self._code_point = code_point
        self._string = chr(self._code_point)
        self._regex = code_point_to_regex(code_point)
        #
        if properties is None:
            self._properties: MutableSequence[EmojiCharProperty] = []
        elif isinstance(properties, EmojiCharProperty):
            self._properties = [properties]
        elif isinstance(properties, Iterable):
            self._properties = list(properties)
        else:
            raise TypeError(
                f"Argument `properties` expects `EmojiCharProperty`, `Iterable[EmojiCharProperty]`, or `None`, but actual {type(properties)}"
            )
        #
        if comments is None:
            self._comments: MutableSequence[str] = []
        elif isinstance(comments, str):
            self._comments = [comments]
        elif isinstance(comments, Iterable):
            self._comments = [s for s in comments if isinstance(s, str)]
        else:
            raise TypeError(f"Argument `comments` expects `str`, `Iterable[str]`, or `None`, but actual {type(comments)}")

    def __str__(self):
        return self._string

    def __repr__(self):
        return "<{} code_point={} char={!r}>".format(
            type(self).__name__,
            self.code_point_string,
            self.string,
        )

    _initialed = False

    @classmethod
    def initial(cls):
        """Initial the class

        Load Emoji Characters and it's properties from package data file into class internal dictionary
        """
        if cls._initialed:
            return
        for content, comment in read_data_file_iterable("emoji-data.txt"):
            cps, property_text = (part.strip() for part in content.split(";", 1))
            cps_parts = cps.split("..", 1)
            property_ = EmojiCharProperty(property_text)
            for cp in range(int(cps_parts[0], 16), 1 + int(cps_parts[-1], 16)):
                try:
                    inst = cls[cp]
                except KeyError:
                    cls[cp] = cls(cp, property_, comment)
                else:
                    inst._add_property(property_)
                    inst._add_comment(comment)
        for cp in (TEXT_PRESENTATION_SELECTOR, EMOJI_PRESENTATION_SELECTOR, EMOJI_KEYCAP):
            if cp not in cls:
                cls[cp] = cls(cp)
        # OK!
        cls._initialed = True

    @classmethod
    def release(cls):
        if not cls._initialed:
            return
        keys = list(cls)
        for k in keys:
            del cls[k]
        cls._initialed = False

    @classmethod
    def items(cls) -> Iterator[Tuple[int, EmojiCharacter]]:
        """Returns an iterator of all code-point -> emoji-character pairs of the class"""
        return ((k, cls[k]) for k in cls)

    @classmethod
    def keys(cls) -> Iterator[int]:
        """Returns an iterator of each emoji-character's key code-point of the class"""
        yield from cls

    @classmethod
    def values(cls) -> Iterator[EmojiCharacter]:
        """Returns an iterator of all emoji-characters of the class"""
        return (cls[k] for k in cls)

    def _add_property(self, val: EmojiCharProperty):
        if val not in self._properties:
            self._properties.append(val)

    def _add_comment(self, val: str):
        if val not in self._properties:
            self._comments.append(val)

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
        return self._properties

    @property
    def comments(self) -> Sequence[str]:
        """Comments of the Emoji"""
        return self._comments

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
    def from_character(cls, c: str) -> EmojiCharacter:
        """Get :class:`EmojiCharacter` instance from a single Emoji Unicode character

        Args:
            c: Emoji character

                Note:
                    ``c`` should be a **single** unicode character, that is: ``len(c) == 1``.

        Returns:
            Instance returned from the class's internal dictionary

        Raises:
            KeyError: When character not found in the class' internal dictionary
        """
        return cls[ord(c)]

    @classmethod
    def from_hex(cls, value: Union[int, str]) -> EmojiCharacter:
        """Get an :class:`EmojiCharacter` instance by Emoji Unicode integer value or it's hex string

        Args:
            value: Emoji Unicode, either integer value or hex string

        Returns:
            Instance returned from the class's internal dictionary

        Raises:
            KeyError: When code not found in the class' internal dictionary
        """
        if isinstance(value, str):
            return cls[int(value, 16)]
        return cls[int(value)]


EmojiCharacter.initial()

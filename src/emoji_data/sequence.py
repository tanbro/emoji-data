from __future__ import annotations

import re
import sys
from typing import Pattern, Union

if sys.version_info < (3, 11):  # pragma: no cover
    from typing_extensions import Self
else:  # pragma: no cover
    from typing import Self

if sys.version_info < (3, 9):  # pragma: no cover
    from typing import Iterable, Sequence, Tuple, Generator
else:  # pragma: no cover
    from collections.abc import Iterable, Sequence, Generator

from .character import EmojiCharacter
from .types import BaseDictContainer
from .utils import data_file, read_data_file_iterable

__all__ = ["EmojiSequence"]

# http://www.unicode.org/reports/tr51/#Data_Files_Table
# keep the order!
DATA_FILES = [
    "emoji-variation-sequences.txt",
    "emoji-zwj-sequences.txt",
    "emoji-sequences.txt",
]


class MetaClass(BaseDictContainer):
    pass


class EmojiSequence(metaclass=MetaClass):
    """Emoji and Text Presentation Sequences used to represent emoji

    see: http://www.unicode.org/reports/tr51/#Emoji_Sequences
    """

    def __init__(
        self,
        code_points: Union[Iterable[int], int],
        type_field: str = "",
        description: str = "",
        comment: str = "",
    ):
        if isinstance(code_points, Iterable):
            self._code_points = list(code_points)
        else:
            self._code_points = [code_points]
        self._string = "".join(chr(n) for n in self._code_points)
        self._characters = [EmojiCharacter.from_hex(n) for n in self._code_points]
        self._type_field = type_field.strip()
        self._comment = comment.strip()
        self._description = description
        # regex
        self._regex = r""
        if not self._regex:
            self._regex = "".join(m.regex for m in self._characters)
        self._regex_pat = re.compile(self._regex)

    def __len__(self):
        return len(self._code_points)

    def __str__(self):
        return self._string

    def __repr__(self):
        return "<{} code_points={!r} string={!r}, description={!r}>".format(
            type(self).__name__,
            self.code_points_string,
            self.string,
            self.description,
        )

    _initialed = False

    pattern: Pattern
    """Compiled regular expression pattern object for all-together Emoji sequences.
    """

    @classmethod
    def initial(cls):
        """Initial the class

        Load Emoji Sequences from package data file into class internal dictionary
        """
        if cls._initialed:
            return
        EmojiCharacter.initial()

        def _decode_code_points(_cps, **_kwargs):
            try:
                _cp_head, _cp_tail = _cps.split("..", 1)  # begin..end form
            except ValueError:
                _arr_cp = [int(x, 16) for x in _cps.split()]
                _seq = cls(_arr_cp, **_kwargs)
                cls[_seq.string] = _seq
            else:
                # begin..end form: A range of single char emoji-seq
                for _cp in range(int(_cp_head, 16), 1 + int(_cp_tail, 16)):
                    _seq = cls(_cp, **_kwargs)
                    cls[_seq.string] = _seq

        for fname in DATA_FILES:
            with data_file(fname).open(encoding="utf8") as fp:
                for content, comment in read_data_file_iterable(fp):
                    if fname in ("emoji-sequences.txt", "emoji-zwj-sequences.txt"):
                        cps, type_field, description = (part.strip() for part in content.split(";", 2))
                        _decode_code_points(cps, type_field=type_field, description=description, comment=comment)
                    elif fname == "emoji-variation-sequences.txt":
                        cps, description = (part.strip() for part in content.split(";", 1))
                        _decode_code_points(cps, description=description, comment=comment)
                    else:
                        raise RuntimeError(f"Invalid data file name {fname}")
        # build regex
        cls.pattern = re.compile(
            r"|".join(m.regex for m in sorted((m for m in cls.values()), key=lambda x: len(x.code_points), reverse=True))
        )
        # initialed OK
        cls._initialed = True

    @classmethod
    def release(cls):
        if not cls._initialed:
            return
        keys = list(cls)
        for k in keys:
            del cls[k]
        cls._initialed = False

    if sys.version_info < (3, 9):

        @classmethod
        def items(cls) -> Iterable[Tuple[str, Self]]:
            return ((k, cls[k]) for k in cls)

    else:

        @classmethod
        def items(cls) -> Iterable[tuple[str, Self]]:
            """Return an iterator of all string -> emoji-sequence pairs of the class"""
            return ((k, cls[k]) for k in cls)

    @classmethod
    def keys(cls) -> Iterable[str]:
        """Return an iterator of each emoji-sequence's key string of the class"""
        return (k for k in cls)

    @classmethod
    def values(cls) -> Iterable[Self]:
        """Return an iterator of all emoji-sequences of the class"""
        return (cls[k] for k in cls)

    @classmethod
    def from_string(cls, s: str) -> Self:
        """Get an :class:`EmojiSequence` instance from string

        :param s: Emoji string
        :return: Instance from internal dictionary
        :raise KeyError: When passed-in ``s`` not found in internal dictionary
        """
        return cls[s]

    @classmethod
    def from_characters(cls, value: Union[EmojiCharacter, Iterable[EmojiCharacter]]) -> Self:
        """Get an :class:`EmojiSequence` instance from :class:`EmojiCharacter` object or list

        :param value: Single or iterable object of :class:`EmojiCharacter`, composing the sequence
        :return: Instance from internal dictionary
        :raise KeyError: When passed-in value not found in internal dictionary
        :raise TypeError: When passed-in value is not :class:`.EmojiCharacter` object or list
        """
        if isinstance(value, EmojiCharacter):
            s = value.string
        elif isinstance(value, Iterable):
            s = "".join(m.string for m in value)
        else:
            raise TypeError("Argument `value` must be one of `EmojiCharacter` or `Iterable[EmojiCharacter]`")
        return cls.from_string(s)

    @classmethod
    def from_hex(cls, value: Union[str, int, Iterable[str], Iterable[int]]) -> Self:
        """Get an :class:`EmojiSequence` instance by unicode code point(s)

        :type value: Union[str, int, Iterable[str], Iterable[int]]
        :param value: A single or sequence of HEX string/code.

            - it could be:

              - one or more code-point(s) in HEX format string, separated by spaces
              - a single code-point integer
              - An iterable object whose members are code-point string in HEX format
              - An iterable object whose members are code-point integer

        :return: Instance returned from the class's internal dictionary

        :raise KeyError: When passed-in value not found in the class' internal dictionary
        """
        if isinstance(value, str):
            cps_array = value.split()  # type: ignore[assignment]
        elif isinstance(value, int):
            cps_array = (value,)  # type: ignore[assignment]
        elif isinstance(value, Iterable) and not isinstance(value, str) and all(isinstance(m, (str, int)) for m in value):
            cps_array = value  # type: ignore[assignment]
        else:
            raise TypeError(
                f"Argument `value` expects to be one of `str`, `bytes`, `int`, or a sequence of that, but actual is {type(value)}"
            )
        return cls.from_characters(EmojiCharacter.from_hex(cp) for cp in cps_array)

    @property
    def type_field(self) -> str:
        """A convenience for parsing the emoji sequence files, and is not intended to be maintained as a property.

        may be one of:

        - `"Basic_Emoji"`
        - `"Emoji_Keycap_Sequence"`
        - `"Emoji_Flag_Sequence"`
        - `"Emoji_Tag_Sequence"`
        - `"Emoji_Modifier_Sequence"`
        - `"RGI_Emoji_ZWJ_Sequence"`
        """
        return self._type_field

    @property
    def description(self) -> str:
        return self._description

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def characters(self) -> Sequence[EmojiCharacter]:
        """Emoji character objects list which makes up the Emoji Sequence"""
        return self._characters

    @property
    def hex(self) -> str:
        """Python style hex string of each emoji-characters's code-point, separated by spaces

        eg: ``0xa9 0xfe0f``
        """
        return " ".join(c.hex for c in self.characters)

    @property
    def string(self) -> str:
        """string of the Emoji Sequence"""
        return self._string

    @property
    def regex(self) -> str:
        """Regular expression string of the Emoji Sequence"""
        return self._regex

    @property
    def regex_pattern(self):
        """Compiled regular expression pattern of the Emoji Sequence"""
        return self._regex_pat

    @property
    def code_points(self) -> Sequence[int]:
        """List of unicode integer value of the characters who make up Emoji Sequence"""
        return self._code_points

    @property
    def code_points_string(self) -> str:
        """Unicode style hex string of each emoji-characters's code-point, separated by spaces

        eg: ``00A9 FE0F``
        """
        return " ".join(c.code_point_string for c in self.characters)

    if sys.version_info < (3, 9):

        @classmethod
        def find_all(cls, s: str) -> Sequence[Tuple[Self, int, int]]:
            return list(cls.find(s))

    else:

        @classmethod
        def find_all(cls, s: str) -> Sequence[tuple[Self, int, int]]:
            """Find out all emoji sequences in a string, and return them in a list

            Item of the returned list is as same as that in the iterator of :meth:`find`

            The function equals::

                list(EmojiSequence.find(s))

            or ::

                [x for x in EmojiSequence.find(s)]
            """
            return list(cls.find(s))

    if sys.version_info < (3, 9):

        @classmethod
        def find(cls, s: str) -> Generator[Tuple[Self, int, int], None, None]:
            m = cls.pattern.search(s)
            while m:
                yield cls.from_string(m.group()), m.start(), m.end()
                m = cls.pattern.search(s, m.end())

    else:

        @classmethod
        def find(cls, s: str) -> Generator[tuple[Self, int, int], None, None]:
            """Return an iterator which yields all emoji sequences in a string, without actually storing them all simultaneously.

            :param s: The string to find emoji sequences in it

            :return: Item of the iterator is a 3-member tuple:

                0. The found :class:`.EmojiSequence` object
                1. Begin position of the emoji sequence in the string
                2. End position of the emoji sequence in the string
            """
            m = cls.pattern.search(s)
            while m:
                yield cls.from_string(m.group()), m.start(), m.end()
                m = cls.pattern.search(s, m.end())


EmojiSequence.initial()

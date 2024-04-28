from __future__ import annotations

import re
import sys
from typing import ClassVar, Generator, Iterable, Iterator, Optional, Pattern, Sequence, Tuple, Union, final

if sys.version_info < (3, 11):  # pragma: no cover
    from typing_extensions import Self
else:  # pragma: no cover
    from typing import Self

from .character import EmojiCharacter
from .types import BaseDictContainer
from .utils import emoji_data_lines

__all__ = ["EmojiSequence"]

# http://www.unicode.org/reports/tr51/#Data_Files_Table
# keep the order!
DATA_FILES = ("emoji-variation-sequences.txt", "emoji-zwj-sequences.txt", "emoji-sequences.txt")


class MetaClass(BaseDictContainer[str, "EmojiSequence"]):
    pass


@final
class EmojiSequence(metaclass=MetaClass):  # pyright: ignore[reportGeneralTypeIssues]
    """Emoji and Text Presentation Sequences used to represent emoji

    See also:
        http://www.unicode.org/reports/tr51/#Emoji_Sequences
    """

    def __init__(
        self,
        code_points: Union[int, Iterable[int]],
        type_field: Optional[str] = None,
        version: Optional[str] = None,
        variation: Optional[str] = None,
        description: Optional[str] = None,
    ):
        if isinstance(code_points, Iterable):
            self._code_points = list(code_points)
        else:
            self._code_points = [code_points]
        self._string = "".join(chr(n) for n in self._code_points)
        self._characters = [EmojiCharacter.from_hex(n) for n in self._code_points]
        self._type_field = type_field or ""
        self._version = version or ""
        self._variation = variation or ""
        self._description = description or ""
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
        return "<{} code_points={!r} string={!r} version={!r} description={!r}>".format(
            type(self).__name__, self.code_points_string, self.string, self.version, self.description
        )

    _initialed = False

    pattern: ClassVar[Pattern[str]]
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
            for content, comment in emoji_data_lines(fname):
                if fname in ("emoji-sequences.txt", "emoji-zwj-sequences.txt"):
                    cps, type_field, description = (part.strip() for part in content.split(";", 2))
                    version = comment.split(maxsplit=1)[0]
                    _decode_code_points(cps, type_field=type_field, version=version, description=description)
                elif fname == "emoji-variation-sequences.txt":
                    cps, variation, _ = (part.strip() for part in content.split(";", 2))
                    version, description = (x.strip() for x in comment.split(maxsplit=1))
                    version = "E" + version.lstrip("(").rstrip(")").strip()
                    description = f"{description.lower()} ({variation})"
                    _decode_code_points(cps, version=version, variation=variation, description=description)
                else:
                    raise RuntimeError(f"Invalid data file name {fname}")
        # build regex
        cls.pattern = re.compile(
            r"|".join(
                m.regex
                for m in sorted(
                    (m for m in cls.values()),
                    key=lambda x: len(x.code_points),
                    reverse=True,
                )
            )
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

    @classmethod
    def items(cls) -> Iterator[Tuple[str, Self]]:
        """Returns an iterator of all string -> emoji-sequence pairs of the class"""
        return ((k, cls[k]) for k in cls)  # pyright: ignore[reportReturnType]

    @classmethod
    def keys(cls) -> Iterator[str]:
        """Returns an iterator of each emoji-sequence's key string of the class"""
        yield from cls

    @classmethod
    def values(cls) -> Iterator[Self]:
        """Returns an iterator of all emoji-sequences of the class"""
        return (cls[k] for k in cls)  # pyright: ignore[reportReturnType]

    @classmethod
    def from_string(cls, s: str) -> Self:
        """Get an :class:`EmojiSequence` instance from string

        Args:
            s: Emoji string

        Returns:
            Instance from internal dictionary

        Raises:
            KeyError: When passed-in ``s`` not found in internal dictionary
        """
        return cls[s]  # pyright: ignore[reportReturnType]

    @classmethod
    def from_characters(cls, value: Union[EmojiCharacter, Iterable[EmojiCharacter]]) -> Self:
        """Get an :class:`EmojiSequence` instance from :class:`EmojiCharacter` object or list

        Args:
            value: Single or iterable object of :class:`EmojiCharacter`, composing the sequence

        Returns:
            Instance from internal dictionary

        Raises:
            KeyError: When passed-in value not found in internal dictionary
            TypeError: When passed-in value is not :class:`.EmojiCharacter` object or list
        """
        if isinstance(value, EmojiCharacter):
            s = value.string
        elif isinstance(value, Iterable):
            s = "".join(m.string for m in value)
        else:
            raise TypeError("Argument `value` must be one of `EmojiCharacter` or `Iterable[EmojiCharacter]`")
        return cls.from_string(s)

    @classmethod
    def from_hex(cls, value: Union[int, str, Iterable[Union[int, str]]]) -> Self:
        """Get an :class:`EmojiSequence` instance by unicode code point(s)

        Args:
            value: A single or sequence of HEX string/code.

                it could be:

                - one or more code-point(s) in HEX format string, separated by spaces
                - a single code-point integer
                - An iterable object whose members are code-point string in HEX format
                - An iterable object whose members are code-point integer

        Returns:
            Instance returned from the class's internal dictionary

        Raises:
            KeyError: When passed-in value not found in the class internal dictionary
        """
        cps_array: Iterable[Union[int, str]]
        if isinstance(value, str):
            cps_array = value.split()
        elif isinstance(value, int):
            cps_array = (value,)
        elif isinstance(value, Iterable):
            cps_array = value
        else:
            raise TypeError(
                f"Argument `value` expects to be one of `str`, `bytes`, `int`, or a sequence of that, but actual is {type(value)}"
            )
        return cls.from_characters(EmojiCharacter.from_hex(cp) for cp in cps_array)  # pyright: ignore[reportReturnType]

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
        """Description"""
        return self._description

    @property
    def version(self) -> str:
        """Version of the Emoji.

        Example:
            ``E0.0``, ``E0.6``, ``E11.0``
        """
        return self._version

    @property
    def variation(self) -> str:
        """``"emoji style"`` or ``"text style"`` of a variable sequence"""
        return self._variation

    @property
    def characters(self) -> Sequence[EmojiCharacter]:
        """Emoji character objects list which makes up the Emoji Sequence"""
        return self._characters

    @property
    def hex(self) -> str:
        """Python style hex string of each emoji-characters's code-point, separated by spaces

        Example:
            ``"0xa9 0xfe0f"``
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
        """List of unicode integer value of the characters who make up this Emoji Sequence"""
        return self._code_points

    @property
    def code_points_string(self) -> str:
        """Unicode style hex string of each emoji-characters's code-point, separated by spaces

        eg: ``"00A9 FE0F"``
        """
        return " ".join(c.code_point_string for c in self.characters)

    @classmethod
    def find_all(cls, s: str) -> Sequence[Tuple[Self, int, int]]:
        """Find out all emoji sequences in a string, and return them in a list

        Items of the returned list is the same as ``yield`` result of :meth:`find`

        The function equals::

            list(EmojiSequence.find(s))

        or ::

            [x for x in EmojiSequence.find(s)]
        """
        return list(cls.find(s))  # pyright: ignore[reportReturnType]

    @classmethod
    def find(cls, s: str) -> Generator[Tuple[Self, int, int], None, None]:
        """Return an iterator which yields all emoji sequences in a string, without actually storing them all simultaneously.

        Args:
            s: The string to find emoji sequences in it

        Yields:
            : Yields at every matched emoji sequence as a 3-members tuple, whose members are:

                0. The found :class:`.EmojiSequence` object
                1. Begin position of the emoji sequence in the string
                2. End position of the emoji sequence in the string
        """
        for m in cls.pattern.finditer(s):
            yield cls.from_string(m.group()), m.start(), m.end()


EmojiSequence.initial()

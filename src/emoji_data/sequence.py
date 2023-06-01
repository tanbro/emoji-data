import re
from typing import Iterable, List, Tuple, Union

from .character import EmojiCharacter
from .types import BaseDictContainer
from .utils import data_file, read_data_file_iterable

__all__ = ["EmojiSequence"]

# http://www.unicode.org/reports/tr51/#Data_Files_Table
_DATA_FILES = [
    "emoji-variation-sequences.txt",
    "emoji-zwj-sequences.txt",
    "emoji-sequences.txt",
]


class _MetaClass(BaseDictContainer):
    pass


class EmojiSequence(metaclass=_MetaClass):
    """Emoji and Text Presentation Sequences used to represent emoji

    see: http://www.unicode.org/reports/tr51/#Emoji_Variation_Sequences
    """

    def __init__(
        self,
        code_points: Union[Iterable[int], int],
        status: str = "",
        type_field: str = "",
        description: str = "",
        comment: str = "",
    ):
        if isinstance(code_points, Iterable):
            self._code_points = list(code_points)
        else:
            self._code_points = [code_points]
        self._status = status.strip()
        self._string = "".join(chr(n) for n in self._code_points)
        self._characters = [EmojiCharacter.from_hex(n) for n in self._code_points]
        self._type_field = type_field.strip()
        self._comment = comment.strip()
        self._description = description
        # regex
        self._regex = r""
        if not self._regex:
            self._regex = "".join(m.regex for m in self._characters)
        self._regex_compiled = re.compile(self._regex)

    def __len__(self):
        return len(self._code_points)

    def __str__(self):
        return self._string

    def __repr__(self):
        return "<{} code_points={!r} status={!r}, string={!r}, description={!r}>".format(
            type(self).__name__,
            " ".join("{:04X}".format(n) for n in self._code_points),
            self._status,
            self._string,
            self._description,
        )

    _initialed = False

    pattern = re.compile(r"")
    """Compiled regular express pattern object for all-together Emoji sequences.
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
                if _seq.string not in cls:
                    cls[_seq.string] = _seq
            else:
                # begin..end form: A range of single char emoji-seq
                for _cp in range(int(_cp_head, 16), 1 + int(_cp_tail, 16)):
                    _seq = cls(_cp, **_kwargs)
                    if _seq.string not in cls:
                        cls[_seq.string] = _seq

        for fname in _DATA_FILES:
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
        ordered_list = sorted((m for m in cls.values()), key=lambda x: len(x.code_points), reverse=True)
        exp = r"|".join(m.regex for m in ordered_list)
        cls.pattern = re.compile(exp)
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
    def items(cls) -> Iterable[Tuple[str, "EmojiSequence"]]:
        """Return an iterator of all string -> emoji-sequence pairs of the class"""
        return ((k, cls[k]) for k in cls)

    @classmethod
    def values(cls) -> Iterable["EmojiSequence"]:
        """Return an iterator of all emoji-sequences of the class"""
        return (cls[k] for k in cls)

    @classmethod
    def from_string(cls, s: str) -> "EmojiSequence":
        """Get an :class:`EmojiSequence` instance from string

        :param str value: Emoji string
        :return: Instance from internal dictionary
        :rtype: EmojiSequence
        :raise KeyError: When passed-in value not found in internal dictionary
        """
        return cls[s]

    @classmethod
    def from_characters(cls, value: Union[EmojiCharacter, Iterable[EmojiCharacter]]) -> "EmojiSequence":
        """Get an :class:`EmojiSequence` instance from :class:`EmojiCharacter` object or list

        :param value: Single or iterable object of :class:`EmojiCharacter`, composing the sequence
        :return: Instance from internal dictionary
        :rtype: EmojiSequence
        :raise KeyError: When passed-in value not found in internal dictionary
        """
        if isinstance(value, EmojiCharacter):
            s = value.string
        elif isinstance(value, Iterable):
            s = "".join(m.string for m in value)
        else:
            raise TypeError("Argument `value` must be one of `EmojiCharacter` or `Iterable[EmojiCharacter]`")
        return cls.from_string(s)

    @classmethod
    def from_hex(cls, value: Union[str, int, Iterable[str], Iterable[int]]) -> "EmojiSequence":
        """Get an :class:`EmojiSequence` instance by unicode code point(s)

        :type value: Union[str, int, Iterable[str], Iterable[int]]
        :param value: A single or sequence of HEX string/code.

            - it could be:

              - one or more code points in hex format string, separated by spaces
              - one code point integer
              - An iterable object whose members are code point in hex format string
              - An iterable object whose members are code point integer

        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiSequence

        :raise KeyError: When passed-in value not found in the class' internal dictionary
        """
        if isinstance(value, str):
            cps_array = value.split()
        elif isinstance(value, int):
            cps_array = (value,)
        elif isinstance(value, Iterable):
            cps_array = value
        else:
            raise TypeError("The `args` should be one of `str`, `int`, or a sequence of that")
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

        or other string

        :type: str
        """
        return self._type_field

    @property
    def description(self) -> str:
        return self._description

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def characters(self) -> List[EmojiCharacter]:
        """Emoji character objects list which makes up the Emoji Sequence

        :type: List[EmojiCharacter]
        """
        return self._characters

    @property
    def hex(self) -> str:
        """Return code points in hex format string, separated by spaces"""
        return " ".join(c.hex for c in self._characters)

    @property
    def string(self) -> str:
        """string of the Emoji Sequence

        :type: str
        """
        return self._string

    @property
    def regex(self) -> str:
        """Regular express of the Emoji Sequence

        :type: str
        """
        return self._regex

    @property
    def regex_compiled(self):
        """Compiled regular express pattern of the Emoji Sequence"""
        return self._regex_compiled

    @property
    def code_points(self) -> List[int]:
        """List of unicode integer value of the characters who make up Emoji Sequence

        :type: List[int]
        """
        return self._code_points

    @classmethod
    def find_all(cls, s: str) -> List[Tuple["EmojiSequence", int, int]]:
        """Find out all emoji sequences in a string, and return them in a list

        Item of the list is same as :meth:`find`
        """
        return list(cls.find(s))

    @classmethod
    def find(cls, s: str) -> Iterable[Tuple["EmojiSequence", int, int]]:
        """Return an iterator which yields all emoji sequences in a string, without actually storing them all simultaneously.

        Item of the iterator is a 3-member tuple:

        #. ``0``: The found :class:`.EmojiSequence` object
        #. ``1``: Begin position of the emoji sequence string
        #. ``2``: End position of the emoji sequence string
        """
        m = cls.pattern.search(s)
        while m:
            yield cls.from_string(m.group()), m.start(), m.end()
            m = cls.pattern.search(s, m.end())


EmojiSequence.initial()

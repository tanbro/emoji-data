import os
import re
from typing import Union, List, Iterable

from pkg_resources import Requirement, resource_stream

from . import version
from .character import EmojiCharacter
from .types import BaseDictContainer
from .utils import read_data_file_iterable

__all__ = ['EmojiSequence']

PACKAGE = '.'.join(version.__name__.split('.')[:-1])

DATA_FILE_HANDLES = [
    resource_stream(Requirement.parse(PACKAGE), os.path.join(*(PACKAGE.split('.') + ['data', s])))
    for s in ('emoji-zwj-sequences.txt', 'emoji-sequences.txt', 'emoji-variation-sequences.txt')
]


class _MetaClass(BaseDictContainer):
    pass


class EmojiSequence(metaclass=_MetaClass):
    """Emoji and Text Presentation Sequences used to represent emoji

    see: http://www.unicode.org/reports/tr51/#Emoji_Variation_Sequences
    """

    def __init__(self,
                 code_points: Union[Iterable[int], int],
                 type_field: str = '',
                 description: str = '',
                 comment: str = ''):
        if isinstance(code_points, Iterable):
            self._code_points = list(code_points)
        else:
            self._code_points = [code_points]
        self._string = ''.join(chr(n) for n in self._code_points)
        self._characters = [EmojiCharacter.from_hex(n) for n in self._code_points]
        self._type_field = type_field.strip()
        self._comment = comment.strip()
        self._description = description
        # regex
        self._regex = r''
        # TODO: S(SelectorKeycap|Selector)?
        # 这样的形式： [数字*#] + selector + keycap, 此时 seq, seq + selector 都是合理的 unqualified 格式！
        # if self._codepoints[-1] in (EMOJI_PRESENTATION_SELECTOR, TEXT_PRESENTATION_SELECTOR):
        #     if not all(not EmojiCharacter.is_emoji_character(cp) for cp in self._codepoints[:-1]):
        #         self._regex = r'{}({})?'.format(
        #             ''.join(m.regex for m in self._characters[:-1]),
        #             self._characters[-1].regex
        #         )
        if not self._regex:
            self._regex = ''.join(m.regex for m in self._characters)
        self._regex_compiled = re.compile(self._regex)

    def __str__(self):
        return self._string

    def __repr__(self):
        return '<{} codes={} text={!r}>'.format(
            type(self).__name__,
            self._code_points,
            self._string,
        )

    _initialed = False
    pattern = None
    """Compiled regular express pattern object for all-together Emoji sequences.
    """

    @classmethod
    def initial(cls):
        """Initial the class

        Load Emoji Characters and there properties, the sequences from package data file into class internal dictionary

        .. note:: **MUST** call this before other operations on the class
        """
        if cls._initialed:
            return
        EmojiCharacter.initial()
        for file_index, handle in enumerate(DATA_FILE_HANDLES):
            for content, comment in read_data_file_iterable(handle):
                if not content:
                    continue
                cps, type_field, description = (part.strip() for part in content.split(';', 2))
                # codes ...
                cps_parts = cps.split('..', 1)  # begin..end form
                if len(cps_parts) > 1:  # A range of single char emoji-seq
                    for cp in range(int(cps_parts[0], 16), 1 + int(cps_parts[1], 16)):  # pylint:disable=invalid-name
                        inst = cls(cp, type_field, description, comment)
                        if inst.string not in cls:
                            cls[inst.string] = inst
                else:
                    code_points = [int(cp, 16) for cp in cps.split()]
                    inst = cls(code_points, type_field, description, comment)
                    if inst.string not in cls:
                        cls[inst.string] = inst
        # build regex
        seqs = sorted((m for _, m in cls), key=lambda x: len(x.codepoints), reverse=True)  # type: List[EmojiSequence]
        exp = r'|'.join(m.regex for m in seqs)
        pat = re.compile(exp)
        cls.pattern = pat
        # initialed OK
        cls._initialed = True

    @classmethod
    def from_text(cls, text):  # type: (str)->EmojiSequence
        """Get an :class:`EmojiSequence` instance by text

        :param text: Pass-in text
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiSequence
        :raises RuntimeError: When non-emoji character in text
        :raises KeyError: When passed-in value not found in the class' internal dictionary
        """
        text = text.strip()
        if not all(ord(s) in EmojiCharacter for s in text):
            raise RuntimeError('Not all characters in the text is Emoji character.')
        try:
            return cls[text]
        except KeyError:
            raise KeyError('[{}]({!r})'.format(' '.join(hex(ord(c)).upper() for c in text), text))

    @classmethod
    def from_characters(cls, characters):  # type: (Iterable[EmojiCharacter])->EmojiSequence
        """Get an :class:`EmojiSequence` instance by :class:`EmojiCharacter` object or list

        :param Iterable[EmojiCharacter] characters: Pass-in object or list/iterable
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiSequence
        :raises KeyError: When passed-in value not found in the class' internal dictionary
        """
        text = ''.join(m.string for m in characters)
        return cls.from_text(text)

    @classmethod
    def from_codepoints(cls, values):  # type: (Iterable[int])->EmojiSequence
        """Get an :class:`EmojiSequence` instance by a list of unicode integer value

        :param Iterable[int] values: List of code points
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiSequence
        :raises KeyError: When passed-in value not found in the class' internal dictionary
        """
        text = ''.join(EmojiCharacter.from_hex(m).string for m in values)
        return cls.from_text(text)

    @classmethod
    def from_hex(cls, *args):  # type: (Union[str, int, Iterable[str], Iterable[int]])->EmojiSequence
        """Get an :class:`EmojiSequence` instance by a **space separated** unicode hex string

        :param Union[str, Iterable[str]] args: Hex string(s)

            *. When ONLY ONE args passed in, it could be:
              *. A **space separated** hex string
              *. A single unicode code-point integer
              *. An iterable object with single unicode's hex string as it's members
              *. An iterable object with single unicode's code-point integer as it's members
            *. When MORE THAN ONE args passed in, every member of args could be:
              *. A single unicode's hex string
              *. A single unicode's integer value

        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiSequence

        :raises KeyError: When passed-in value not found in the class' internal dictionary
        """
        if len(args) == 1:
            arg0 = args[0]
            if isinstance(arg0, str):
                args = arg0.split()
            elif isinstance(arg0, int):
                args = [arg0]
            elif isinstance(arg0, Iterable):
                args = arg0
            else:
                raise TypeError(
                    'The single `args` should be `str`, `int`, `Iterable[str]`, `Iterable[int]`'
                )
        return cls.from_characters(EmojiCharacter.from_hex(m) for m in args)

    @property
    def type_field(self):
        return self._type_field

    @property
    def description(self):
        return self._description

    @property
    def comment(self):
        return self._comment

    @property
    def characters(self) -> List[EmojiCharacter]:
        """Emoji character objects list which makes up the Emoji Sequence

        :type: List[EmojiCharacter]
        """
        return self._characters

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
        """Compiled regular express pattern of the Emoji Sequence
        """
        return self._regex_compiled

    @property
    def codepoints(self) -> List[int]:
        """List of unicode integer value of the characters who make up Emoji Sequence

        :type: List[int]
        """
        return self._code_points

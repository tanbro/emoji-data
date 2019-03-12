import os
import re
from typing import Union, List, Iterable

from pkg_resources import Requirement, resource_stream

from . import version
from .character import EmojiCharacter
from .utils import BaseDictContainer, preproc_line_data

__all__ = ['EmojiSequence']

PACKAGE = '.'.join(version.__name__.split('.')[:-1])
SEQUENCES_DATAFILE_STREAM = resource_stream(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-sequences.txt']))
)
ZWJ_SEQUENCES_DATAFILE_STREAM = resource_stream(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-zwj-sequences.txt']))
)


class _MetaClass(BaseDictContainer):
    pass


class EmojiSequence(metaclass=_MetaClass):
    """Emoji and Text Presentation Sequences used to represent emoji

    see: http://www.unicode.org/reports/tr51/#Emoji_Variation_Sequences
    """

    def __init__(self, chars: Union[Iterable[EmojiCharacter], EmojiCharacter], type_: str = '', desc: str = ''):
        if isinstance(chars, Iterable):
            self._chars = list(chars)
        else:
            self._chars = [chars]
        self._type = type_.strip()
        self._desc = desc.strip()
        #
        self._codes = [m.code for m in self._chars]
        self._string = ''.join(m.string for m in self._chars)
        self._regex = ''.join(m.regex for m in self._chars)
        self._regex_compiled = re.compile(self._regex)

    def __str__(self):
        return self._string

    def __repr__(self):
        return '<{} codes={} text={!r}>'.format(
            type(self).__name__,
            self._codes,
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
        for fp in SEQUENCES_DATAFILE_STREAM, ZWJ_SEQUENCES_DATAFILE_STREAM:
            for data in fp:  # type: bytes
                line = preproc_line_data(data)
                if not line:
                    continue
                code_points, type_field, description = (part.strip() for part in line.split(';', 2))
                # codes ...
                code_points_parts = code_points.split('..', 1)  # begin..end form
                if len(code_points_parts) > 1:
                    for code in range(int(code_points_parts[0], 16), 1 + int(code_points_parts[1], 16)):
                        inst = cls(EmojiCharacter.from_code(code), type_field, description)
                        cls[inst.string] = inst
                else:
                    chars = (EmojiCharacter.from_code(code) for code in (int(s, 16) for s in code_points.split()))
                    inst = cls(chars, type_field, description)
                    cls[inst.string] = inst
        # build regex
        seqs = sorted((m for _, m in cls), key=lambda x: len(x.codes), reverse=True)  # type: List[EmojiSequence]
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
    def from_codes(cls, codes):  # type: (Iterable[int])->EmojiSequence
        """Get an :class:`EmojiSequence` instance by a list of unicode integer value

        :param Iterable[int] codes: Pass-in int list
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiSequence
        :raises KeyError: When passed-in value not found in the class' internal dictionary
        """
        text = ''.join(EmojiCharacter.from_code(m).string for m in codes)
        return cls.from_text(text)

    @classmethod
    def from_hexes(cls, hexes):  # type: (Iterable[str])->EmojiSequence
        """Get an :class:`EmojiSequence` instance by a list of unicode hex express

        :param Iterable[str] hexes: Pass-in int list
        :return: Instance returned from the class's internal dictionary
        :rtype: EmojiSequence
        :raises KeyError: When passed-in value not found in the class' internal dictionary
        """
        text = ''.join(EmojiCharacter.from_hex(m).string for m in hexes)
        return cls.from_text(text)

    @property
    def chars(self) -> List[EmojiCharacter]:
        """Emoji character objects list which makes up the Emoji Sequence

        :type: List[EmojiCharacter]
        """
        return self._chars

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
    def codes(self) -> List[int]:
        """List of unicode integer value of the characters who make up Emoji Sequence

        :type: List[int]
        """
        return self._codes

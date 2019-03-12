"""Other sequences used to represent emoji
"""

import os
import re
import typing as t

from pkg_resources import Requirement, resource_stream

from . import version
from .character import EmojiCharacter

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

TRePattern = type(re.compile(r''))


class _MetaClass(type):
    def __new__(cls, name, bases, attrs):
        cls._data = dict()
        return super().__new__(cls, name, bases, attrs)

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


class EmojiSequence(metaclass=_MetaClass):
    def __init__(self, chars: t.Union[t.Iterable[EmojiCharacter], EmojiCharacter], type_: str = '', desc: str = ''):
        if isinstance(chars, t.Iterable):
            self._chars = list(chars)
        else:
            self._chars = [chars]
        self._type = type_.strip()
        self._desc = desc.strip()
        #
        self._codes = [m.code for m in self._chars]
        self._text = ''.join(m.string for m in self._chars)
        self._regex = ''.join(m.regex for m in self._chars)
        self._regex_compiled = re.compile(self._regex)

    def __str__(self):
        return self._text

    def __repr__(self):
        return '<{} codes={} text={!r}>'.format(
            type(self).__name__,
            self._codes,
            self._text,
        )

    _initialed = False
    pattern = None  # type: TRePattern
    """Regular express pattern object for all-together Emoji sequences.
    """

    @classmethod
    def initial(cls):
        """

        :return:
        """
        if cls._initialed:
            return
        EmojiCharacter.initial()
        for ss in SEQUENCES_DATAFILE_STREAM, ZWJ_SEQUENCES_DATAFILE_STREAM:
            for byte_string in ss:  # type: bytes
                byte_string = byte_string.strip()
                if not byte_string:
                    continue
                if byte_string[0] in b'#;':
                    continue
                line = byte_string.decode('utf-8')  # type: str
                line = line.split('#', 1)[0].strip()
                code_points, type_field, description = (part.strip() for part in line.split(';', 2))
                # codes ...
                code_points_parts = code_points.split('..', 1)  # begin..end form
                if len(code_points_parts) > 1:
                    for code in range(int(code_points_parts[0], 16), 1 + int(code_points_parts[1], 16)):
                        inst = cls(EmojiCharacter.from_code(code), type_field, description)
                        cls[inst._text] = inst
                else:
                    chars = (EmojiCharacter.from_code(code) for code in (int(s, 16) for s in code_points.split()))
                    inst = cls(chars, type_field, description)
                    cls[inst._text] = inst
        # build regex
        seqs = sorted((m for _, m in cls), key=lambda x: len(x.codes), reverse=True)  # type: t.List[EmojiSequence]
        exp = r'|'.join(m.regex for m in seqs)
        pat = re.compile(exp)
        cls.pattern = pat
        # initialed OK
        cls._initialed = True

    @classmethod
    def from_text(cls, text):  # type: (str)->EmojiSequence
        text = text.strip()
        if not all(ord(s) in EmojiCharacter for s in text):
            raise RuntimeError('Not all characters in the text is Emoji character.')
        try:
            return cls[text]
        except KeyError:
            raise KeyError('[{}]({!r})'.format(' '.join(hex(ord(c)).upper() for c in text), text))

    @classmethod
    def from_characters(cls, characters):  # type: (t.List[EmojiCharacter])->EmojiSequence
        text = ''.join(m.string for m in characters)
        return cls.from_text(text)

    @classmethod
    def from_codes(cls, codes):  # type: (t.Iterable[int])->EmojiSequence
        text = ''.join(EmojiCharacter.from_code(m).string for m in codes)
        return cls.from_text(text)

    @classmethod
    def from_hexes(cls, hexes):  # type: (t.Iterable[str])->EmojiSequence
        text = ''.join(EmojiCharacter.from_hex(m).string for m in hexes)
        return cls.from_text(text)

    @property
    def chars(self) -> t.List[EmojiCharacter]:
        return self._chars

    @property
    def text(self) -> str:
        return self._text

    @property
    def regex(self) -> str:
        return self._regex

    @property
    def regex_compiled(self):
        return self._regex_compiled

    @property
    def codes(self) -> t.List[int]:
        return self._codes

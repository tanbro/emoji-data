import os
import re
from typing import Dict, Iterable, List, Tuple, Union

from pkg_resources import Requirement, resource_filename

from . import version
from .character import EmojiCharacter
from .types import BaseDictContainer
from .utils import read_data_file_iterable

__all__ = ['EmojiSequence']

PACKAGE = '.'.join(version.__name__.split('.')[:-1])


def _get_data_file_name(name):
    return resource_filename(
        Requirement.parse(PACKAGE),
        os.path.join(*(PACKAGE.split('.') + ['data', name]))
    )


DATA_FILES = {
    'zwj-sequences': _get_data_file_name('emoji-zwj-sequences.txt'),
    'sequences': _get_data_file_name('emoji-sequences.txt'),
    'variation-sequences': _get_data_file_name('emoji-variation-sequences.txt'),
    'test': _get_data_file_name('emoji-test.txt')
}  # type: Dict[str, str]


class _MetaClass(BaseDictContainer):
    pass


class EmojiSequence(metaclass=_MetaClass):
    """Emoji and Text Presentation Sequences used to represent emoji

    see: http://www.unicode.org/reports/tr51/#Emoji_Variation_Sequences
    """

    def __init__(self,
                 code_points: Union[Iterable[int], int],
                 status: str = '',
                 type_field: str = '',
                 description: str = '',
                 comment: str = ''):
        if isinstance(code_points, Iterable):
            self._code_points = list(code_points)
        else:
            self._code_points = [code_points]
        self._status = status.strip()
        self._string = ''.join(chr(n) for n in self._code_points)
        self._characters = [EmojiCharacter.from_hex(n) for n in self._code_points]
        self._type_field = type_field.strip()
        self._comment = comment.strip()
        self._description = description
        # regex
        self._regex = r''
        if not self._regex:
            self._regex = ''.join(m.regex for m in self._characters)
        self._regex_compiled = re.compile(self._regex)

    def __len__(self):
        return len(self._code_points)

    def __str__(self):
        return self._string

    def __repr__(self):
        return '<{} code_points={!r} status={!r}, string={!r}, description={!r}>'.format(
            type(self).__qualname__,
            ' '.join('{:04X}'.format(n) for n in self._code_points),
            self._status,
            self._string,
            self._description
        )

    _initialed = False

    pattern = re.compile(r'')
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
        for data_name, data_file in DATA_FILES.items():
            with open(data_file, encoding='utf8') as fp:
                for content, comment in read_data_file_iterable(fp):
                    if data_name == 'test':
                        cps, status = (part.strip() for part in content.split(';', 1))
                        code_points = [int(cp, 16) for cp in cps.split()]
                        inst = cls(code_points, status=status, comment=comment)
                        s = inst.string
                        try:
                            existed_inst = cls[s]
                        except KeyError:
                            cls[s] = inst
                        else:
                            existed_inst.status = status
                    else:
                        cps, type_field, description = (part.strip() for part in content.split(';', 2))
                        # codes ...
                        try:
                            cp_head, cp_tail = cps.split('..', 1)  # begin..end form
                        except ValueError:
                            code_points = [int(cp, 16) for cp in cps.split()]
                            inst = cls(code_points, type_field, '', description, comment)  # type: EmojiSequence
                            text = inst.string
                            if text not in cls:
                                cls[text] = inst
                        else:
                            # A range of single char emoji-seq
                            for cp in range(int(cp_head, 16), 1 + int(cp_tail, 16)):
                                inst = cls(cp, type_field, '', description, comment)  # type: EmojiSequence
                                if inst.string not in cls:
                                    cls[inst.string] = inst
        # build regex
        ordered_list = sorted((m for m in cls.values()), key=lambda x: len(x.code_points), reverse=True)
        exp = r'|'.join(m.regex for m in ordered_list)
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
    def items(cls):  # type: ()->Iterable[Tuple[str, EmojiSequence]]
        """Return an iterator of all string -> emoji-sequence pairs of the class
        """
        return ((k, cls[k]) for k in cls)

    @classmethod
    def values(cls):  # type: ()->Iterable[EmojiSequence]
        """Return an iterator of all emoji-sequences of the class
        """
        return (cls[k] for k in cls)

    @classmethod
    def from_text(cls, value):  # type: (str)->EmojiSequence
        """Get an :class:`EmojiSequence` instance by text

        :param str value: Emoji string
        :return: Instance from internal dictionary
        :rtype: EmojiSequence
        :raises RuntimeError: When non-emoji character in text
        :raises KeyError: When passed-in value not found in internal dictionary
        """
        value = value.strip()
        if not all(ord(s) in EmojiCharacter for s in value):
            raise RuntimeError('Not all characters in the text is Emoji character.')
        try:
            return cls[value]
        except KeyError:
            code_points_text = ' '.join('{:04X}'.format(ord(c)) for c in value)
            raise KeyError('[{}]({!r})'.format(code_points_text, value))

    @classmethod
    def from_emoji_character(cls, value):  # type: (Union[EmojiCharacter, Iterable[EmojiCharacter]])->EmojiSequence
        """Get an :class:`EmojiSequence` instance by :class:`EmojiCharacter` object or list

        :param value: Single or iterable object of :class:`EmojiCharacter`, composing the sequence
        :return: Instance from internal dictionary
        :rtype: EmojiSequence
        :raises KeyError: When passed-in value not found in internal dictionary
        """
        if isinstance(value, EmojiCharacter):
            s = value.string
        elif isinstance(value, Iterable):
            s = ''.join(m.string for m in value)
        else:
            raise TypeError('Argument `value` must be one of `EmojiCharacter` or `Iterable[EmojiCharacter]`')
        return cls.from_text(s)

    @classmethod
    def from_hex(cls, value):  # type: (Union[str, int, Iterable[str], Iterable[int]])->EmojiSequence
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

        :raises KeyError: When passed-in value not found in the class' internal dictionary
        """
        cps_list = list()  # type: Iterable[str] | Iterable[int]
        if isinstance(value, str):
            cps_list = value.split()
        elif isinstance(value, int):
            cps_list = [value]
        elif isinstance(value, Iterable):
            cps_list = value
        else:
            raise TypeError(
                'The `args` should be one of `str`, `int`, or a sequence of that'
            )
        return cls.from_emoji_character(EmojiCharacter.from_hex(cp) for cp in cps_list)

    @property
    def type_field(self) -> str:
        """A convenience for parsing the emoji sequence files, and is not intended to be maintained as a property.

        one of the following:

        - `"Basic_Emoji"`
        - `"Emoji_Keycap_Sequence"`
        - `"Emoji_Flag_Sequence"`
        - `"Emoji_Tag_Sequence"`
        - `"Emoji_Modifier_Sequence"`

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
    def code_points(self) -> List[int]:
        """List of unicode integer value of the characters who make up Emoji Sequence

        :type: List[int]
        """
        return self._code_points

    @classmethod
    def find(cls, s):  # type: (str) ->  List[Tuple[EmojiSequence, int, int]]
        """Finds out all emoji sequences in a string, and return them in a list
        """
        return list(cls.iter_find(s))

    @classmethod
    def iter_find(cls, s):  # type: (str) ->  Iterable[Tuple[EmojiSequence, int, int]]
        """Return an iterator which yields all emoji sequences in a string, without actually storing them all simultaneously.

        Item of the iterator is a 3-member tuple:

        #. ``0``: The found :class:`.EmojiSequence` object
        #. ``1``: Begin position of the emoji sequence string
        #. ``2``: End position of the emoji sequence string
        """
        m = cls.pattern.search(s)
        while m:
            yield cls.from_text(m.group()), m.start(), m.end()
            m = cls.pattern.search(s, m.end())


EmojiSequence.initial()

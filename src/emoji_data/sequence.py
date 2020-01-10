import os
import re
from typing import Dict, Iterable, List, Union

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


class EmojiSequence(metaclass=_MetaClass):  # pylint: disable=too-many-instance-attributes,too-many-arguments
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
    pattern = None
    """Compiled regular express pattern object for all-together Emoji sequences.
    """

    @classmethod
    def initial(cls):  # pylint:disable=too-many-locals
        """Initial the class

        Load Emoji Sequences from package data file into class internal dictionary
        """
        if cls._initialed:
            return
        EmojiCharacter.initial()
        for data_name, data_file in DATA_FILES.items():
            with open(data_file, encoding='utf-8') as fp:
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
                            for cp in range(int(cp_head, 16), 1 + int(cp_tail, 16)):  # pylint:disable=invalid-name
                                inst = cls(cp, type_field, '', description, comment)  # type: EmojiSequence
                                if inst.string not in cls:
                                    cls[inst.string] = inst
        # build regex
        seqs = sorted((m for _, m in cls), key=lambda x: len(x.code_points), reverse=True)  # type: List[EmojiSequence]
        exp = r'|'.join(m.regex for m in seqs)
        pat = re.compile(exp)
        cls.pattern = pat
        # initialed OK
        cls._initialed = True

    @classmethod
    def from_text(cls, text):  # type: (str)->EmojiSequence
        """Get an :class:`EmojiSequence` instance by text

        :param str text: Emoji string
        :return: Instance from internal dictionary
        :rtype: EmojiSequence
        :raises RuntimeError: When non-emoji character in text
        :raises KeyError: When passed-in value not found in internal dictionary
        """
        text = text.strip()
        if not all(ord(s) in EmojiCharacter for s in text):
            raise RuntimeError('Not all characters in the text is Emoji character.')
        try:
            return cls[text]
        except KeyError:
            code_points_text = ' '.join('{:04X}'.format(ord(c)) for c in text)
            raise KeyError('[{}]({!r})'.format(code_points_text, text))

    @classmethod
    def from_characters(cls, characters):  # type: (Iterable[EmojiCharacter])->EmojiSequence
        """Get an :class:`EmojiSequence` instance by :class:`EmojiCharacter` object or list

        :param Iterable[EmojiCharacter] characters: Single or iterable object of :class:`EmojiCharacter`, composing the sequence
        :return: Instance from internal dictionary
        :rtype: EmojiSequence
        :raises KeyError: When passed-in value not found in internal dictionary
        """
        text = ''.join(m.string for m in characters)
        return cls.from_text(text)

    @classmethod
    def from_hex(cls, *args):  # type: (Union[str, int, Iterable[str], Iterable[int]])->EmojiSequence
        """Get an :class:`EmojiSequence` instance by unicode code point(s)

        :param Union[str,Iterable[str]] args: Hex string(s)

            - When ONLY ONE args passed in, it could be:

              - one or more code points in hex format string, separated by spaces
              - one code point integer
              - An iterable object whose members are code point in hex format string
              - An iterable object whose members are code point integer

            - When MORE THAN ONE args passed in, every member of args could be:

              - one code point in hex format string
              - one code point integer

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
    def description(self):
        return self._description

    @property
    def comment(self):
        return self._comment

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
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


EmojiSequence.initial()

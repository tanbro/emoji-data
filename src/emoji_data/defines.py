"""Regular express for Emoji Definitions

see: http://www.unicode.org/reports/tr51/#Definitions
"""

import re
from enum import Enum

from .character import (EMOJI_KEYCAP, EMOJI_PRESENTATION_SELECTOR,
                        REGIONAL_INDICATORS, TAGS, TEXT_PRESENTATION_SELECTOR,
                        ZWJ, EmojiCharacter, EmojiCharProperty)
from .utils import code_point_to_regex

__all__ = ['EMOJI_PATTERNS', 'QualifiedType', 'detect_qualified',
           'is_default_emoji_presentation_character', 'is_default_text_presentation_character',
           'is_emoji_character', 'is_emoji_core_sequence', 'is_emoji_flag_sequence', 'is_emoji_keycap_sequence',
           'is_emoji_modifier', 'is_emoji_modifier_base', 'is_emoji_modifier_sequence',
           'is_emoji_presentation_selector', 'is_emoji_presentation_sequence', 'is_emoji_sequence',
           'is_emoji_tag_sequence', 'is_emoji_zwj_element', 'is_emoji_zwj_sequence', 'is_regional_indicator',
           'is_tag_base', 'is_tag_spec', 'is_tag_term', 'is_text_presentation_selector',
           'is_text_presentation_sequence', 'is_qualified_emoji_character']


class QualifiedType(Enum):
    FULLY_QUALIFIED = 'fully-qualified'
    MINIMALLY_QUALIFIED = 'minimally-qualified'
    UNQUALIFIED = 'unqualified'


RX_EMOJI_CHARACTER = r'[{0}]'.format(''.join(m.regex for _, m in EmojiCharacter))

RX_DEFAULT_EMOJI_PRESENTATION_CHARACTER = r'[{0}]'.format(
    ''.join(
        m.regex for _, m in EmojiCharacter
        if EmojiCharProperty.EPRES in m.properties
    )
)

RX_DEFAULT_TEXT_PRESENTATION_CHARACTER = r'[{0}]'.format(
    ''.join(
        m.regex for _, m in EmojiCharacter
        if EmojiCharProperty.EPRES not in m.properties
    )
)

RX_TEXT_PRESENTATION_SELECTOR = r'{0}'.format(code_point_to_regex(TEXT_PRESENTATION_SELECTOR))

RX_TEXT_PRESENTATION_SEQUENCE = r'({0}{1})'.format(RX_EMOJI_CHARACTER, TEXT_PRESENTATION_SELECTOR)

RX_EMOJI_PRESENTATION_SELECTOR = r'{0}'.format(code_point_to_regex(EMOJI_PRESENTATION_SELECTOR))

RX_EMOJI_PRESENTATION_SEQUENCE = r'({}{})'.format(RX_EMOJI_CHARACTER, EMOJI_PRESENTATION_SELECTOR)

RX_EMOJI_MODIFIER = r'[{}]'.format(
    ''.join(
        m.regex for _, m in EmojiCharacter
        if EmojiCharProperty.EMOD in m.properties
    )
)

RX_EMOJI_MODIFIER_BASE = r'[{}]'.format(
    ''.join(
        m.regex for _, m in EmojiCharacter
        if EmojiCharProperty.EBASE in m.properties
    )
)

RX_EMOJI_MODIFIER_SEQUENCE = r'({}{})'.format(RX_EMOJI_MODIFIER_BASE, RX_EMOJI_MODIFIER)

RX_REGIONAL_INDICATOR = r'[{}-{}]'.format(
    *(code_point_to_regex(n) for n in (REGIONAL_INDICATORS[0], REGIONAL_INDICATORS[-1]))
)

RX_EMOJI_FLAG_SEQUENCE = r'({0}{0})'.format(RX_REGIONAL_INDICATOR)

RX_TAG_BASE = r'({}|{}|{})'.format(RX_EMOJI_CHARACTER, RX_EMOJI_MODIFIER_SEQUENCE, RX_EMOJI_PRESENTATION_SEQUENCE)

RX_TAG_SPEC = r'[{}-{}]'.format(*(code_point_to_regex(n) for n in (TAGS[0], TAGS[-2])))

RX_TAG_TERM = r'{}'.format(code_point_to_regex(TAGS[-1]))

RX_EMOJI_TAG_SEQUENCE = r'({}{}{})'.format(RX_TAG_BASE, RX_TAG_SPEC, RX_TAG_TERM)

RX_EMOJI_KEYCAP_SEQUENCE = r'([0-9#*]{}{})'.format(
    *(code_point_to_regex(n) for n in (EMOJI_PRESENTATION_SELECTOR, EMOJI_KEYCAP))
)

RX_EMOJI_CORE_SEQUENCE = r'({}|{}|{}|{}|{})'.format(
    RX_EMOJI_CHARACTER, RX_EMOJI_PRESENTATION_SEQUENCE, RX_EMOJI_KEYCAP_SEQUENCE, RX_EMOJI_MODIFIER_SEQUENCE, RX_EMOJI_FLAG_SEQUENCE
)

RX_EMOJI_ZWJ_ELEMENT = r'({}|{}|{})'.format(
    RX_EMOJI_CHARACTER, RX_EMOJI_PRESENTATION_SEQUENCE, RX_EMOJI_MODIFIER_SEQUENCE
)

RX_EMOJI_ZWJ_SEQUENCE = r'({0}({1}{0})+)'.format(
    RX_EMOJI_ZWJ_ELEMENT, code_point_to_regex(ZWJ)
)

RX_EMOJI_SEQUENCE = r'({}|{}|{})'.format(
    RX_EMOJI_CORE_SEQUENCE, RX_EMOJI_ZWJ_SEQUENCE, RX_EMOJI_TAG_SEQUENCE
)

EMOJI_PATTERNS = {
    'EMOJI_CHARACTER': re.compile(RX_EMOJI_CHARACTER),
    'DEFAULT_EMOJI_PRESENTATION_CHARACTER': re.compile(RX_DEFAULT_EMOJI_PRESENTATION_CHARACTER),
    'DEFAULT_TEXT_PRESENTATION_CHARACTER': re.compile(RX_DEFAULT_TEXT_PRESENTATION_CHARACTER),
    'TEXT_PRESENTATION_SELECTOR': re.compile(RX_TEXT_PRESENTATION_SELECTOR),
    'TEXT_PRESENTATION_SEQUENCE': re.compile(RX_TEXT_PRESENTATION_SEQUENCE),
    'EMOJI_PRESENTATION_SELECTOR': re.compile(RX_EMOJI_PRESENTATION_SELECTOR),
    'EMOJI_PRESENTATION_SEQUENCE': re.compile(RX_EMOJI_PRESENTATION_SEQUENCE),
    'EMOJI_MODIFIER': re.compile(RX_EMOJI_MODIFIER),
    'EMOJI_MODIFIER_BASE': re.compile(RX_EMOJI_MODIFIER_BASE),
    'EMOJI_MODIFIER_SEQUENCE': re.compile(RX_EMOJI_MODIFIER_SEQUENCE),
    'REGIONAL_INDICATOR': re.compile(RX_REGIONAL_INDICATOR),
    'EMOJI_FLAG_SEQUENCE': re.compile(RX_EMOJI_FLAG_SEQUENCE),
    'TAG_BASE': re.compile(RX_TAG_BASE),
    'TAG_SPEC': re.compile(RX_TAG_SPEC),
    'TAG_TERM': re.compile(RX_TAG_TERM),
    'EMOJI_TAG_SEQUENCE': re.compile(RX_EMOJI_TAG_SEQUENCE),
    'EMOJI_KEYCAP_SEQUENCE': re.compile(RX_EMOJI_KEYCAP_SEQUENCE),
    'EMOJI_CORE_SEQUENCE': re.compile(RX_EMOJI_CORE_SEQUENCE),
    'EMOJI_ZWJ_ELEMENT': re.compile(RX_EMOJI_ZWJ_ELEMENT),
    'EMOJI_ZWJ_SEQUENCE': re.compile(RX_EMOJI_ZWJ_SEQUENCE),
    'EMOJI_SEQUENCE': re.compile(RX_EMOJI_SEQUENCE)
}


def is_emoji_character(c: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_CHARACTER'].fullmatch(c) is not None


def is_default_emoji_presentation_character(c: str) -> bool:
    return EMOJI_PATTERNS['DEFAULT_EMOJI_PRESENTATION_CHARACTER'].fullmatch(c) is not None


def is_default_text_presentation_character(c: str) -> bool:
    return EMOJI_PATTERNS['DEFAULT_TEXT_PRESENTATION_CHARACTER'].fullmatch(c) is not None


def is_text_presentation_selector(c: str) -> bool:
    return EMOJI_PATTERNS['TEXT_PRESENTATION_SELECTOR'].fullmatch(c) is not None


def is_text_presentation_sequence(s: str) -> bool:
    return EMOJI_PATTERNS['TEXT_PRESENTATION_SEQUENCE'].fullmatch(s) is not None


def is_emoji_presentation_selector(c: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_PRESENTATION_SELECTOR'].fullmatch(c) is not None


def is_emoji_presentation_sequence(s: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_PRESENTATION_SEQUENCE'].fullmatch(s) is not None


def is_emoji_modifier(c: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_MODIFIER'].fullmatch(c) is not None


def is_emoji_modifier_base(c: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_MODIFIER_BASE'].fullmatch(c) is not None


def is_emoji_modifier_sequence(s: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_MODIFIER_SEQUENCE'].fullmatch(s) is not None


def is_regional_indicator(s: str) -> bool:
    return EMOJI_PATTERNS['REGIONAL_INDICATOR'].fullmatch(s) is not None


def is_emoji_flag_sequence(s: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_FLAG_SEQUENCE'].fullmatch(s) is not None


def is_tag_base(s: str) -> bool:
    return EMOJI_PATTERNS['TAG_BASE'].fullmatch(s) is not None


def is_tag_spec(s: str) -> bool:
    return EMOJI_PATTERNS['TAG_SPEC'].fullmatch(s) is not None


def is_tag_term(c: str) -> bool:
    return EMOJI_PATTERNS['TAG_TERM'].fullmatch(c) is not None


def is_emoji_tag_sequence(s: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_TAG_SEQUENCE'].fullmatch(s) is not None


def is_emoji_keycap_sequence(s: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_KEYCAP_SEQUENCE'].fullmatch(s) is not None


def is_emoji_core_sequence(s: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_CORE_SEQUENCE'].fullmatch(s) is not None


def is_emoji_zwj_element(s: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_ZWJ_ELEMENT'].fullmatch(s) is not None


def is_emoji_zwj_sequence(s: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_ZWJ_SEQUENCE'].fullmatch(s) is not None


def is_emoji_sequence(s: str) -> bool:
    return EMOJI_PATTERNS['EMOJI_SEQUENCE'].fullmatch(s) is not None


def is_qualified_emoji_character(s: str, i: int) -> bool:
    """An emoji character in a string that

    - (a) has default emoji presentation or
    - (b) is the first character in an emoji modifier sequence or
    - (c) is not a default emoji presentation character, but is the first character in an emoji presentation sequence.

    :param str s: string
    :param int i: index of the character in the string to check if qualified
    :return: True of False
    :rtype: bool

    ref: http://www.unicode.org/reports/tr51/#def_qualified_emoji_character
    """
    c = s[i]
    if is_default_emoji_presentation_character(c):
        return True
    if EMOJI_PATTERNS['EMOJI_MODIFIER_SEQUENCE'].match(s[i:]):
        return True
    if EMOJI_PATTERNS['EMOJI_PRESENTATION_SEQUENCE'].match(s[i:]):
        return True
    return False


def detect_qualified(s: str) -> QualifiedType:
    s = s.strip()
    if not all(is_emoji_character(c) for c in s):
        raise ValueError('Not every character of `s` is Emoji character')
    if is_emoji_sequence(s):
        if all(is_qualified_emoji_character(s, i) for i, _ in enumerate(s)):
            return QualifiedType.FULLY_QUALIFIED
        if is_qualified_emoji_character(s, 0):
            return QualifiedType.MINIMALLY_QUALIFIED
    return QualifiedType.UNQUALIFIED

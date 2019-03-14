"""Regular express for Emoji Definitions

see: http://www.unicode.org/reports/tr51/#Definitions
"""
import re

from .character import (EmojiCharacter, EmojiCharProperty, TEXT_PRESENTATION_SELECTOR, EMOJI_PRESENTATION_SELECTOR,
                        REGIONAL_INDICATORS, TAGS, EMOJI_KEYCAP, ZWJ)
from .utils import code_point_to_regex

__all__ = ['patterns', 'is_default_emoji_presentation_character', 'is_default_text_presentation_character',
           'is_emoji_character', 'is_emoji_core_sequence', 'is_emoji_flag_sequence', 'is_emoji_keycap_sequence',
           'is_emoji_modifier', 'is_emoji_modifier_base', 'is_emoji_modifier_sequence',
           'is_emoji_presentation_selector', 'is_emoji_presentation_sequence', 'is_emoji_sequence',
           'is_emoji_tag_sequence', 'is_emoji_zwj_element', 'is_emoji_zwj_sequence', 'is_regional_indicator',
           'is_tag_base', 'is_tag_spec', 'is_tag_term', 'is_text_presentation_selector',
           'is_text_presentation_sequence']

emoji_character = r'[{0}]'.format(''.join(m.regex for m in EmojiCharacter))

default_emoji_presentation_character = r'[{0}]'.format(
    ''.join(
        m.regex for m in EmojiCharacter
        if EmojiCharProperty.EPRES in m.properties
    )
)

default_text_presentation_character = r'[{0}]'.format(
    ''.join(
        m.regex for m in EmojiCharacter
        if EmojiCharProperty.EPRES not in m.properties
    )
)

text_presentation_selector = r'{0}'.format(code_point_to_regex(TEXT_PRESENTATION_SELECTOR))

text_presentation_sequence = r'({0}{1})'.format(emoji_character, text_presentation_selector)

emoji_presentation_selector = r'{0}'.format(code_point_to_regex(EMOJI_PRESENTATION_SELECTOR))

emoji_presentation_sequence = r'({0}{1})'.format(emoji_character, emoji_presentation_selector)

emoji_modifier = r'[{0}]'.format(
    ''.join(
        m.regex for m in EmojiCharacter
        if EmojiCharProperty.EMOD in m.properties
    )
)

emoji_modifier_base = r'[{0}]'.format(
    ''.join(
        m.regex for m in EmojiCharacter
        if EmojiCharProperty.EBASE in m.properties
    )
)

emoji_modifier_sequence = r'({}{})'.format(emoji_modifier_base, emoji_modifier)

regional_indicator = r'[{0[0]}-{0[-1]}]'.format([code_point_to_regex(n) for n in REGIONAL_INDICATORS[0]])

emoji_flag_sequence = r'({0}{0})'.format(regional_indicator)

tag_base = r'({}|{}|{})'.format(emoji_character, emoji_modifier_sequence, emoji_presentation_sequence)

tag_spec = r'[{0[0]}-{0[-2]}]'.format([code_point_to_regex(n) for n in TAGS[0]])

tag_term = r'{0[-1]}'.format([code_point_to_regex(n) for n in TAGS[0]])

emoji_tag_sequence = r'({}{}{})'.format(tag_base, tag_spec, tag_term)

emoji_keycap_sequence = r'([0-9#*]{}{})'.format(EMOJI_PRESENTATION_SELECTOR, EMOJI_KEYCAP)

emoji_core_sequence = r'({}|{}|{}|{}|{})'.format(
    emoji_character, emoji_presentation_sequence, emoji_keycap_sequence, emoji_modifier_sequence, emoji_flag_sequence
)

emoji_zwj_element = r'({}|{}|{})'.format(
    emoji_character, emoji_presentation_sequence, emoji_modifier_sequence
)

emoji_zwj_sequence = r'({}{})+'.format(
    code_point_to_regex(ZWJ), emoji_zwj_element
)

emoji_sequence = r'({}|{}|{})'.format(
    emoji_core_sequence, emoji_zwj_sequence, emoji_tag_sequence
)

patterns = {
    'emoji_character': re.compile(emoji_character),
    'default_emoji_presentation_character': re.compile(default_emoji_presentation_character),
    'default_text_presentation_character': re.compile(default_text_presentation_character),
    'text_presentation_selector': re.compile(text_presentation_selector),
    'text_presentation_sequence': re.compile(text_presentation_sequence),
    'emoji_presentation_selector': re.compile(emoji_presentation_selector),
    'emoji_presentation_sequence': re.compile(emoji_presentation_sequence),
    'emoji_modifier': re.compile(emoji_modifier),
    'emoji_modifier_base': re.compile(emoji_modifier_base),
    'emoji_modifier_sequence': re.compile(emoji_modifier_sequence),
    'regional_indicator': re.compile(regional_indicator),
    'emoji_flag_sequence': re.compile(emoji_flag_sequence),
    'tag_base': re.compile(tag_base),
    'tag_spec': re.compile(tag_spec),
    'tag_term': re.compile(tag_term),
    'emoji_tag_sequence': re.compile(emoji_tag_sequence),
    'emoji_keycap_sequence': re.compile(emoji_keycap_sequence),
    'emoji_core_sequence': re.compile(emoji_core_sequence),
    'emoji_zwj_element': re.compile(emoji_zwj_element),
    'emoji_zwj_sequence': re.compile(emoji_zwj_sequence),
    'emoji_sequence': re.compile(emoji_sequence)
}


def is_emoji_character(s: str) -> bool:
    return patterns['emoji_character'].fullmatch(s) is not None


def is_default_emoji_presentation_character(s: str) -> bool:
    return patterns['default_emoji_presentation_character'].fullmatch(s) is not None


def is_default_text_presentation_character(s: str) -> bool:
    return patterns['default_text_presentation_character'].fullmatch(s) is not None


def is_text_presentation_selector(s: str) -> bool:
    return patterns['text_presentation_selector'].fullmatch(s) is not None


def is_text_presentation_sequence(s: str) -> bool:
    return patterns['text_presentation_sequence'].fullmatch(s) is not None


def is_emoji_presentation_selector(s: str) -> bool:
    return patterns['emoji_presentation_selector'].fullmatch(s) is not None


def is_emoji_presentation_sequence(s: str) -> bool:
    return patterns['emoji_presentation_sequence'].fullmatch(s) is not None


def is_emoji_modifier(s: str) -> bool:
    return patterns['emoji_modifier'].fullmatch(s) is not None


def is_emoji_modifier_base(s: str) -> bool:
    return patterns['emoji_modifier_base'].fullmatch(s) is not None


def is_emoji_modifier_sequence(s: str) -> bool:
    return patterns['emoji_modifier_sequence'].fullmatch(s) is not None


def is_regional_indicator(s: str) -> bool:
    return patterns['regional_indicator'].fullmatch(s) is not None


def is_emoji_flag_sequence(s: str) -> bool:
    return patterns['emoji_flag_sequence'].fullmatch(s) is not None


def is_tag_base(s: str) -> bool:
    return patterns['tag_base'].fullmatch(s) is not None


def is_tag_spec(s: str) -> bool:
    return patterns['tag_spec'].fullmatch(s) is not None


def is_tag_term(s: str) -> bool:
    return patterns['tag_term'].fullmatch(s) is not None


def is_emoji_tag_sequence(s: str) -> bool:
    return patterns['emoji_tag_sequence'].fullmatch(s) is not None


def is_emoji_keycap_sequence(s: str) -> bool:
    return patterns['emoji_keycap_sequence'].fullmatch(s) is not None


def is_emoji_core_sequence(s: str) -> bool:
    return patterns['emoji_core_sequence'].fullmatch(s) is not None


def is_emoji_zwj_element(s: str) -> bool:
    return patterns['emoji_zwj_element'].fullmatch(s) is not None


def is_emoji_zwj_sequence(s: str) -> bool:
    return patterns['emoji_zwj_sequence'].fullmatch(s) is not None


def is_emoji_sequence(s: str) -> bool:
    return patterns['emoji_sequence'].fullmatch(s) is not None

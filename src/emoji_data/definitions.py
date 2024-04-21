"""Regular expressions for Emoji Definitions

ref: http://www.unicode.org/reports/tr51/#Definitions
"""

import re
from enum import Enum
from typing import Pattern, Mapping, MutableMapping

from .character import (
    EMOJI_KEYCAP,
    EMOJI_PRESENTATION_SELECTOR,
    REGIONAL_INDICATORS,
    TAGS,
    TEXT_PRESENTATION_SELECTOR,
    ZWJ,
    EmojiCharacter,
    EmojiCharProperty,
)
from .utils import code_point_to_regex

__all__ = [
    "EMOJI_PATTERNS",
    "QualifiedType",
    "detect_qualified",
    "is_default_emoji_presentation_character",
    "is_default_text_presentation_character",
    "is_emoji_character",
    "is_emoji_core_sequence",
    "is_emoji_flag_sequence",
    "is_emoji_keycap_sequence",
    "is_emoji_modifier",
    "is_emoji_modifier_base",
    "is_emoji_modifier_sequence",
    "is_emoji_presentation_selector",
    "is_emoji_presentation_sequence",
    "is_emoji_sequence",
    "is_emoji_tag_sequence",
    "is_emoji_zwj_element",
    "is_emoji_zwj_sequence",
    "is_regional_indicator",
    "is_tag_base",
    "is_tag_spec",
    "is_tag_term",
    "is_text_presentation_selector",
    "is_text_presentation_sequence",
    "is_qualified_emoji_character",
]


class QualifiedType(Enum):
    FULLY_QUALIFIED = "fully-qualified"
    MINIMALLY_QUALIFIED = "minimally-qualified"
    UNQUALIFIED = "unqualified"


def make_regex_dict() -> Mapping[str, str]:
    d: MutableMapping[str, str] = {}
    d.update(
        {
            "EMOJI_CHARACTER": r"["
            + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EMOJI in m.properties)
            + r"]"
        }
    )
    d.update(
        {
            "DEFAULT_EMOJI_PRESENTATION_CHARACTER": r"["
            + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EPRES in m.properties)
            + r"]"
        }
    )
    d.update(
        {
            "DEFAULT_TEXT_PRESENTATION_CHARACTER": r"["
            + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EPRES not in m.properties)
            + r"]"
        }
    )
    d.update({"TEXT_PRESENTATION_SELECTOR": code_point_to_regex(TEXT_PRESENTATION_SELECTOR)})
    d.update({"TEXT_PRESENTATION_SEQUENCE": r"({EMOJI_CHARACTER}{TEXT_PRESENTATION_SELECTOR})".format(**d)})
    d.update({"EMOJI_PRESENTATION_SELECTOR": code_point_to_regex(EMOJI_PRESENTATION_SELECTOR)})
    d.update({"EMOJI_PRESENTATION_SEQUENCE": r"({EMOJI_CHARACTER}{EMOJI_PRESENTATION_SELECTOR})".format(**d)})
    d.update(
        {
            "EMOJI_MODIFIER": r"["
            + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EMOD in m.properties)
            + r"]"
        }
    )
    d.update(
        {
            "EMOJI_MODIFIER_BASE": r"["
            + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EBASE in m.properties)
            + r"]"
        }
    )
    d.update({"EMOJI_MODIFIER_SEQUENCE": r"({EMOJI_MODIFIER_BASE}{EMOJI_MODIFIER})".format(**d)})
    d.update(
        {
            "REGIONAL_INDICATOR": r"["
            + code_point_to_regex(REGIONAL_INDICATORS[0])
            + r"-"
            + code_point_to_regex(REGIONAL_INDICATORS[-1])
            + r"]"
        }
    )
    d.update({"EMOJI_FLAG_SEQUENCE": r"({REGIONAL_INDICATOR}{REGIONAL_INDICATOR})".format(**d)})
    d.update({"TAG_BASE": r"({EMOJI_CHARACTER}|{EMOJI_MODIFIER_SEQUENCE}|{EMOJI_PRESENTATION_SEQUENCE})".format(**d)})
    d.update({"TAG_SPEC": r"[" + code_point_to_regex(TAGS[0]) + r"-" + code_point_to_regex(TAGS[-2]) + r"]"})
    d.update({"TAG_TERM": code_point_to_regex(TAGS[-1])})
    d.update({"EMOJI_TAG_SEQUENCE": r"({TAG_BASE}{TAG_SPEC}{TAG_TERM})".format(**d)})
    d.update(
        {
            "EMOJI_KEYCAP_SEQUENCE": r"([0-9#*]{}{})".format(
                *(code_point_to_regex(n) for n in (EMOJI_PRESENTATION_SELECTOR, EMOJI_KEYCAP))
            )
        }
    )
    d.update(
        {
            "EMOJI_CORE_SEQUENCE": r"("
            r"{EMOJI_CHARACTER}"
            r"|{EMOJI_PRESENTATION_SEQUENCE}"
            r"|{EMOJI_KEYCAP_SEQUENCE}"
            r"|{EMOJI_MODIFIER_SEQUENCE}"
            r"|{EMOJI_FLAG_SEQUENCE}"
            r")".format(**d)
        }
    )
    d.update({"EMOJI_ZWJ_ELEMENT": r"({EMOJI_CHARACTER}|{EMOJI_PRESENTATION_SEQUENCE}|{EMOJI_MODIFIER_SEQUENCE})".format(**d)})
    d.update({"EMOJI_ZWJ_SEQUENCE": r"({EMOJI_ZWJ_ELEMENT}({0}{EMOJI_ZWJ_ELEMENT})+)".format(code_point_to_regex(ZWJ), **d)})
    d.update({"EMOJI_SEQUENCE": r"({EMOJI_CORE_SEQUENCE}|{EMOJI_ZWJ_SEQUENCE}|{EMOJI_TAG_SEQUENCE})".format(**d)})
    return d


EMOJI_PATTERNS: Mapping[str, Pattern[str]] = {k: re.compile(v) for k, v in make_regex_dict().items()}


def is_emoji_character(c: str) -> bool:
    """detect emoji character

    A character that has the Emoji property.

    ::

        emoji_character := \\p{Emoji}

    - These characters are recommended for use as emoji.

    See also:
        https://unicode.org/reports/tr51/#Emoji_Characters
    """
    _c = chr(ord(c))
    return EMOJI_PATTERNS["EMOJI_CHARACTER"].fullmatch(_c) is not None


def is_default_emoji_presentation_character(c: str) -> bool:
    """detect default emoji presentation character

    A character that, by default, should appear with an emoji presentation, rather than a text presentation.

    ::

        default_emoji_presentation_character := \\p{Emoji_Presentation}

    - These characters have the Emoji_Presentation property.

    See also:
        https://unicode.org/reports/tr51/#def_emoji_presentation
    """
    _c = chr(ord(c))
    return EMOJI_PATTERNS["DEFAULT_EMOJI_PRESENTATION_CHARACTER"].fullmatch(_c) is not None


def is_default_text_presentation_character(c: str) -> bool:
    """detect default text presentation character

    A character that, by default, should appear with a text presentation, rather than an emoji presentation.

    See also:
        https://unicode.org/reports/tr51/#def_text_presentation_sequence
    """
    _c = chr(ord(c))
    return EMOJI_PATTERNS["DEFAULT_TEXT_PRESENTATION_CHARACTER"].fullmatch(_c) is not None


def is_text_presentation_selector(c: str) -> bool:
    """detect text presentation selector

    The character U+FE0E VARIATION SELECTOR-15 (VS15), used to request a text presentation for an emoji character. (Also known as text variation selector in prior versions of this specification.)

    See also:
        https://unicode.org/reports/tr51/#def_emoji_presentation_selector
    """
    return EMOJI_PATTERNS["TEXT_PRESENTATION_SELECTOR"].fullmatch(c) is not None


def is_text_presentation_sequence(s: str) -> bool:
    """detect text presentation selector

    The character U+FE0E VARIATION SELECTOR-15 (VS15), used to request a text presentation for an emoji character. (Also known as text variation selector in prior versions of this specification.)

    See also:
        https://unicode.org/reports/tr51/#def_text_presentation_sequence
    """
    return EMOJI_PATTERNS["TEXT_PRESENTATION_SEQUENCE"].fullmatch(s) is not None


def is_emoji_presentation_selector(c: str) -> bool:
    """detect emoji presentation selector

    The character U+FE0F VARIATION SELECTOR-16 (VS16), used to request an emoji presentation for an emoji character. (Also known as emoji variation selector in prior versions of this specification.)

    See also:
        https://unicode.org/reports/tr51/#def_emoji_presentation_selector
    """
    return EMOJI_PATTERNS["EMOJI_PRESENTATION_SELECTOR"].fullmatch(c) is not None


def is_emoji_presentation_sequence(s: str) -> bool:
    """detect emoji presentation sequence

    A variation sequence consisting of an emoji character followed by a emoji presentation selector.

    ::

        emoji_presentation_sequence := emoji_character emoji_presentation_selector

    - The only valid emoji presentation sequences are those listed in emoji-variation-sequences.txt

    See also:
        https://unicode.org/reports/tr51/#def_emoji_presentation_sequence
    """
    return EMOJI_PATTERNS["EMOJI_PRESENTATION_SEQUENCE"].fullmatch(s) is not None


def is_emoji_modifier(c: str) -> bool:
    """detect emoji modifier

    A character that can be used to modify the appearance of a preceding emoji in an emoji modifier sequence.

    See also:
        https://unicode.org/reports/tr51/#def_emoji_modifier
    """
    _c = chr(ord(c))
    return EMOJI_PATTERNS["EMOJI_MODIFIER"].fullmatch(_c) is not None


def is_emoji_modifier_base(c: str) -> bool:
    """Detect emoji modifier base

    A character whose appearance can be modified by a subsequent emoji modifier in an emoji modifier sequence.

    See also:
        https://unicode.org/reports/tr51/#def_emoji_modifier_base
    """
    _c = chr(ord(c))
    return EMOJI_PATTERNS["EMOJI_MODIFIER_BASE"].fullmatch(_c) is not None


def is_emoji_modifier_sequence(s: str) -> bool:
    """Detect emoji modifier sequence

    A sequence of the following form::

        emoji_modifier_sequence := emoji_modifier_base emoji_modifier
    """
    return EMOJI_PATTERNS["EMOJI_MODIFIER_SEQUENCE"].fullmatch(s) is not None


def is_regional_indicator(s: str) -> bool:
    """A singleton Regional Indicator character is not a well-formed emoji flag sequence."""
    return EMOJI_PATTERNS["REGIONAL_INDICATOR"].fullmatch(s) is not None


def is_emoji_flag_sequence(s: str) -> bool:
    """Detect emoji flag sequence

    A sequence of two Regional Indicator characters, where the corresponding ASCII characters are valid region sequences as specified by Unicode region subtags in [CLDR], with idStatus = “regular”, “deprecated”, or “macroregion”.
    """
    return EMOJI_PATTERNS["EMOJI_FLAG_SEQUENCE"].fullmatch(s) is not None


def is_tag_base(s: str) -> bool:
    return EMOJI_PATTERNS["TAG_BASE"].fullmatch(s) is not None


def is_tag_spec(s: str) -> bool:
    return EMOJI_PATTERNS["TAG_SPEC"].fullmatch(s) is not None


def is_tag_term(c: str) -> bool:
    return EMOJI_PATTERNS["TAG_TERM"].fullmatch(c) is not None


def is_emoji_tag_sequence(s: str) -> bool:
    return EMOJI_PATTERNS["EMOJI_TAG_SEQUENCE"].fullmatch(s) is not None


def is_emoji_keycap_sequence(s: str) -> bool:
    """Detect emoji keycap sequence

    A sequence of the following form::

        emoji_keycap_sequence := [0-9#*] \\x{FE0F 20E3}
    """
    return EMOJI_PATTERNS["EMOJI_KEYCAP_SEQUENCE"].fullmatch(s) is not None


def is_emoji_core_sequence(s: str) -> bool:
    return EMOJI_PATTERNS["EMOJI_CORE_SEQUENCE"].fullmatch(s) is not None


def is_emoji_zwj_element(s: str) -> bool:
    return EMOJI_PATTERNS["EMOJI_ZWJ_ELEMENT"].fullmatch(s) is not None


def is_emoji_zwj_sequence(s: str) -> bool:
    return EMOJI_PATTERNS["EMOJI_ZWJ_SEQUENCE"].fullmatch(s) is not None


def is_emoji_sequence(s: str) -> bool:
    return EMOJI_PATTERNS["EMOJI_SEQUENCE"].fullmatch(s) is not None


def is_qualified_emoji_character(s: str, i: int) -> bool:
    """check if an emoji character in a string is qualified.

    An emoji character in a string that

    - (a) has default emoji presentation or
    - (b) is the first character in an emoji modifier sequence or
    - (c) is not a default emoji presentation character, but is the first character in an emoji presentation sequence.

    is qualified.

    Args:
        s: the string where the character in it
        i: index of the character in the string to check if qualified

    Returns: :data:`True` if qualified else :data:`False`

    See also:
        http://www.unicode.org/reports/tr51/#def_qualified_emoji_character
    """
    c = s[i]
    if not is_emoji_character(c):
        return False
    if is_default_emoji_presentation_character(c):  # default emoji presentation
        return True
    if EMOJI_PATTERNS["EMOJI_MODIFIER_SEQUENCE"].match(s[i:]):  # first character in an emoji modifier sequence
        return True
    if EMOJI_PATTERNS["EMOJI_PRESENTATION_SEQUENCE"].match(s[i:]):  # first character in an emoji presentation sequence
        return True
    return False


def detect_qualified(s: str) -> QualifiedType:
    """Detect qualified type of emoji string

    - qualified emoji character — An emoji character in a string that

        - (a) has default emoji presentation or
        - (b) is the first character in an emoji modifier sequence or
        - (c) is not a default emoji presentation character, but is the first character in an emoji presentation sequence.

    - fully-qualified emoji — A qualified emoji character, or an emoji sequence in which each emoji character is qualified.
    - minimally-qualified emoji — An emoji sequence in which the first character is qualified but the sequence is not fully qualified.
    - unqualified emoji — An emoji that is neither fully-qualified nor minimally qualified.

    Args:
        s: string to detect
    """
    if not s:
        raise ValueError("Argument `s` should not be empty or null")
    if is_qualified_emoji_character(s, 0):
        n = len(s)
        if n == 1:
            return QualifiedType.FULLY_QUALIFIED
        if all(is_qualified_emoji_character(s, i) for i in range(1, n) if is_emoji_character(s[i])):
            return QualifiedType.FULLY_QUALIFIED
        return QualifiedType.MINIMALLY_QUALIFIED
    return QualifiedType.UNQUALIFIED

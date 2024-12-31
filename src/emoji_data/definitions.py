"""Regular expressions for Emoji Definitions

Note:
    :func:`initial_emoji_patterns` **MUST** be called first before using any of the functions in the module.

See also:
    http://www.unicode.org/reports/tr51/#Definitions
"""

import re
from enum import Enum
from typing import Mapping, Pattern

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
    "get_emoji_patterns",
    "initial_emoji_patterns",
    "release_emoji_patterns",
    "QualifiedType",
    "detect_qualified",
    "is_extended_pictographic_character",
    "is_emoji_component",
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
    """RGI_Emoji_Qualification — the status of emoji sequences

    This is an enumerated property of strings, defined by the emoji-test.txt file [emoji-data].
    It assigns one of the three values in ED-18, ED-18a, ED-19 to each emoji in ED-27 RGI emoji set and related sequences with missing variation selectors.
    The property value names and short aliases are:

    - Fully_Qualified, FQE
    - Minimally_Qualified, MQE
    - Unqualified, UQE

    See also:
        https://www.unicode.org/reports/tr51/#def_rgi_emoji_qualification
    """

    FULLY_QUALIFIED = "FQE"
    MINIMALLY_QUALIFIED = "MQE"
    UNQUALIFIED = "UQE"


def initial_emoji_patterns():
    """Initial the emoji patterns dictionary

    **MUST** be called first before using any of the functions in the module.
    """
    global _EMOJI_PATTERNS
    if _EMOJI_PATTERNS:
        return

    d = {}

    d["EMOJI_CHARACTER"] = (
        r"[" + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EMOJI in m.properties) + r"]"
    )

    d["EXTENDED_PICTOGRAPHIC_CHARACTER"] = (
        r"[" + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EXTPICT in m.properties) + r"]"
    )

    d["EMOJI_COMPONENT"] = (
        r"[" + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.ECOMP in m.properties) + r"]"
    )

    d["DEFAULT_EMOJI_PRESENTATION_CHARACTER"] = (
        r"[" + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EPRES in m.properties) + r"]"
    )

    d["DEFAULT_TEXT_PRESENTATION_CHARACTER"] = (
        r"[" + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EPRES not in m.properties) + r"]"
    )
    d["TEXT_PRESENTATION_SELECTOR"] = code_point_to_regex(TEXT_PRESENTATION_SELECTOR)
    d["TEXT_PRESENTATION_SEQUENCE"] = r"({EMOJI_CHARACTER}{TEXT_PRESENTATION_SELECTOR})".format(**d)
    d["EMOJI_PRESENTATION_SELECTOR"] = code_point_to_regex(EMOJI_PRESENTATION_SELECTOR)
    d["EMOJI_PRESENTATION_SEQUENCE"] = r"({EMOJI_CHARACTER}{EMOJI_PRESENTATION_SELECTOR})".format(**d)
    d["EMOJI_MODIFIER"] = (
        r"[" + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EMOD in m.properties) + r"]"
    )
    d["EMOJI_MODIFIER_BASE"] = (
        r"[" + "".join(m.regex for m in EmojiCharacter.values() if EmojiCharProperty.EBASE in m.properties) + r"]"
    )
    d["EMOJI_MODIFIER_SEQUENCE"] = r"({EMOJI_MODIFIER_BASE}{EMOJI_MODIFIER})".format(**d)
    d["REGIONAL_INDICATOR"] = (
        r"[" + code_point_to_regex(REGIONAL_INDICATORS[0]) + r"-" + code_point_to_regex(REGIONAL_INDICATORS[-1]) + r"]"
    )
    d["EMOJI_FLAG_SEQUENCE"] = r"({REGIONAL_INDICATOR}{REGIONAL_INDICATOR})".format(**d)
    d["TAG_BASE"] = r"({EMOJI_CHARACTER}|{EMOJI_MODIFIER_SEQUENCE}|{EMOJI_PRESENTATION_SEQUENCE})".format(**d)
    d["TAG_SPEC"] = r"[" + code_point_to_regex(TAGS[0]) + r"-" + code_point_to_regex(TAGS[-2]) + r"]"
    d["TAG_TERM"] = code_point_to_regex(TAGS[-1])
    d["EMOJI_TAG_SEQUENCE"] = r"({TAG_BASE}{TAG_SPEC}{TAG_TERM})".format(**d)
    d["EMOJI_KEYCAP_SEQUENCE"] = r"([0-9#*]{}{})".format(
        *(code_point_to_regex(x) for x in (EMOJI_PRESENTATION_SELECTOR, EMOJI_KEYCAP))
    )
    d["EMOJI_CORE_SEQUENCE"] = (
        r"("
        r"{EMOJI_CHARACTER}"
        r"|{EMOJI_PRESENTATION_SEQUENCE}"
        r"|{EMOJI_KEYCAP_SEQUENCE}"
        r"|{EMOJI_MODIFIER_SEQUENCE}"
        r"|{EMOJI_FLAG_SEQUENCE}"
        r")".format(**d)
    )
    d["EMOJI_ZWJ_ELEMENT"] = r"({EMOJI_CORE_SEQUENCE}|{EMOJI_TAG_SEQUENCE})".format(**d)
    d["EMOJI_ZWJ_SEQUENCE"] = r"({EMOJI_ZWJ_ELEMENT}({0}{EMOJI_ZWJ_ELEMENT})+)".format(code_point_to_regex(ZWJ), **d)
    d["EMOJI_SEQUENCE"] = r"({EMOJI_CORE_SEQUENCE}|{EMOJI_ZWJ_SEQUENCE}|{EMOJI_TAG_SEQUENCE})".format(**d)

    _EMOJI_PATTERNS = {k: re.compile(v) for k, v in d.items()}


def release_emoji_patterns():
    """Release emoji patterns dictionary"""
    global _EMOJI_PATTERNS
    _EMOJI_PATTERNS = {}


def get_emoji_patterns() -> Mapping[str, Pattern[str]]:
    return _EMOJI_PATTERNS


_EMOJI_PATTERNS: Mapping[str, Pattern[str]] = {}


def is_emoji_character(c: str) -> bool:
    """detect emoji character

    A character that has the Emoji property.

    ::

        emoji_character := \\p{Emoji}

    - These characters are recommended for use as emoji.

    See also:
        https://unicode.org/reports/tr51/#Emoji_Characters
    """
    c = chr(ord(c))
    return _EMOJI_PATTERNS["EMOJI_CHARACTER"].fullmatch(c) is not None


def is_extended_pictographic_character(c: str) -> bool:
    """extended pictographic character — a character that has the **Extended_Pictographic** property.

    - These characters are pictographic, or otherwise similar in kind to characters with the Emoji property.
    - The **Extended_Pictographic** property is used to customize segmentation (as described in [UAX29] and [UAX14]) so that possible future emoji ZWJ sequences will not break grapheme clusters, words, or lines.
      Unassigned codepoints with Line_Break=ID in some blocks are also assigned the **Extended_Pictographic** property.
      Those blocks are intended for future allocation of emoji characters.

    See also:
        https://www.unicode.org/reports/tr51/#def_level1_emoji
    """
    c = chr(ord(c))
    return _EMOJI_PATTERNS["EXTENDED_PICTOGRAPHIC_CHARACTER"].fullmatch(c) is not None


def is_emoji_component(c: str) -> bool:
    """emoji component — A character that has the **Emoji_Component** property.

    - These characters are used in emoji sequences but normally do not appear on emoji keyboards as separate choices, such as keycap base characters or Regional_Indicator characters.
    - Some **emoji components** are **emoji characters**, and others (such as tag characters and **ZWJ**) are not.

    See also:
        https://www.unicode.org/reports/tr51/#def_level2_emoji
    """
    c = chr(ord(c))
    return _EMOJI_PATTERNS["EMOJI_COMPONENT"].fullmatch(c) is not None


def is_default_emoji_presentation_character(c: str) -> bool:
    """default emoji presentation character — A character that, by default, should appear with an emoji presentation, rather than a text presentation.

    ::

        default_emoji_presentation_character := \\p{Emoji_Presentation}

    - These characters have the **Emoji_Presentation** property. See `Annex A: Emoji Properties and Data Files <https://unicode.org/reports/tr51/#Emoji_Properties_and_Data_Files>`_.

    See also:
        https://unicode.org/reports/tr51/#def_emoji_presentation
    """
    c = chr(ord(c))
    return _EMOJI_PATTERNS["DEFAULT_EMOJI_PRESENTATION_CHARACTER"].fullmatch(c) is not None


def is_default_text_presentation_character(c: str) -> bool:
    """default text presentation character — A character that, by default, should appear with a text presentation, rather than an emoji presentation.

    ::

        default_text_presentation_character := \\P{Emoji_Presentation}

    - These characters do not have the **Emoji_Presentation** property; that is, their **Emoji_Presentation** property value is **No**.
      See `Annex A: Emoji Properties and Data Files <https://unicode.org/reports/tr51/#Emoji_Properties_and_Data_Files>`_.

    See also:
        https://unicode.org/reports/tr51/#def_text_presentation
    """
    c = chr(ord(c))
    return _EMOJI_PATTERNS["DEFAULT_TEXT_PRESENTATION_CHARACTER"].fullmatch(c) is not None


def is_text_presentation_selector(c: str) -> bool:
    """text presentation selector
    — The character U+FE0E VARIATION SELECTOR-15 (VS15), used to request a text presentation for an emoji character.
    (Also known as text variation selector in prior versions of this specification.)

    ::

        text_presentation_selector := \\x{FE0E}

    See also:
        https://unicode.org/reports/tr51/#def_text_presentation_selector
    """
    return _EMOJI_PATTERNS["TEXT_PRESENTATION_SELECTOR"].fullmatch(c) is not None


def is_text_presentation_sequence(s: str) -> bool:
    """text presentation sequence
    — A variation sequence consisting of an emoji character followed by a text presentation selector.

    ::

        text_presentation_sequence := emoji_character text_presentation_selector

    - The only valid **text presentation sequences** are those listed in **emoji-variation-sequences.txt** [`emoji-data <https://unicode.org/reports/tr51/#emoji_data>`_].

    See also:
        https://unicode.org/reports/tr51/#def_text_presentation_sequence
    """
    return _EMOJI_PATTERNS["TEXT_PRESENTATION_SEQUENCE"].fullmatch(s) is not None


def is_emoji_presentation_selector(c: str) -> bool:
    """emoji presentation selector
    — The character U+FE0F VARIATION SELECTOR-16 (VS16), used to request an emoji presentation for an emoji character.
    (Also known as emoji variation selector in prior versions of this specification.)

    ::

        emoji_presentation_selector := \\x{FE0F}

    See also:
        https://unicode.org/reports/tr51/#def_emoji_presentation_selector
    """
    return _EMOJI_PATTERNS["EMOJI_PRESENTATION_SELECTOR"].fullmatch(c) is not None


def is_emoji_presentation_sequence(s: str) -> bool:
    """emoji presentation sequence
    — A variation sequence consisting of an emoji character followed by a emoji presentation selector.

    ::

        emoji_presentation_sequence := emoji_character emoji_presentation_selector

    - The only valid **emoji presentation sequences** are those listed in **emoji-variation-sequences.txt** [`emoji-data <https://unicode.org/reports/tr51/#emoji_data>`_].

    See also:
        https://unicode.org/reports/tr51/#def_emoji_presentation_sequence
    """
    return _EMOJI_PATTERNS["EMOJI_PRESENTATION_SEQUENCE"].fullmatch(s) is not None


def is_emoji_modifier(c: str) -> bool:
    """emoji modifier
    — A character that can be used to modify the appearance of a preceding emoji in an emoji modifier sequence.

    ::

        emoji_modifier := \\p{Emoji_Modifier}

    - These characters have the **Emoji_Modifier** property. See `Annex A: Emoji Properties and Data Files <https://unicode.org/reports/tr51/#Emoji_Properties_and_Data_Files>`_.

    See also:
        https://unicode.org/reports/tr51/#def_emoji_modifier
    """
    _c = chr(ord(c))
    return _EMOJI_PATTERNS["EMOJI_MODIFIER"].fullmatch(_c) is not None


def is_emoji_modifier_base(c: str) -> bool:
    """emoji modifier base
    — A character whose appearance can be modified by a subsequent emoji modifier in an emoji modifier sequence.

    ::

        emoji_modifier_base := \\p{Emoji_Modifier_Base}

    - These characters have the **Emoji_Modifier_Base property**. See `Annex A: Emoji Properties and Data Files <https://unicode.org/reports/tr51/#Emoji_Properties_and_Data_Files>`_.
    - They are also listed in `Characters Subject to Emoji Modifiers <https://unicode.org/reports/tr51/#Subject_Emoji_Modifiers>`_.

    See also:
        https://unicode.org/reports/tr51/#def_emoji_modifier_base
    """
    _c = chr(ord(c))
    return _EMOJI_PATTERNS["EMOJI_MODIFIER_BASE"].fullmatch(_c) is not None


def is_emoji_modifier_sequence(s: str) -> bool:
    """emoji modifier sequence
    — A sequence of the following form::

        emoji_modifier_sequence :=
            emoji_modifier_base emoji_modifier
    """
    return _EMOJI_PATTERNS["EMOJI_MODIFIER_SEQUENCE"].fullmatch(s) is not None


def is_regional_indicator(s: str) -> bool:
    """A singleton Regional Indicator character is not a well-formed emoji flag sequence."""
    return _EMOJI_PATTERNS["REGIONAL_INDICATOR"].fullmatch(s) is not None


def is_emoji_flag_sequence(s: str) -> bool:
    """emoji flag sequence
    — A sequence of two Regional Indicator characters,
    where the corresponding ASCII characters are valid region sequences
    as specified by `Unicode region subtags <https://www.unicode.org/reports/tr35/#unicode_region_subtag>`_
    in [`CLDR <https://www.unicode.org/reports/tr51/#CLDR>`_],
    with idStatus = “regular”, “deprecated”, or “macroregion”.
    See also `Annex B: Valid Emoji Flag Sequences <https://www.unicode.org/reports/tr51/#Flags>`_.

    ::

        emoji_flag_sequence :=
            regional_indicator regional_indicator

        regional_indicator := \\p{Regional_Indicator}

    A singleton Regional Indicator character is not a well-formed **emoji flag sequence**.

    See also:
        https://www.unicode.org/reports/tr51/#def_emoji_flag_sequence

    """
    return _EMOJI_PATTERNS["EMOJI_FLAG_SEQUENCE"].fullmatch(s) is not None


def is_tag_base(s: str) -> bool:
    return _EMOJI_PATTERNS["TAG_BASE"].fullmatch(s) is not None


def is_tag_spec(s: str) -> bool:
    return _EMOJI_PATTERNS["TAG_SPEC"].fullmatch(s) is not None


def is_tag_term(c: str) -> bool:
    return _EMOJI_PATTERNS["TAG_TERM"].fullmatch(c) is not None


def is_emoji_tag_sequence(s: str) -> bool:
    """emoji tag sequence (ETS)
    — A sequence of the following form::

        emoji_tag_sequence := tag_base tag_spec tag_end
        tag_base           := emoji_character
                            | emoji_modifier_sequence
                            | emoji_presentation_sequence
        tag_spec           := [\\x{E0020}-\\x{E007E}]+
        tag_end            := \\x{E007F}

    - The `tag_spec` consists of all characters from U+E0020 TAG SPACE to U+E007E TAG TILDE. Each tag_spec defines a particular visual variant to be applied to the tag_base character(s). Though tag_spec includes the values U+E0041 TAG LATIN CAPITAL LETTER A .. U+E005A TAG LATIN CAPITAL LETTER Z, they are not used currently and are reserved for future extensions.
    - The `tag_end` consists of the character U+E007F CANCEL TAG, and must be used to terminate the sequence.
    - A sequence of tag characters that is not part of an `emoji_tag_sequence` is not a well-formed **emoji tag sequence**.

    See also:
        https://www.unicode.org/reports/tr51/#def_emoji_tag_sequence
    """
    return _EMOJI_PATTERNS["EMOJI_TAG_SEQUENCE"].fullmatch(s) is not None


def is_emoji_keycap_sequence(s: str) -> bool:
    """emoji keycap sequence
    — A sequence of the following form::

        emoji_keycap_sequence := [0-9#*] \\x{FE0F 20E3}

    - These sequences are in the **emoji-sequences.txt** file listed under the type_field **Emoji_Keycap_Sequence**

    See also:
        https://www.unicode.org/reports/tr51/#def_emoji_keycap_sequence
    """
    return _EMOJI_PATTERNS["EMOJI_KEYCAP_SEQUENCE"].fullmatch(s) is not None


def is_emoji_core_sequence(s: str) -> bool:
    """emoji core sequence
    — A sequence of the following form::

        emoji_core_sequence :=
            emoji_character
        | emoji_presentation_sequence
        | emoji_keycap_sequence
        | emoji_modifier_sequence
        | emoji_flag_sequence

    See also:
        https://www.unicode.org/reports/tr51/#def_emoji_core_sequence
    """
    return _EMOJI_PATTERNS["EMOJI_CORE_SEQUENCE"].fullmatch(s) is not None


def is_emoji_zwj_element(s: str) -> bool:
    """emoji ZWJ element
    — An element that can be used in an emoji ZWJ sequence, as follows::

        emoji_zwj_element :=
            emoji_core_sequence
        | emoji_tag_sequence

    See also:
        https://www.unicode.org/reports/tr51/#def_emoji_zwj_element
    """
    return _EMOJI_PATTERNS["EMOJI_ZWJ_ELEMENT"].fullmatch(s) is not None


def is_emoji_zwj_sequence(s: str) -> bool:
    """emoji ZWJ sequence
    — An emoji sequence with at least one joiner character.

    ::

        emoji_zwj_sequence :=
        emoji_zwj_element ( ZWJ emoji_zwj_element )+

        ZWJ := \\x{200d}

    See also:
        https://www.unicode.org/reports/tr51/#def_emoji_zwj_sequence
    """
    return _EMOJI_PATTERNS["EMOJI_ZWJ_SEQUENCE"].fullmatch(s) is not None


def is_emoji_sequence(s: str) -> bool:
    """emoji sequence
    — A core sequence, tag sequence, or ZWJ sequence, as follows::

        emoji_sequence :=
            emoji_core_sequence
        | emoji_zwj_sequence
        | emoji_tag_sequence

    Note:
        all emoji sequences are single grapheme clusters: there is never a grapheme cluster boundary within an emoji sequence.
        This affects editing operations, such as cursor movement or deletion, as well as word break, line break, and so on.
        For more information, see [`UAX29 <https://www.unicode.org/reports/tr51/#UAX29>`_].

    See also:
        https://www.unicode.org/reports/tr51/#def_emoji_sequence
    """
    return _EMOJI_PATTERNS["EMOJI_SEQUENCE"].fullmatch(s) is not None


def is_qualified_emoji_character(s: str, i: int) -> bool:
    """An emoji character in a string that

    - (a) has default emoji presentation or
    - (b) is the first character in an emoji modifier sequence or
    - (c) is not a default emoji presentation character, but is the first character in an emoji presentation sequence.

    Args:
        s: the string where the character in it
        i: index of the character in the string to check if qualified

    See also:
        http://www.unicode.org/reports/tr51/#def_qualified_emoji_character
    """
    c = s[i]
    if not is_emoji_character(c):
        return False
    if is_default_emoji_presentation_character(c):  # default emoji presentation
        return True
    if _EMOJI_PATTERNS["EMOJI_MODIFIER_SEQUENCE"].match(s[i:]):  # first character in an emoji modifier sequence
        return True
    if _EMOJI_PATTERNS["EMOJI_PRESENTATION_SEQUENCE"].match(s[i:]):  # first character in an emoji presentation sequence
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
        s: Emoji string to detect

    See also:
        - https://www.unicode.org/reports/tr51/#def_qualified_emoji_character
        - https://www.unicode.org/reports/tr51/#def_fully_qualified_emoji
        - https://www.unicode.org/reports/tr51/#def_minimally_qualified_emoji
        - https://www.unicode.org/reports/tr51/#def_unqualified_emoji
    """
    if is_qualified_emoji_character(s, 0):
        n = len(s)
        if n == 1:
            return QualifiedType.FULLY_QUALIFIED
        if all(is_qualified_emoji_character(s, i) for i in range(1, n) if is_emoji_character(s[i])):
            return QualifiedType.FULLY_QUALIFIED
        return QualifiedType.MINIMALLY_QUALIFIED
    return QualifiedType.UNQUALIFIED

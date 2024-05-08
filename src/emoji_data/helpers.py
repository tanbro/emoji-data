from .character import EmojiCharacter
from .definitions import clear_emoji_regex_dict, make_emoji_regex_dict
from .sequence import EmojiSequence

__all__ = ["load_emoji_data", "unload_emoji_data"]


def load_emoji_data():
    """Load all emoji data from in-package data file.

    Including Emoji characters and sequences
    """
    EmojiCharacter.initial()
    make_emoji_regex_dict()
    EmojiSequence.initial()


def unload_emoji_data():
    """Release emoji data stored in memory"""
    EmojiSequence.release()
    clear_emoji_regex_dict()
    EmojiCharacter.release()

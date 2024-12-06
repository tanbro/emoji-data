from .character import EmojiCharacter
from .definitions import initial_emoji_patterns, release_emoji_patterns
from .sequence import EmojiSequence

__all__ = ["load_emoji_data", "unload_emoji_data"]


def load_emoji_data():
    """Load all emoji data from in-package data file.

    Including Emoji characters and sequences
    """
    EmojiCharacter.initial()
    initial_emoji_patterns()
    EmojiSequence.initial()


def unload_emoji_data():
    """Release emoji data stored in memory"""
    EmojiSequence.release()
    release_emoji_patterns()
    EmojiCharacter.release()

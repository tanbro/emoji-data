from .character import EmojiCharacter
from .definitions import initial_emoji_patterns, release_emoji_patterns
from .sequence import EmojiSequence

__all__ = ["load_emoji_data", "unload_emoji_data"]


def load_emoji_data():
    """Load all emoji data to memory.

    Including internal data of :class:`.EmojiCharacter`, :class:`.EmojiSequence` and :mod:`.definitions`

    Its equivalent to calling :meth:`.EmojiCharacter.initial`, :func:`.initial_emoji_patterns` and :meth:`.EmojiSequence.initial`
    """
    EmojiCharacter.initial()
    initial_emoji_patterns()
    EmojiSequence.initial()


def unload_emoji_data():
    """Release emoji data stored"""
    EmojiSequence.release()
    release_emoji_patterns()
    EmojiCharacter.release()

from .character import EmojiCharacter
from .definitions import clear_emoji_regex_dict, make_emoji_regex_dict
from .sequence import EmojiSequence

__all__ = ["load_emoji_data", "unload_emoji_data"]


def load_emoji_data():
    EmojiCharacter.initial()
    make_emoji_regex_dict()
    EmojiSequence.initial()


def unload_emoji_data():
    EmojiSequence.release()
    clear_emoji_regex_dict()
    EmojiCharacter.release()

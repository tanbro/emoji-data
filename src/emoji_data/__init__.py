"""
A library represents emoji sequences and characters from the data files listed in `Unicode® Technical Standard #51 <http://www.unicode.org/reports/tr51/>`_
"""
from .character import EmojiCharacter, EmojiCharProperty
from .sequence import EmojiSequence
from .version import version as __version__

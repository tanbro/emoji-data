"""
A library represents emoji characters and sequences defined in `Unicode® Technical Standard #51 Data Files <http://www.unicode.org/reports/tr51/#Data_Files_Table>`_

Starting with Version 11.0 of Unicode® Technical Standard #51(UNICODE EMOJI) specification, the repertoire of emoji characters is synchronized with the Unicode Standard, and has the same version numbering system.

See also:
    https://www.unicode.org/reports/tr51/
"""

from ._version import __version__, __version_tuple__
from .character import *
from .definitions import *
from .helpers import *
from .sequence import *
from .utils import *

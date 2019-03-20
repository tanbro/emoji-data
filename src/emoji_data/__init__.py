"""
A library represents emoji sequences and characters in `Unicode® Technical Standard #51 Data Files <http://www.unicode.org/reports/tr51/#Data_Files_Table>`_
"""

from .character import *
from .definitions import *
from .sequence import *
from .utils import code_points_to_string, code_point_to_regex
from .version import version as __version__

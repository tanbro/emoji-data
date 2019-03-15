"""
A library represents emoji sequences and characters from the data files listed in `Unicode® Technical Standard #51 <http://www.unicode.org/reports/tr51/>`_
"""

from .character import *
from .defines import *
from .sequence import *
from .utils import code_points_to_string, code_point_to_regex
from .version import version as __version__

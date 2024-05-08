from datetime import date

from ._version import version, version_tuple

__all__ = ["version", "version_tuple", "EMOJI_VERSION", "EMOJI_DATE", "EMOJI_REVISION"]

EMOJI_VERSION = "15.1"
EMOJI_DATE = date.fromisoformat("2023-09-05")
EMOJI_REVISION = "25"

from datetime import date

from ._version import version, version_tuple

__all__ = ["version", "version_tuple", "EMOJI_VERSION", "EMOJI_DATE", "EMOJI_REVISION"]

EMOJI_VERSION = "17.0"
EMOJI_DATE = date.fromisoformat("2025-09-04")
EMOJI_REVISION = "29"

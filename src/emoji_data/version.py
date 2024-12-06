from datetime import date

from ._version import version, version_tuple

__all__ = ["version", "version_tuple", "EMOJI_VERSION", "EMOJI_DATE", "EMOJI_REVISION"]

EMOJI_VERSION = "16.0"
EMOJI_DATE = date.fromisoformat("2024-08-15")
EMOJI_REVISION = "27"

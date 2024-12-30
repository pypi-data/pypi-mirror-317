from importlib.metadata import version

from nmk_base.version import VersionResolver

__title__ = "nmk-badges"
try:
    __version__ = version(__title__)
except Exception:  # pragma: no cover
    # For debug
    __version__ = "unknown"


class NmkBadgesVersionResolver(VersionResolver):
    def get_version(self) -> str:
        return __version__

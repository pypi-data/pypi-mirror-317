"""
lunchable-pushlunch
"""

from lunchable_pushlunch.__about__ import __application__, __version__
from lunchable_pushlunch.pushover import PushLunch

__all__ = [
    "__application__",
    "__version__",
    "PushLunch",
]

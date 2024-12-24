"""Module specific values and logic."""

from importlib.metadata import version
from typing import Final

__version__: Final[str] = version(__package__)

USER_AGENT: Final[str] = __package__

"""Blazingly fast Markdown parser."""

from __future__ import annotations

from pyromark._options import Options
from pyromark._pyromark import (
    Markdown,
    __version__ as __version__,  # noqa: PLC0414
    events,
    html,
)

__all__ = ("Markdown", "Options", "events", "html")

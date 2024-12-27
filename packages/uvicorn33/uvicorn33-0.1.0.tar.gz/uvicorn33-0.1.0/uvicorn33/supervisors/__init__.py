from __future__ import annotations

from typing import TYPE_CHECKING

from uvicorn33.supervisors.basereload import BaseReload
from uvicorn33.supervisors.multiprocess import Multiprocess

if TYPE_CHECKING:
    ChangeReload: type[BaseReload]
else:
    try:
        from uvicorn33.supervisors.watchfilesreload import WatchFilesReload as ChangeReload
    except ImportError:  # pragma: no cover
        from uvicorn33.supervisors.statreload import StatReload as ChangeReload

__all__ = ["Multiprocess", "ChangeReload"]

"""Windows audio adapter: device enumeration + low-latency playback."""

from __future__ import annotations

import logging
import sys

log = logging.getLogger(__name__)


class WinAudioAdapter:
    def __init__(self) -> None:
        self._is_windows = sys.platform == "win32"

    def list_devices(self) -> list[str]:
        if not self._is_windows:
            return ["default"]
        try:
            import sounddevice as sd

            return [d["name"] for d in sd.query_devices()]
        except Exception as exc:  # noqa: BLE001
            log.debug("device enumeration failed: %s", exc)
            return ["default"]

    def describe(self) -> str:
        return f"windows-audio ({'native' if self._is_windows else 'portable'})"
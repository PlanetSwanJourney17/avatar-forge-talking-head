"""CUDA adapter: report GPU availability + memory for the render pipeline."""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class CudaAdapter:
    def __init__(self) -> None:
        self._available = False
        self._device = "cpu"
        self._probe()

    def _probe(self) -> None:
        try:
            import onnxruntime as ort

            providers = ort.get_available_providers()
            if "CUDAExecutionProvider" in providers:
                self._available = True
                self._device = "cuda"
        except Exception as exc:  # noqa: BLE001 - probe must never crash startup
            log.debug("cuda probe failed: %s", exc)

    @property
    def available(self) -> bool:
        return self._available

    @property
    def device(self) -> str:
        return self._device

    def describe(self) -> str:
        return f"{self._device} ({'ok' if self._available else 'fallback to cpu'})"
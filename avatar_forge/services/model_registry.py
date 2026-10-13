"""Lazy ONNX session registry + weight presence checks."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import onnxruntime as ort

if TYPE_CHECKING:
    from avatar_forge.config.settings import Settings

log = logging.getLogger(__name__)

REQUIRED_MODELS = ("landmark", "lipsync", "render", "speaker")


class ModelRegistry:
    def __init__(self, settings: "Settings") -> None:
        self._settings = settings
        self._sessions: dict[str, ort.InferenceSession] = {}
        self._providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]

    def _weight_path(self, name: str) -> Path:
        return self._settings.weights_dir / f"{name}.onnx"

    def session(self, name: str) -> ort.InferenceSession:
        if name in self._sessions:
            return self._sessions[name]
        path = self._weight_path(name)
        if not path.exists():
            raise FileNotFoundError(f"missing model weights: {path}")
        log.info("loading onnx session %s", path.name)
        sess = ort.InferenceSession(str(path), providers=self._providers)
        self._sessions[name] = sess
        return sess

    def cache_path(self, filename: str) -> Path:
        return self._settings.cache_dir / filename

    def missing_weights(self) -> list[str]:
        return [n for n in REQUIRED_MODELS if not self._weight_path(n).exists()]

    def describe(self) -> str:
        present = [n for n in REQUIRED_MODELS if self._weight_path(n).exists()]
        return f"{len(present)}/{len(REQUIRED_MODELS)} models ({', '.join(present) or 'none'})"

    def nearest_voice(self, embedding: np.ndarray) -> str:
        table = self._settings.voice_table
        if not table:
            return "unknown"
        names = list(table.keys())
        mat = np.stack([table[n] for n in names]).astype(np.float32)
        sims = mat @ embedding / (np.linalg.norm(mat, axis=1) * np.linalg.norm(embedding) + 1e-8)
        return names[int(np.argmax(sims))]
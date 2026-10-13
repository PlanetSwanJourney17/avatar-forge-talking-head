"""RigProfile: face landmarks + blendshape basis for one avatar."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass(slots=True)
class RigProfile:
    source: Path
    landmark_count: int
    blendshape_count: int
    landmarks: np.ndarray  # [68, 2] float32, normalized [0,1]
    basis: np.ndarray      # [52, 512] float32, identity basis

    def to_json(self) -> dict[str, Any]:
        return {
            "source": str(self.source),
            "landmark_count": self.landmark_count,
            "blendshape_count": self.blendshape_count,
            "landmarks": self.landmarks.tolist(),
            "basis": self.basis.tolist(),
        }

    @classmethod
    def from_json(cls, payload: dict[str, Any]) -> "RigProfile":
        return cls(
            source=Path(payload["source"]),
            landmark_count=int(payload["landmark_count"]),
            blendshape_count=int(payload["blendshape_count"]),
            landmarks=np.asarray(payload["landmarks"], dtype=np.float32),
            basis=np.asarray(payload["basis"], dtype=np.float32),
        )
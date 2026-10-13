"""AudioTrack: mono float32 samples + sample rate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True, slots=True)
class AudioTrack:
    samples: np.ndarray  # [N] float32, mono, peak-normalized
    sample_rate: int
    source: Path

    @property
    def duration_s(self) -> float:
        return float(self.samples.shape[0]) / float(self.sample_rate)

    @property
    def rms_dbfs(self) -> float:
        rms = float(np.sqrt(np.mean(np.square(self.samples)) + 1e-12))
        return 20.0 * float(np.log10(rms))
"""RenderJob: a queued render request with its resolved settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


@dataclass(slots=True)
class RenderJob:
    face: Path
    audio: Path
    out: Path
    rig_name: str = "default"
    fps: int = 25
    resolution: tuple[int, int] = (512, 512)
    job_id: str = field(default_factory=lambda: uuid4().hex[:12])
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if self.fps <= 0:
            raise ValueError(f"fps must be positive, got {self.fps}")
        w, h = self.resolution
        if w <= 0 or h <= 0:
            raise ValueError(f"resolution must be positive, got {self.resolution}")
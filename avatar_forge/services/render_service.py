"""Render service: frame batch -> mp4 via ffmpeg adapter."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from avatar_forge.services.lipsync_service import FrameBatch

if TYPE_CHECKING:
    from avatar_forge.adapters.ffmpeg_adapter import FfmpegAdapter
    from avatar_forge.services.model_registry import ModelRegistry

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class WrittenVideo:
    path: Path
    frame_count: int
    duration_s: float


class RenderService:
    def __init__(self, models: "ModelRegistry", ffmpeg: "FfmpegAdapter") -> None:
        self._models = models
        self._ffmpeg = ffmpeg

    def write_video(
        self, batch: FrameBatch, sample_rate: int, out: Path
    ) -> WrittenVideo:
        out.parent.mkdir(parents=True, exist_ok=True)
        frame_count = int(batch.frames.shape[0])
        duration = frame_count / batch.fps
        self._ffmpeg.write_frames(
            frames=batch.frames,
            fps=batch.fps,
            out=out,
            audio=None,
        )
        log.info("wrote %d frames (%.2fs) -> %s", frame_count, duration, out)
        return WrittenVideo(path=out, frame_count=frame_count, duration_s=duration)

    def preview_frame(self, batch: FrameBatch, index: int) -> np.ndarray:
        if not 0 <= index < batch.frames.shape[0]:
            raise IndexError(f"frame {index} out of range [0, {batch.frames.shape[0]})")
        return batch.frames[index]
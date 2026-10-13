"""Render handler: face + audio -> talking-head video."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from avatar_forge.bootstrap.container import Container


@dataclass(frozen=True, slots=True)
class RenderResult:
    output_path: Path
    frames: int
    duration_s: float


class RenderHandler:
    def __init__(self, container: "Container") -> None:
        self._c = container

    def handle(self, *, face: Path, audio: Path, out: Path, rig_name: str) -> RenderResult:
        profile = self._c.rig.load_or_extract(face, rig_name)
        track = self._c.voice.load_track(audio)
        frames = self._c.lipsync.synthesize(profile, track)
        written = self._c.render.write_video(frames, track.sample_rate, out)
        return RenderResult(
            output_path=written.path,
            frames=written.frame_count,
            duration_s=written.duration_s,
        )
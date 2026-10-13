"""ffmpeg adapter: pipe raw RGB frames into an mp4 via imageio-ffmpeg."""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np

log = logging.getLogger(__name__)


class FfmpegAdapter:
    def __init__(self, ffmpeg_bin: str | None = None) -> None:
        self._bin = ffmpeg_bin or imageio_ffmpeg.get_ffmpeg_exe()

    def describe(self) -> str:
        if not shutil.which(self._bin) and not Path(self._bin).exists():
            return "missing"
        return self._bin

    def write_frames(
        self,
        *,
        frames: np.ndarray,
        fps: int,
        out: Path,
        audio: Path | None = None,
    ) -> None:
        if frames.ndim != 4 or frames.shape[-1] != 3:
            raise ValueError(f"expected [T,H,W,3], got {frames.shape}")
        t, h, w, _ = frames.shape
        cmd = [
            self._bin, "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{w}x{h}", "-r", str(fps),
            "-i", "pipe:0",
        ]
        if audio is not None:
            cmd += ["-i", str(audio), "-shortest", "-c:a", "aac"]
        cmd += ["-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "18", str(out)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        assert proc.stdin is not None
        try:
            proc.stdin.write(frames.astype(np.uint8).tobytes())
            proc.stdin.close()
        finally:
            _, err = proc.communicate()
            if proc.returncode != 0:
                raise RuntimeError(f"ffmpeg failed ({proc.returncode}): {err.decode(errors='replace')}")
"""Lipsync synthesis: rig + audio track -> per-frame blendshape weights."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from avatar_forge.models.rig_profile import RigProfile
from avatar_forge.models.audio_track import AudioTrack
from avatar_forge.utils.signal_ops import mel_spectrogram, frame_windows

if TYPE_CHECKING:
    from avatar_forge.adapters.cuda_adapter import CudaAdapter
    from avatar_forge.services.model_registry import ModelRegistry

log = logging.getLogger(__name__)

FPS = 25
MEL_BINS = 80
WINDOW_MS = 40


@dataclass(frozen=True, slots=True)
class FrameBatch:
    """Synthesized frames: RGB uint8 [T, H, W, 3] plus per-frame weights."""

    frames: np.ndarray
    weights: np.ndarray
    fps: int


class LipsyncService:
    def __init__(self, models: "ModelRegistry", cuda: "CudaAdapter") -> None:
        self._models = models
        self._cuda = cuda

    def synthesize(self, profile: RigProfile, track: AudioTrack) -> FrameBatch:
        mel = mel_spectrogram(track.samples, track.sample_rate, n_mels=MEL_BINS)
        windows = frame_windows(mel, fps=FPS, window_ms=WINDOW_MS)
        log.info("lipsync: %d frames, mel=%s", windows.shape[0], mel.shape)

        session = self._models.session("lipsync")
        identity = profile.basis[None, ...].astype(np.float32)
        weights = session.run(None, {"mel": windows.astype(np.float32), "id": identity})[0]

        renderer = self._models.session("render")
        frames = renderer.run(None, {"weights": weights.astype(np.float32)})[0]
        frames_u8 = np.clip(frames * 255.0, 0, 255).astype(np.uint8)
        return FrameBatch(frames=frames_u8, weights=weights, fps=FPS)
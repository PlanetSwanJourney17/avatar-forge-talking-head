"""Voice service: load + normalize the driving audio track."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import soundfile as sf

from avatar_forge.models.audio_track import AudioTrack
from avatar_forge.utils.signal_ops import resample_linear, peak_normalize

if TYPE_CHECKING:
    from avatar_forge.services.model_registry import ModelRegistry

log = logging.getLogger(__name__)

TARGET_SR = 16_000


class VoiceService:
    def __init__(self, models: "ModelRegistry") -> None:
        self._models = models

    def load_track(self, audio: Path) -> AudioTrack:
        samples, sr = sf.read(str(audio), dtype="float32", always_2d=True)
        mono = samples.mean(axis=1)
        if sr != TARGET_SR:
            log.info("resampling %d -> %d Hz", sr, TARGET_SR)
            mono = resample_linear(mono, sr, TARGET_SR)
            sr = TARGET_SR
        mono = peak_normalize(mono, target_dbfs=-3.0)
        return AudioTrack(samples=mono, sample_rate=sr, source=audio)

    def estimate_speaker(self, track: AudioTrack) -> str:
        # speaker embedding model -> nearest known voice id
        session = self._models.session("speaker")
        emb = session.run(None, {"audio": track.samples[None, :].astype(np.float32)})[0]
        return self._models.nearest_voice(emb[0])
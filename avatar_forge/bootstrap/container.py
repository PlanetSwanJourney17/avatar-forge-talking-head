"""Dependency container. Wires adapters + services for handlers."""

from __future__ import annotations

from dataclasses import dataclass

from avatar_forge.adapters.ffmpeg_adapter import FfmpegAdapter
from avatar_forge.adapters.cuda_adapter import CudaAdapter
from avatar_forge.adapters.win_audio_adapter import WinAudioAdapter
from avatar_forge.config.settings import Settings, load_settings
from avatar_forge.services.lipsync_service import LipsyncService
from avatar_forge.services.rig_service import RigService
from avatar_forge.services.render_service import RenderService
from avatar_forge.services.voice_service import VoiceService
from avatar_forge.services.model_registry import ModelRegistry


@dataclass(slots=True)
class Container:
    settings: Settings
    models: ModelRegistry
    rig: RigService
    lipsync: LipsyncService
    voice: VoiceService
    render: RenderService
    ffmpeg: FfmpegAdapter
    cuda: CudaAdapter
    audio: WinAudioAdapter


def build_container() -> Container:
    settings = load_settings()
    ffmpeg = FfmpegAdapter(settings.ffmpeg_bin)
    cuda = CudaAdapter()
    audio = WinAudioAdapter()
    models = ModelRegistry(settings)
    return Container(
        settings=settings,
        models=models,
        rig=RigService(models, cuda),
        lipsync=LipsyncService(models, cuda),
        voice=VoiceService(models),
        render=RenderService(models, ffmpeg),
        ffmpeg=ffmpeg,
        cuda=cuda,
        audio=audio,
    )
"""Face rig extraction: landmarks -> blendshape basis for the avatar."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from avatar_forge.models.rig_profile import RigProfile
from avatar_forge.utils.image_ops import load_rgb, resize_keep_aspect

if TYPE_CHECKING:
    from avatar_forge.adapters.cuda_adapter import CudaAdapter
    from avatar_forge.services.model_registry import ModelRegistry

log = logging.getLogger(__name__)

LANDMARK_COUNT = 68
BLENDSHAPE_COUNT = 52


class RigService:
    def __init__(self, models: "ModelRegistry", cuda: "CudaAdapter") -> None:
        self._models = models
        self._cuda = cuda

    def extract(self, face: Path) -> RigProfile:
        image = load_rgb(face)
        image = resize_keep_aspect(image, 512)
        session = self._models.session("landmark")
        # landmark model expects NCHW float32 in [0,1]
        tensor = (image.astype(np.float32) / 255.0).transpose(2, 0, 1)[None, ...]
        landmarks, basis = session.run(None, {"image": tensor})
        return RigProfile(
            source=face,
            landmark_count=LANDMARK_COUNT,
            blendshape_count=BLENDSHAPE_COUNT,
            landmarks=landmarks[0].astype(np.float32),
            basis=basis[0].astype(np.float32),
        )

    def load_or_extract(self, face: Path, rig_name: str) -> RigProfile:
        cached = self._models.cache_path(f"rig-{rig_name}.json")
        if cached.exists():
            log.info("loading cached rig %s", cached)
            return RigProfile.from_json(json.loads(cached.read_text(encoding="utf-8")))
        profile = self.extract(face)
        self.save(profile, cached)
        return profile

    def save(self, profile: RigProfile, out: Path) -> None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(profile.to_json(), indent=2), encoding="utf-8")
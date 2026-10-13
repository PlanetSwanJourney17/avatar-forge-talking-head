"""Rig handler: extract a face rig profile from a still image."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from avatar_forge.bootstrap.container import Container
    from avatar_forge.models.rig_profile import RigProfile


class RigHandler:
    def __init__(self, container: "Container") -> None:
        self._c = container

    def handle(self, *, face: Path, out: Path) -> "RigProfile":
        profile = self._c.rig.extract(face)
        self._c.rig.save(profile, out)
        return profile
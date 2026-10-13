"""Image helpers for face loading and resizing."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def load_rgb(path: Path) -> np.ndarray:
    """Load an image as RGB uint8 [H,W,3]."""
    with Image.open(path) as im:
        return np.asarray(im.convert("RGB"), dtype=np.uint8)


def resize_keep_aspect(image: np.ndarray, size: int) -> np.ndarray:
    """Resize so the long edge equals `size`, preserving aspect ratio."""
    h, w = image.shape[:2]
    scale = size / float(max(h, w))
    new_w, new_h = max(1, round(w * scale)), max(1, round(h * scale))
    with Image.fromarray(image) as im:
        return np.asarray(im.resize((new_w, new_h), Image.BILINEAR), dtype=np.uint8)
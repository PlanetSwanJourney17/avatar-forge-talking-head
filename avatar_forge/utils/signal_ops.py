"""Audio signal helpers: resample, normalize, mel spectrogram, framing."""

from __future__ import annotations

import numpy as np


def resample_linear(x: np.ndarray, src_sr: int, dst_sr: int) -> np.ndarray:
    if src_sr == dst_sr:
        return x
    n_dst = int(round(x.shape[0] * dst_sr / src_sr))
    src_idx = np.linspace(0.0, x.shape[0] - 1, n_dst, dtype=np.float64)
    return np.interp(src_idx, np.arange(x.shape[0]), x).astype(np.float32)


def peak_normalize(x: np.ndarray, target_dbfs: float = -3.0) -> np.ndarray:
    peak = float(np.max(np.abs(x)) + 1e-12)
    target = 10.0 ** (target_dbfs / 20.0)
    return (x * (target / peak)).astype(np.float32)


def mel_spectrogram(
    samples: np.ndarray,
    sample_rate: int,
    *,
    n_mels: int = 80,
    n_fft: int = 800,
    hop: int = 200,
) -> np.ndarray:
    """Return log-mel [n_mels, T] float32. Simple triangular filterbank."""
    window = np.hanning(n_fft).astype(np.float32)
    n_frames = 1 + (samples.shape[0] - n_fft) // hop
    if n_frames <= 0:
        return np.zeros((n_mels, 1), dtype=np.float32)
    frames = np.stack([samples[i * hop : i * hop + n_fft] * window for i in range(n_frames)])
    spec = np.abs(np.fft.rfft(frames, n=n_fft)) ** 2
    filters = _mel_filterbank(sample_rate, n_fft, n_mels)
    mel = spec @ filters.T
    return np.log(mel + 1e-6).T.astype(np.float32)


def _mel_filterbank(sample_rate: int, n_fft: int, n_mels: int) -> np.ndarray:
    def hz_to_mel(f: float) -> float:
        return 2595.0 * np.log10(1.0 + f / 700.0)

    def mel_to_hz
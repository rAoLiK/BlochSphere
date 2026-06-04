"""Generate animated GIF of Bloch sphere state evolution using qutip.Bloch."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")  # non-interactive backend

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from qutip import Bloch


# ---------------------------------------------------------------------------
# Styling constants
# ---------------------------------------------------------------------------
INIT_VECTOR_COLOR = "#2471a3"               # blue — initial state
FINAL_VECTOR_COLOR = "#c0392b"              # red — final state
TRAIL_COLOR = "#e67e22"                     # orange trajectory
TRAIL_ALPHA = 0.60
ARC_STEPS = 10                              # smoother arcs
FIG_DPI = 140
FIG_SIZE = (4.3, 4.3)                       # slightly larger
FPS = 15
MAX_GIF_FRAMES = 50
PAUSE_FRAMES = 6                            # duplicates at start / end for pause

# Sans-serif math font for |0⟩ |1⟩ labels
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "mathtext.fontset": "dejavusans",
    "axes.linewidth": 1.2,
})


def _sample_indices(total: int, target: int) -> np.ndarray:
    """Return evenly-spaced indices from [0, total-1], at most *target*."""
    if total <= target:
        return np.arange(total)
    return np.round(np.linspace(0, total - 1, target)).astype(int)


def _setup_bloch() -> Bloch:
    """Create a qutip.Bloch with academic light-theme styling."""
    fig = plt.figure(figsize=FIG_SIZE, dpi=FIG_DPI)
    fig.patch.set_facecolor("white")
    # Center the sphere with balanced margins
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
    b = Bloch(fig=fig)
    b.font_size = 16
    b.font_color = "#222222"
    b.vector_width = 3
    b.sphere_color = "#f5f5f5"
    b.sphere_alpha = 0.12
    b.frame_color = "#888888"
    b.frame_width = 1.4
    b.view = [-60, 30]
    b.xlabel = [r"$x$", ""]
    b.ylabel = [r"$y$", ""]
    # Plain text labels — sans-serif, horizontally aligned
    b.zlabel = [r"$\left|0\right\rangle$", r"$\left|1\right\rangle$"]
    return b


def _lerp_color(c1: str, c2: str, t: float) -> tuple[float, float, float]:
    """Linearly interpolate between two hex colours."""
    from matplotlib.colors import to_rgb
    r1, g1, b1 = to_rgb(c1)
    r2, g2, b2 = to_rgb(c2)
    return (r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t)


def generate_bloch_gif(
    frames: list[tuple[float, float, float]],
    boundaries: Optional[list[int]] = None,
    labels: Optional[list[str]] = None,
) -> bytes:
    """Build an animated GIF from Bloch-vector frames.

    Parameters
    ----------
    frames
        List of (x, y, z) tuples – one per animation step.
    boundaries
        Frame-index where each gate segment starts (chain mode).
        ``None`` for single-gate mode (treated as one segment).
    labels
        Gate label per segment, e.g. ``["X", "H", "Rx(π/2)"]``.

    Returns
    -------
    bytes
        Raw GIF data suitable for ``st.download_button``.
    """
    if not frames:
        raise ValueError("frames must be non-empty")

    # Determine segments
    if boundaries is None:
        boundaries = [0]
    if labels is None:
        labels = [""]

    n_segments = len(labels)

    # Sample frames for manageable GIF size
    indices = _sample_indices(len(frames), MAX_GIF_FRAMES)
    n_gif = len(indices)

    # Build playback sequence: pause → animation → pause
    first_idx = int(indices[0])
    last_idx = int(indices[-1])
    playback_indices = (
        [first_idx] * PAUSE_FRAMES
        + [int(i) for i in indices]
        + [last_idx] * PAUSE_FRAMES
    )
    n_play = len(playback_indices)

    # Segment lookup
    def seg_for_frame(fi: int) -> int:
        for s in range(n_segments - 1, -1, -1):
            if fi >= boundaries[s]:
                return s
        return 0

    # Pre-compute arc pairs: for each playback frame, store (start, end) pairs
    # Draw every consecutive pair up to current frame — no subsampling, no jaggies
    arc_cache: list[list[tuple[tuple[float, float, float], tuple[float, float, float]]]] = []
    for pfi in playback_indices:
        pairs = []
        for ti in range(1, pfi + 1):
            pairs.append((frames[ti - 1], frames[ti]))
        arc_cache.append(pairs)

    # Create Bloch instance
    b = _setup_bloch()

    def _update(frame_idx: int):
        b.clear()
        fi = playback_indices[frame_idx]
        current = frames[fi]
        t_ratio = fi / max(len(frames) - 1, 1)  # 0→1 progress

        # --- Trajectory trail: every consecutive pair, no subsampling ---
        for pt_prev, pt_next in arc_cache[frame_idx]:
            try:
                b.add_arc(pt_prev, pt_next, fmt="-", steps=ARC_STEPS,
                          color=TRAIL_COLOR, alpha=TRAIL_ALPHA, linewidth=2.0)
            except Exception:
                pass

        # --- State vector — colour fades from blue (init) to red (final) ---
        vec_color = _lerp_color(INIT_VECTOR_COLOR, FINAL_VECTOR_COLOR, t_ratio)
        b.add_vectors(list(current), colors=[vec_color])
        b.render()

    anim = FuncAnimation(
        b.fig, _update, frames=n_play,
        interval=1000 // FPS, blit=False, repeat=True,
    )

    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        anim.save(tmp_path, writer=PillowWriter(fps=FPS),
                  savefig_kwargs={"facecolor": "white"})
        plt.close(b.fig)
        return Path(tmp_path).read_bytes()
    finally:
        Path(tmp_path).unlink(missing_ok=True)

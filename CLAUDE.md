# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interactive 3D Bloch Sphere visualization for quantum computing education. Users select an initial quantum state (|0>, |1>, |+>) and a quantum gate (X, Y, Z, H, Rx, Ry, Rz), then watch the state vector animate on a Three.js-rendered Bloch sphere inside a Streamlit app.

## Run Commands

```bash
conda activate bloch
streamlit run app.py    # opens http://localhost:8501
```

Environment setup (one-time):
```bash
bash env/setup.sh       # Linux/WSL — creates conda env "bloch"
# or: env\setup.bat     # Windows
```

No test suite, linter, or CI is configured.

## Architecture

Three-layer design orchestrated by `app.py`:

1. **`ui/`** — Streamlit sidebar controls (`controls.py`), state/matrix display panel (`display.py`), retro-futuristic CSS theme (`styles.py`). All widget state flows through `st.session_state`.

2. **`quantum/`** — `BlochState` wraps a QuTiP `Qobj` (2x1 ket). `gates.py` returns gate dicts with unitary matrix, rotation axis, angle, and LaTeX. `evolution.py` generates 80 interpolated animation frames via partial rotations.

3. **`visualization/`** — `scene.py` builds a standalone HTML page with embedded Three.js (v0.160.0 via CDN). The HTML is injected into Streamlit via `st.components.v1.html()`. Contains all 3D geometry (sphere wireframe, axes, state vector arrow, trajectory arc, rotation axis highlight) and client-side animation loop.

## Key Design Decisions

- **No pip/requirements.txt** — all dependencies are managed through `env/environment.yml` (conda).
- **Three.js is embedded, not npm-installed** — `scene.py` contains a multi-line JavaScript template string that gets data injected as JSON. When modifying the 3D scene, you edit JS inside a Python f-string in `visualization/scene.py`.
- **Animation is client-side** — Python computes frames as (x,y,z) Bloch vectors; Three.js interpolates and renders them. The `speed` parameter controls animation frame rate in the browser.
- **Gate definitions are dicts** — each gate in `gates.py` returns `{"matrix", "axis", "angle", "label", "latex"}`. The `axis` and `angle` fields drive both the trajectory computation and the 3D rotation axis highlight.

## Conventions

- Python 3.10, QuTiP for quantum math, NumPy/SciPy as backends.
- Session state keys: `frames` (animation data), `gate_applied` (whether a gate was just applied).
- The CSS theme is black-orange retro-futuristic with JetBrains Mono font; changes to `styles.py` affect the entire app appearance.
- The Bloch sphere uses physics convention: Z up, X right, Y forward (right-handed).

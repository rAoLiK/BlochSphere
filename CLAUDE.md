# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interactive 3D Bloch Sphere visualization for quantum computing education. Users select an initial quantum state (|0>, |1>, |+>, or custom polar coordinates) and quantum gates (X, Y, Z, H, Rx, Ry, Rz), then watch the state vector animate on a Three.js-rendered Bloch sphere inside a Streamlit app.

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

## Testing

```bash
conda activate bloch
python -m pytest tests/ -v          # all tests
python -m pytest tests/test_state.py -v   # single file
```

`pytest.ini` filters out QuTiP UserWarnings. No linter or CI is configured.

## Architecture

Three-layer design orchestrated by `app.py`, which uses a two-tab layout ("SINGLE GATE" and "GATE CHAIN"):

1. **`quantum/`** — Quantum backend built on QuTiP.
   - `BlochState` (`state.py`) wraps a QuTiP `Qobj` (2x1 ket). Constructed from label ("|0⟩", "|1⟩", "|+⟩"), explicit ket, or polar (theta, phi). Provides `bloch_vector()`, `probabilities()`, `to_ket_text()`, `apply_gate()`.
   - `gates.py` returns gate dicts: `{"matrix", "axis", "angle", "label", "matrix_tex"}`. All gates use `_rotation_gate()` via R_n(θ) = cos(θ/2)·I − i·sin(θ/2)(n·σ). Public API: `get_gate(name, theta)`.
   - `evolution.py` generates 80 interpolated frames per gate via partial rotations. `generate_chain_frames()` chains multiple gates, tracking boundaries, labels, and intermediate states.

2. **`ui/`** — Streamlit UI components. All widget state flows through `st.session_state`.
   - `controls.py`: `render_controls()` (sidebar: theme, initial state, gate selector, APPLY/RESET, speed), `render_chain_controls()` (multi-gate grid with popovers, max 6 per row), `render_chain_evolution()` (intermediate state table).
   - `display.py`: `render_state_display()` (Dirac notation, probabilities bar, Bloch coords), `render_gate_matrix()` (LaTeX rendering).
   - `styles.py`: Two themes (dark: black-orange retro-futuristic; light: warm-gray + muted rose). Uses CSS custom properties. Light mode includes a JS MutationObserver for popover/portal styling.

3. **`visualization/`** — `scene.py` builds a standalone HTML page with embedded Three.js v0.160.0 (CDN via importmap). Injected into Streamlit via `st.iframe()`. Contains all 3D geometry, animation controls, CRT scanline overlay, and chain animation support.

## Data Flow

```
User interaction (sidebar controls)
  → controls dict from render_controls()
  → BlochState construction / gate application (quantum/)
  → generate_frames() or generate_chain_frames() (quantum/evolution.py)
  → scene_data dict
  → build_scene_html() (visualization/scene.py) → full HTML string
  → st.iframe() in Streamlit → Three.js client-side animation
```

## Key Design Decisions

- **No pip/requirements.txt** — all dependencies managed through `env/environment.yml` (conda).
- **Three.js is embedded, not npm-installed** — `scene.py` contains a multi-line JS template string with data injected as JSON. When modifying the 3D scene, you edit JS inside a Python f-string in `visualization/scene.py`.
- **Animation is client-side** — Python computes (x,y,z) Bloch vector frames; Three.js renders them. The `speed` parameter controls frame rate in the browser.
- **Gate definitions are dicts** — `axis` and `angle` fields drive both trajectory computation and 3D rotation axis highlight.
- **Animation trigger mechanism** — integer counters (`anim_trigger`, `chain_trigger`) are appended as HTML comments to the scene HTML to force Streamlit to re-render the iframe when data changes.

## Session State Keys

Key mutable state in `st.session_state`:
- `bloch_state` — current `BlochState` instance
- `history`, `history_labels` — gate application history (single-gate mode)
- `frames` — animation frame list for single-gate mode
- `anim_trigger`, `chain_trigger` — integer counters forcing iframe re-render
- `chain_gates` — list of gate dicts for chain mode configuration
- `chain_frames`, `chain_boundaries`, `chain_labels`, `chain_details`, `chain_final_state` — chain animation data
- `last_gate_label`, `last_gate_angle`, `last_axis`, `last_matrix_tex` — most recent gate info
- `initial_state_label`, `last_custom_key` — initial state tracking
- `theme_selector` — "Dark" or "Light"

## Conventions

- Python 3.10, QuTiP for quantum math, NumPy/SciPy as backends.
- The Bloch sphere uses physics convention: Z up, X right, Y forward (right-handed).
- CSS theme uses JetBrains Mono font; changes to `styles.py` affect the entire app appearance.
- 4-space indentation, type hints on function signatures, docstrings on classes and public functions.
- Module `__init__.py` files re-export public APIs (e.g., `from quantum import BlochState, get_gate, generate_frames, generate_chain_frames`).

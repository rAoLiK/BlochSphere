# Bloch Sphere — Interactive Single-Qubit Gate Evolution

**Interactive 3D visualization of quantum states and gate operations on the Bloch sphere.**

Built with Streamlit + QuTiP + Three.js.

## Features

- **3D Bloch Sphere** with interactive rotation, zoom, and pan
- **State vector** smoothly animating through gate operations
- **Trajectory arcs** tracing the evolution path on the sphere surface
- **Gate support**: X, Y, Z (Pauli), H (Hadamard), Rx, Ry, Rz (parametric rotation)
- **Initial states**: |0⟩, |1⟩, |+⟩
- **Real-time data**: Dirac notation, measurement probabilities, Bloch coordinates
- **Retro-futuristic UI**: Black-orange theme, CRT scanline effect, monospace typography

## Quick Start

### Prerequisites

- [Miniforge](https://github.com/conda-forge/miniforge) or Anaconda
- Git

### Setup

**Linux / WSL:**
```bash
bash env/setup.sh
conda activate bloch
streamlit run app.py
```

**Windows:**
```cmd
env\setup.bat
conda activate bloch
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Usage

1. Select an **initial state** from the sidebar (|0⟩, |1⟩, or |+⟩)
2. Choose a **gate** (X, Y, Z, H, Rx, Ry, Rz)
3. For rotation gates (Rx/Ry/Rz), set the **angle** with the slider
4. Click **APPLY** to execute the gate and watch the animation
5. Use the **mouse** to rotate/zoom the 3D view
6. Use the **animation controls** below the sphere for playback

## Project Structure

```
bloch/
├── app.py                    # Streamlit application entry point
├── quantum/                  # Quantum backend (QuTiP)
│   ├── state.py              # BlochState class
│   ├── gates.py              # Gate definitions
│   └── evolution.py          # Animation frame generation
├── ui/                       # Streamlit UI components
│   ├── styles.py             # Retro-futuristic CSS
│   ├── controls.py           # Sidebar control widgets
│   └── display.py            # State information display
├── visualization/            # 3D rendering
│   └── scene.py              # Three.js scene builder
├── env/                      # Conda environment
│   ├── environment.yml
│   ├── setup.sh
│   └── setup.bat
├── report/                   # Academic report
└── README.md                 # This file
```

## Technical Details

- **Quantum backend**: QuTiP for state representation and gate operations
- **3D rendering**: Three.js (loaded via CDN) embedded in Streamlit via `st.components.html()`
- **Animation**: Frame interpolation through fractional gate rotations, rendered in real-time JS
- **Styling**: Custom CSS with JetBrains Mono font, black-orange color scheme

## Requirements Checklist

- [x] Interactive 3D Bloch sphere visualization
- [x] Pauli gates (X, Y, Z) support
- [x] Hadamard gate support
- [x] Parametric rotation gates (Rx, Ry, Rz) with angle slider
- [x] Smooth 3D animation with trajectory arcs
- [x] Real-time state data display
- [x] Cross-platform (Windows + Linux)
- [x] Conda environment management
- [x] Git version control

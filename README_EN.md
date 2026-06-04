<div align="right">

**English** | **[中文](./README.md)**

</div>

# Bloch Sphere — Interactive Single-Qubit Gate Evolution

Interactive 3D visualization of quantum states and gate operations on the Bloch sphere. Built with Streamlit + QuTiP + Three.js.

---

## Features

- **3D Bloch Sphere** — Three.js rendered with interactive rotation, zoom, and pan; CRT scanline visual effect
- **Quantum Gates** — Pauli gates X / Y / Z, Hadamard gate H, and parametric rotation gates Rx / Ry / Rz with continuous angle slider
- **Multiple Initial States** — Six presets: $\vert 0\rangle$, $\vert 1\rangle$, $\vert +\rangle$, $\vert -\rangle$, $\vert +i\rangle$, $\vert -i\rangle$; custom polar coordinates $(\theta, \phi)$ for any point on the Bloch sphere
- **Single Gate Mode** — Apply gates one at a time, observe real-time state evolution with trajectory arcs
- **Gate Chain Mode** — Configure multi-gate sequences via popover dialogs, execute the full chain with one click, view intermediate states in a table
- **Real-time Data Panel** — Dirac notation, probability bar chart, Bloch coordinates, gate matrix LaTeX rendering
- **GIF Export** — One-click academic-style animated GIF with initial state in blue, trajectory in orange, and final state in red; suited for presentations
- **Dual Theme** — Dark theme in black-orange retro-futuristic style, light theme in warm gray; unified global styling

---

## Screenshots

<div align="center">

| Single Gate (Dark) | Gate Chain (Dark) |
|:---:|:---:|
| <img src="./fig/ScreenShot.png" width="400"> | <img src="./fig/ScreenShot_chain.png" width="400"> |

| Single Gate (Light) | Gate Chain (Light) |
|:---:|:---:|
| <img src="./fig/ScreenShot_light.png" width="400"> | <img src="./fig/ScreenShot_chain_light.png" width="400"> |

</div>

---

## Live Demo

### Single Gate Animation

Apply a single quantum gate and watch the state vector evolve in real time.

<div align="center">

| Dark | Light |
|:---:|:---:|
| <img src="./fig/gif/screen/template_single.gif" width="380"> | <img src="./fig/gif/screen/template_single_light.gif" width="380"> |

</div>

### Gate Chain Animation

Configure a sequence of gates and observe the full evolution path with intermediate states.

<div align="center">

| Dark | Light |
|:---:|:---:|
| <img src="./fig/gif/screen/template_chain.gif" width="380"> | <img src="./fig/gif/screen/template_chain_light.gif" width="380"> |

</div>

---

## GIF Export Preview

The application can export animated GIFs of the Bloch sphere evolution. Below are examples of exported GIFs for each gate type.

### Single Gate Exports

<div align="center">

| Gate | Description | GIF Preview |
|------|-------------|:---:|
| X | Bit flip: rotation about the $x$-axis by $\pi$ | <img src="./fig/gif/singlegate/0_X.gif" width="220"> |
| Y | Bit-phase flip: rotation about the $y$-axis by $\pi$ | <img src="./fig/gif/singlegate/1_Y.gif" width="220"> |
| Z | Phase flip: rotation about the $z$-axis by $\pi$ | <img src="./fig/gif/singlegate/2_Z.gif" width="220"> |
| H | Hadamard: rotation about $(x+z)/\sqrt{2}$ by $\pi$ | <img src="./fig/gif/singlegate/3_H.gif" width="220"> |
| Rx | Rotation about $x$-axis by $\theta = 1.97$ rad | <img src="./fig/gif/singlegate/4_Rx(1.97).gif" width="220"> |
| Ry | Rotation about $y$-axis by $\theta = 1.97$ rad | <img src="./fig/gif/singlegate/5_Ry(1.97).gif" width="220"> |
| Rz | Rotation about $z$-axis by $\theta = 1.97$ rad | <img src="./fig/gif/singlegate/6_Rz(1.97).gif" width="220"> |

</div>

### Gate Chain Export

<div align="center">

| Chain | Description | GIF Preview |
|-------|-------------|:---:|
| Multi-gate | Composite evolution through a user-defined gate sequence | <img src="./fig/gif/multigate/bloch_chain.gif" width="220"> |

</div>

---

## Quick Start

### Prerequisites

- [Miniforge](https://github.com/conda-forge/miniforge) or Anaconda

### Installation

Download the latest release archive from the [Releases](https://github.com/rAoLiK/BlochSphere/releases) page, extract it, and enter the project directory:

```bash
tar -xzf BlochSphere-v2.0.tar.gz    # Linux / WSL
# or extract BlochSphere-v2.0.zip    # Windows
cd BlochSphere
```

**Linux / WSL:**
```bash
bash env/setup.sh
conda activate bloch
```

**Windows:**
```cmd
env\setup.bat
conda activate bloch
```

### Run

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

### Run Tests

```bash
python -m pytest tests/ -v
```

---

## Usage Tutorial

### Single Gate Mode

The "SINGLE GATE" tab lets you apply one quantum gate at a time and observe the result.

1. Select an initial state from the sidebar: $\vert 0\rangle$, $\vert 1\rangle$, $\vert +\rangle$, or enter custom polar coordinates $(\theta, \phi)$.
2. Choose a gate: X, Y, Z, H, Rx, Ry, or Rz.
3. For rotation gates (Rx/Ry/Rz), adjust the angle with the slider.
4. Click APPLY to execute the gate. The state vector animates from the initial state to the final state, with a trajectory arc drawn on the sphere surface.
5. Use the mouse to rotate/zoom the 3D view. Use the animation controls below the sphere for playback.

The sidebar displays the current state in Dirac notation, measurement probabilities, and Bloch coordinates in real time.

Custom initial states can be set via polar coordinates $(\theta, \phi)$, allowing exploration of any point on the Bloch sphere:

<img src="./fig/gif/screen/tutor_basic_2.gif" width="100%">

Basic gate operations on the default initial state:

<img src="./fig/gif/screen/tutor_basic_1.gif" width="100%">

### Gate Chain Mode

The "GATE CHAIN" tab lets you configure a sequence of multiple gates and execute them as a single animation.

1. Click "ADD GATE" to add gates to the chain. Each gate appears as a configurable card.
2. Configure each gate's type and parameters by clicking on its card.
3. Click "APPLY CHAIN" to execute the full sequence. The animation shows the state evolving through each gate, with intermediate states displayed in a table.
4. Use the animation speed slider to control playback speed.

<img src="./fig/gif/screen/tutor_chain_1.gif" width="100%">

### GIF Export

Click "EXPORT GIF" in the sidebar to generate an animated GIF of the current state evolution. A "DOWNLOAD GIF" button appears below it once generation completes.

- The GIF shows the Bloch sphere rotating to reveal the trajectory, with the initial state (blue), trajectory (orange), and final state (red) clearly marked.
- Works in both Single Gate and Gate Chain modes.

---

## Theoretical Background

### The Bloch Sphere

Any pure state of a single qubit can be written as:

$$\vert \psi\rangle = \cos\frac{\theta}{2}\vert 0\rangle + e^{i\phi}\sin\frac{\theta}{2}\vert 1\rangle$$

where $\theta \in [0, \pi]$ is the polar angle and $\phi \in [0, 2\pi)$ is the azimuthal angle. This parameterization maps every qubit state to a point on the unit sphere in $\mathbb{R}^3$, known as the Bloch sphere. The north pole corresponds to $\vert 0\rangle$, the south pole to $\vert 1\rangle$, and the equatorial states are equal superpositions of $\vert 0\rangle$ and $\vert 1\rangle$ with varying relative phase.

The Bloch vector $\mathbf{r} = (x, y, z)$ for a state $\vert \psi\rangle$ is given by the expectation values of the Pauli matrices:

$$x = \langle\sigma_x\rangle, \quad y = \langle\sigma_y\rangle, \quad z = \langle\sigma_z\rangle$$

For a pure state, this vector has unit length and lies on the surface of the Bloch sphere. Mixed states (density matrices with $\mathrm{Tr}(\rho^2) < 1$) lie inside the sphere.

### Quantum Gates as Rotations

Single-qubit gates correspond to rotations of the Bloch vector. Every unitary gate $U$ can be expressed as a rotation by angle $\theta$ about some axis $\hat{n}$:

$$U = \exp\!\left(-i\frac{\theta}{2}\,\hat{n}\cdot\boldsymbol{\sigma}\right) = \cos\frac{\theta}{2}\,I - i\sin\frac{\theta}{2}\,(\hat{n}\cdot\boldsymbol{\sigma})$$

where $\hat{n}$ is a unit vector and $\boldsymbol{\sigma} = (\sigma_x, \sigma_y, \sigma_z)$ are the Pauli matrices.

The standard gates and their matrix representations:

<div align="center">

| Gate | Axis | Angle | Matrix | Description |
|------|------|-------|--------|-------------|
| X | $\hat{x}$ | $\pi$ | $\pmatrix{0&1\\\ 1&0}$ | Bit flip: $\vert 0\rangle \leftrightarrow \vert 1\rangle$ |
| Y | $\hat{y}$ | $\pi$ | $\pmatrix{0&-i\\\ i&0}$ | Bit-phase flip |
| Z | $\hat{z}$ | $\pi$ | $\pmatrix{1&0\\\ 0&-1}$ | Phase flip: $\vert 1\rangle \to -\vert 1\rangle$ |
| H | $(\hat{x}+\hat{z})/\sqrt{2}$ | $\pi$ | $\frac{1}{\sqrt{2}}\pmatrix{1&1\\\ 1&-1}$ | Creates equal superposition |
| Rx | $\hat{x}$ | $\theta$ | $\pmatrix{\cos\frac{\theta}{2}&-i\sin\frac{\theta}{2}\\\ -i\sin\frac{\theta}{2}&\cos\frac{\theta}{2}}$ | Arbitrary rotation about $x$ |
| Ry | $\hat{y}$ | $\theta$ | $\pmatrix{\cos\frac{\theta}{2}&-\sin\frac{\theta}{2}\\\ \sin\frac{\theta}{2}&\cos\frac{\theta}{2}}$ | Arbitrary rotation about $y$ |
| Rz | $\hat{z}$ | $\theta$ | $\pmatrix{e^{-i\theta/2}&0\\\ 0&e^{i\theta/2}}$ | Arbitrary rotation about $z$ |

</div>

The Hadamard gate H deserves special attention: it rotates the state by $\pi$ about an axis tilted $45^\circ$ between $\hat{x}$ and $\hat{z}$. This maps $\vert 0\rangle$ to $\vert +\rangle = (\vert 0\rangle+\vert 1\rangle)/\sqrt{2}$ and $\vert 1\rangle$ to $\vert -\rangle = (\vert 0\rangle-\vert 1\rangle)/\sqrt{2}$.

> [!NOTE]
> **Rotation Gate Angle Convention**
>
> Two angle conventions exist in the quantum computing literature. This project follows the standard convention used by modern quantum frameworks such as QuTiP and Qiskit:
>
> $$R_n(\theta) = \exp\!\left(-i\frac{\theta}{2}\,\hat{n}\cdot\boldsymbol{\sigma}\right)$$
>
> Under this convention, the parameter $\theta$ is exactly the actual rotation angle of the Bloch vector on the sphere. For example, setting $\theta = \pi$ rotates the Bloch vector by exactly $\pi$, corresponding to a flip from the north pole to the south pole.
>
> An alternative convention absorbs the factor of $1/2$ into the parameter definition, writing $R_n(\alpha) = \exp(-i\alpha\,\hat{n}\cdot\boldsymbol{\sigma})$, where $\alpha = \theta/2$ is only half the actual rotation angle. In that convention, achieving a $\pi$ rotation requires setting the parameter to $\pi/2$.
>
> The convention used in this project is physically more intuitive: the angle set in the UI is the real rotation angle on the Bloch sphere, with no extra conversion needed.

### State Evolution and Trajectory

When a gate $U$ is applied to a state $\vert \psi\rangle$, the Bloch vector rotates along a great circle arc on the sphere surface. The axis of rotation is the gate's axis, and the angle is the gate's angle. This application visualizes this evolution by interpolating the rotation in small steps, producing a smooth animation that traces the trajectory arc.

For a chain of gates $U_1, U_2, \ldots, U_n$, the final state is:

$$\vert \psi_{\mathrm{final}}\rangle = U_n \cdots U_2\, U_1\,\vert \psi_{\mathrm{initial}}\rangle$$

The trajectory is the concatenation of the individual arcs, with the endpoint of each gate serving as the starting point of the next.

### Measurement and Probabilities

When a qubit in state $\vert \psi\rangle = \alpha\vert 0\rangle + \beta\vert 1\rangle$ is measured in the computational basis:

$$P(0) = \vert \alpha\vert ^2 = \cos^2\frac{\theta}{2}, \qquad P(1) = \vert \beta\vert ^2 = \sin^2\frac{\theta}{2}$$

The $z$-component of the Bloch vector encodes this:

$$z = \cos\theta = P(0) - P(1)$$

States near the north pole ($z \approx 1$) have a high probability of measuring $0$; states near the south pole ($z \approx -1$) have a high probability of measuring $1$.

---

## Project Structure

```
BlochSphere/
├── app.py                    # Streamlit application entry point
├── quantum/                  # Quantum backend (QuTiP)
│   ├── state.py              # BlochState class
│   ├── gates.py              # Gate definitions
│   └── evolution.py          # Animation frame generation
├── ui/                       # Streamlit UI components
│   ├── styles.py             # Dual-theme CSS (dark + light)
│   ├── controls.py           # Sidebar control widgets
│   └── display.py            # State information display
├── visualization/            # 3D rendering and GIF export
│   ├── scene.py              # Three.js scene builder
│   └── gif_export.py         # Matplotlib/qutip.Bloch GIF generator
├── tests/                    # Pytest test suite
│   ├── test_state.py         # BlochState tests
│   ├── test_apply_logic.py   # Gate application tests
│   ├── test_evolution.py     # Frame generation tests
│   └── test_scene.py         # HTML scene tests
├── env/                      # Conda environment config
│   ├── environment.yml
│   ├── setup.sh
│   └── setup.bat
├── fig/                      # Screenshots and GIF demos
│   ├── gif/singlegate/       # Single-gate GIF exports
│   ├── gif/multigate/        # Gate-chain GIF exports
│   └── gif/screen/           # Screen recordings
├── LICENSE                   # MIT License
├── README_EN.md              # English version
└── report/                   # Academic report
```

---

## Technical Details

- **Quantum backend**: QuTiP for state representation and gate operations. BlochState wraps a QuTiP `Qobj` ($2\times1$ ket) and provides methods for probabilities, Bloch vector computation, and gate application.
- **3D rendering**: Three.js v0.160.0 (loaded via CDN importmap) embedded in Streamlit via `st.iframe()`. All 3D geometry, animation controls, and CRT scanline overlay are in a single HTML template generated by `visualization/scene.py`.
- **Animation**: Python computes $(x,y,z)$ Bloch vector frames through fractional gate rotations; Three.js renders them client-side. The speed parameter controls frame rate.
- **GIF export**: Uses `qutip.Bloch` (matplotlib) with `FuncAnimation` and `PillowWriter`. Generates academic-style GIFs with trajectory arcs, color-coded initial/final states, and smooth interpolation.
- **Styling**: CSS custom properties for theming. All component styles live in the base template; `light_overrides` contains only text/background color adjustments. Popover/dialog portals require explicit `[data-baseweb="popover"]` CSS rules.

---

## Dependencies

All managed via conda (`env/environment.yml`):

<div align="center">

| Package | Purpose |
|---------|---------|
| Python 3.10 | Runtime |
| QuTiP | Quantum state and gate math |
| NumPy / SciPy | Numerical computation |
| Matplotlib | GIF rendering backend |
| Pillow | GIF encoding |
| Streamlit | Web UI framework |

</div>

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

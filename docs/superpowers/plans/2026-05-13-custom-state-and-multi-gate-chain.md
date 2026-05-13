# Custom Initial State & Multi-Gate Chain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add arbitrary initial state via polar coordinates and multi-gate chaining with sequential animation playback to the Bloch Sphere app.

**Architecture:** Two independent features layered on the existing three-tier design (quantum → UI → visualization). Feature 1 extends `BlochState` with θ/φ construction and adds a "Custom" dropdown option. Feature 2 adds a gate chain data model, frame concatenation logic, expander-based controls, and multi-segment Three.js animation.

**Tech Stack:** Python 3.10, Streamlit, QuTiP, NumPy, Three.js v0.160.0

**Spec:** `docs/superpowers/specs/2026-05-13-custom-state-and-multi-gate-chain-design.md`

---

### Task 1: BlochState θ/φ Constructor

**Files:**
- Modify: `quantum/state.py:8-18`
- Create: `tests/test_state.py`

- [ ] **Step 1: Write failing tests for BlochState polar constructor**

```python
# tests/test_state.py
import numpy as np
from quantum.state import BlochState


def test_custom_state_north_pole():
    """theta=0 should give |0⟩ (north pole)."""
    s = BlochState(theta=0.0, phi=0.0)
    x, y, z = s.bloch_vector()
    assert abs(x) < 1e-10
    assert abs(y) < 1e-10
    assert abs(z - 1.0) < 1e-10


def test_custom_state_south_pole():
    """theta=pi should give |1⟩ (south pole)."""
    s = BlochState(theta=np.pi, phi=0.0)
    x, y, z = s.bloch_vector()
    assert abs(x) < 1e-10
    assert abs(y) < 1e-10
    assert abs(z + 1.0) < 1e-10


def test_custom_state_equator():
    """theta=pi/2, phi=0 should give |+⟩ (equator at +X)."""
    s = BlochState(theta=np.pi / 2, phi=0.0)
    x, y, z = s.bloch_vector()
    assert abs(x - 1.0) < 1e-10
    assert abs(y) < 1e-10
    assert abs(z) < 1e-10


def test_custom_state_equator_phi():
    """theta=pi/2, phi=pi/2 should give +Y on equator."""
    s = BlochState(theta=np.pi / 2, phi=np.pi / 2)
    x, y, z = s.bloch_vector()
    assert abs(x) < 1e-10
    assert abs(y - 1.0) < 1e-10
    assert abs(z) < 1e-10


def test_custom_state_unit_norm():
    """Any pure state should have Bloch vector norm ~1."""
    for theta in [0.3, 1.0, 2.5]:
        for phi in [0.0, 1.5, 3.14]:
            s = BlochState(theta=theta, phi=phi)
            x, y, z = s.bloch_vector()
            norm = np.sqrt(x**2 + y**2 + z**2)
            assert abs(norm - 1.0) < 1e-10


def test_custom_state_probabilities():
    """theta=pi/2 should give 50/50 probabilities."""
    s = BlochState(theta=np.pi / 2, phi=0.0)
    p0, p1 = s.probabilities()
    assert abs(p0 - 0.5) < 1e-10
    assert abs(p1 - 0.5) < 1e-10
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /mnt/e/Desktop/Bloch_v2 && python -m pytest tests/test_state.py -v`
Expected: FAIL — `BlochState.__init__` does not accept `theta`/`phi` kwargs.

- [ ] **Step 3: Implement θ/φ constructor in BlochState**

Modify `quantum/state.py` — replace lines 8-18 with:

```python
def __init__(self, ket: Qobj | None = None, label: str = "|0⟩",
             theta: float | None = None, phi: float | None = None):
    if ket is not None:
        self.ket = ket
    elif theta is not None and phi is not None:
        alpha = np.cos(theta / 2)
        beta = np.exp(1j * phi) * np.sin(theta / 2)
        self.ket = Qobj([[alpha], [beta]])
    elif label == "|0⟩":
        self.ket = basis(2, 0)
    elif label == "|1⟩":
        self.ket = basis(2, 1)
    elif label == "|+⟩":
        self.ket = (basis(2, 0) + basis(2, 1)).unit()
    else:
        raise ValueError(f"Unknown initial state label: {label}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /mnt/e/Desktop/Bloch_v2 && python -m pytest tests/test_state.py -v`
Expected: All 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add quantum/state.py tests/test_state.py
git commit -m "feat: add theta/phi polar constructor to BlochState"
```

---

### Task 2: Custom State UI Controls

**Files:**
- Modify: `ui/controls.py:7-68`

- [ ] **Step 1: Update INITIAL_STATES and render_controls**

Replace `ui/controls.py` entirely:

```python
"""Sidebar control widgets for Bloch Sphere app."""

import streamlit as st
import numpy as np


INITIAL_STATES = ["|0⟩", "|1⟩", "|+⟩", "Custom"]
GATES = ["X", "Y", "Z", "H", "Rx", "Ry", "Rz"]


def render_controls() -> dict:
    """Render sidebar controls and return selections as a dict.

    Returns keys: initial_state, custom_theta, custom_phi, gate, theta,
                  apply_clicked, reset_clicked, playing, speed
    """
    result = {}

    st.sidebar.markdown("### INITIAL STATE")
    result["initial_state"] = st.sidebar.selectbox(
        "Select initial quantum state",
        INITIAL_STATES,
        label_visibility="collapsed",
    )

    # Custom state polar coordinate sliders
    if result["initial_state"] == "Custom":
        st.sidebar.markdown("### POLAR COORDINATES")
        theta_deg = st.sidebar.slider(
            "θ (polar angle)",
            min_value=0.0,
            max_value=180.0,
            value=90.0,
            step=1.0,
            label_visibility="collapsed",
        )
        phi_deg = st.sidebar.slider(
            "φ (azimuthal angle)",
            min_value=0.0,
            max_value=360.0,
            value=0.0,
            step=1.0,
            label_visibility="collapsed",
        )
        result["custom_theta"] = np.radians(theta_deg)
        result["custom_phi"] = np.radians(phi_deg)
        st.sidebar.caption(
            f"θ = {theta_deg:.0f}°  φ = {phi_deg:.0f}°"
        )
        # Bloch coordinate preview
        t, p = result["custom_theta"], result["custom_phi"]
        bx = np.sin(t) * np.cos(p)
        by = np.sin(t) * np.sin(p)
        bz = np.cos(t)
        st.sidebar.caption(f"Bloch: ({bx:.3f}, {by:.3f}, {bz:.3f})")
    else:
        result["custom_theta"] = None
        result["custom_phi"] = None

    st.sidebar.markdown("### GATE SELECT")
    result["gate"] = st.sidebar.radio(
        "Select quantum gate",
        GATES,
        horizontal=True,
        label_visibility="collapsed",
    )

    # Rotation angle slider (only for Rx, Ry, Rz)
    if result["gate"] in ("Rx", "Ry", "Rz"):
        st.sidebar.markdown("### ROTATION ANGLE")
        theta_deg = st.sidebar.slider(
            "Rotation angle in degrees",
            min_value=0.0,
            max_value=360.0,
            value=90.0,
            step=1.0,
            label_visibility="collapsed",
        )
        result["theta"] = np.radians(theta_deg)
        st.sidebar.caption(f"θ = {theta_deg:.0f}° = {result['theta']:.3f} rad")
    else:
        result["theta"] = 0.0  # Not used for fixed gates

    st.sidebar.markdown("### ACTION")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        result["apply_clicked"] = st.button("APPLY", use_container_width=True)
    with col2:
        result["reset_clicked"] = st.button("RESET", use_container_width=True)

    st.sidebar.markdown("### ANIMATION")
    result["speed"] = st.sidebar.slider(
        "Speed",
        min_value=0.25,
        max_value=4.0,
        value=1.0,
        step=0.25,
        label_visibility="collapsed",
    )
    st.sidebar.caption(f"Speed: {result['speed']:.2f}x")

    return result
```

- [ ] **Step 2: Update `ui/__init__.py` exports**

No change needed — `render_controls` is already exported.

- [ ] **Step 3: Manual verification**

Run `streamlit run app.py`, select "Custom" in the sidebar, verify θ/φ sliders appear with Bloch coordinate preview. Verify selecting |0⟩/|1⟩/|+⟩ still works unchanged.

- [ ] **Step 4: Commit**

```bash
git add ui/controls.py
git commit -m "feat: add Custom initial state with theta/phi sliders"
```

---

### Task 3: Custom State App Integration

**Files:**
- Modify: `app.py:77-88`

- [ ] **Step 1: Update initial state handling in app.py**

Replace the initial state handling block (lines 77-88) in `app.py`:

```python
# ── Handle initial state change ─────────────────────────────────
if controls["initial_state"] == "Custom":
    st.session_state.bloch_state = BlochState(
        theta=controls["custom_theta"],
        phi=controls["custom_phi"],
    )
    st.session_state.history = [st.session_state.bloch_state]
    st.session_state.last_gate_label = "-"
    st.session_state.last_gate_angle = 0.0
    st.session_state.last_axis = None
    st.session_state.last_matrix_tex = ""
    st.session_state.frames = []
    st.session_state.anim_trigger += 1
else:
    if controls["initial_state"] != st.session_state.bloch_state.to_ket_text():
        label = controls["initial_state"]
        st.session_state.bloch_state = BlochState(label=label)
        st.session_state.history = [st.session_state.bloch_state]
        st.session_state.last_gate_label = "-"
        st.session_state.last_gate_angle = 0.0
        st.session_state.last_axis = None
        st.session_state.last_matrix_tex = ""
        st.session_state.frames = []
        st.session_state.anim_trigger += 1
```

- [ ] **Step 2: Manual verification**

Run `streamlit run app.py`. Select "Custom", drag θ/φ sliders, verify the 3D sphere updates in real time. Apply a gate and verify animation works from the custom state. Switch back to |0⟩ and verify it resets correctly.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: integrate custom polar state into app flow"
```

---

### Task 4: generate_chain_frames Function

**Files:**
- Modify: `quantum/evolution.py`
- Create: `tests/test_evolution.py`

- [ ] **Step 1: Write failing tests for generate_chain_frames**

```python
# tests/test_evolution.py
import numpy as np
from quantum.state import BlochState
from quantum.gates import get_gate
from quantum.evolution import generate_chain_frames


def test_chain_single_gate():
    """Chain with one gate should match single gate result."""
    initial = BlochState(label="|0⟩")
    gates = [{"type": "X", "theta": 0.0}]
    result = generate_chain_frames(initial, gates)
    assert len(result["frames"]) == 81  # num_frames_per_gate=80 → 81 points
    assert len(result["boundaries"]) == 1
    assert result["boundaries"][0] == 0
    assert result["labels"] == ["X"]
    # Final state should be |1⟩ (X gate on |0⟩)
    x, y, z = result["final_state"].bloch_vector()
    assert abs(z + 1.0) < 1e-10


def test_chain_multiple_gates():
    """Chain with two gates should concatenate frames."""
    initial = BlochState(label="|0⟩")
    gates = [
        {"type": "X", "theta": 0.0},
        {"type": "Z", "theta": 0.0},
    ]
    result = generate_chain_frames(initial, gates)
    assert len(result["frames"]) == 162  # 81 + 81
    assert result["boundaries"] == [0, 81]
    assert result["labels"] == ["X", "Z"]


def test_chain_rx_gate_with_angle():
    """Chain with Rx gate should use the specified angle."""
    initial = BlochState(label="|0⟩")
    gates = [{"type": "Rx", "theta": np.pi}]
    result = generate_chain_frames(initial, gates, num_frames_per_gate=10)
    # Rx(pi) on |0⟩ should give |1⟩
    x, y, z = result["final_state"].bloch_vector()
    assert abs(z + 1.0) < 1e-6


def test_chain_preserves_state_continuity():
    """Each gate should start where the previous one ended."""
    initial = BlochState(label="|0⟩")
    gates = [
        {"type": "X", "theta": 0.0},
        {"type": "Y", "theta": 0.0},
    ]
    result = generate_chain_frames(initial, gates, num_frames_per_gate=10)
    # Last frame of gate 0 should equal first frame of gate 1
    boundary = result["boundaries"][1]
    f0_end = result["frames"][boundary - 1]
    f1_start = result["frames"][boundary]
    for a, b in zip(f0_end, f1_start):
        assert abs(a - b) < 1e-10


def test_chain_fills_axis_and_angle():
    """generate_chain_frames should populate axis/angle on gate dicts."""
    initial = BlochState(label="|0⟩")
    gates = [{"type": "H", "theta": 0.0}]
    result = generate_chain_frames(initial, gates)
    g = result["gate_details"][0]
    assert "axis" in g
    assert "angle" in g
    assert g["label"] == "H"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /mnt/e/Desktop/Bloch_v2 && python -m pytest tests/test_evolution.py -v`
Expected: FAIL — `generate_chain_frames` does not exist.

- [ ] **Step 3: Implement generate_chain_frames**

Add to `quantum/evolution.py` after the existing `generate_frames` function:

```python
def generate_chain_frames(initial: BlochState, gates: list[dict],
                          num_frames_per_gate: int = 80) -> dict:
    """Compute animation frames for a chain of gates applied sequentially.

    Args:
        initial: Starting quantum state.
        gates: List of dicts with 'type' and 'theta' keys.
               'theta' is ignored for non-rotation gates.
        num_frames_per_gate: Number of interpolation frames per gate.

    Returns:
        dict with keys:
            frames: list of (x, y, z) tuples for the full chain
            boundaries: list of frame start indices for each gate
            labels: list of gate label strings
            gate_details: list of gate dicts with axis/angle for Three.js
            final_state: BlochState after all gates applied
    """
    from .gates import get_gate

    all_frames = []
    boundaries = []
    labels = []
    gate_details = []
    current_state = initial

    for g in gates:
        gate = get_gate(g["type"], g.get("theta", 0.0))
        boundaries.append(len(all_frames))
        labels.append(gate["label"])
        gate_details.append({
            "label": gate["label"],
            "axis": list(gate["axis"]),
            "angle": gate["angle"],
        })
        result = generate_frames(current_state, gate, num_frames_per_gate)
        all_frames.extend(result["frames"])
        current_state = result["final_state"]

    return {
        "frames": all_frames,
        "boundaries": boundaries,
        "labels": labels,
        "gate_details": gate_details,
        "final_state": current_state,
    }
```

- [ ] **Step 4: Update `quantum/__init__.py` to export generate_chain_frames**

Replace `quantum/__init__.py`:

```python
from .state import BlochState
from .gates import gate_x, gate_y, gate_z, gate_h, gate_rx, gate_ry, gate_rz, get_gate
from .evolution import generate_frames, generate_chain_frames
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /mnt/e/Desktop/Bloch_v2 && python -m pytest tests/test_evolution.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add quantum/evolution.py quantum/__init__.py tests/test_evolution.py
git commit -m "feat: add generate_chain_frames for multi-gate sequential animation"
```

---

### Task 5: Chain Controls UI

**Files:**
- Modify: `ui/controls.py`
- Modify: `ui/__init__.py`

- [ ] **Step 1: Add render_chain_controls to controls.py**

Append to `ui/controls.py` after the `render_controls` function:

```python
CHAIN_GATES = ["X", "Y", "Z", "H", "Rx", "Ry", "Rz"]


def render_chain_controls() -> dict:
    """Render multi-gate chain controls below the main layout.

    Returns dict with keys: chain_gates, apply_clicked, reset_clicked
    """
    # Initialize session state for chain
    if "chain_gates" not in st.session_state:
        st.session_state.chain_gates = [
            {"type": "X", "theta": 0.0, "id": "gate_0"},
        ]

    st.markdown("### MULTI-GATE CHAIN")

    # Render each gate as an expander
    for i, gate_cfg in enumerate(st.session_state.chain_gates):
        gate_type = gate_cfg["type"]
        gate_theta = gate_cfg["theta"]
        if gate_type in ("Rx", "Ry", "Rz"):
            title = f"GATE {i + 1} — {gate_type}({gate_theta:.2f} rad)"
        else:
            title = f"GATE {i + 1} — {gate_type}"

        with st.expander(title, expanded=False):
            # Gate type selection
            new_type = st.radio(
                "Gate type",
                CHAIN_GATES,
                index=CHAIN_GATES.index(gate_type),
                horizontal=True,
                key=f"chain_gate_type_{i}",
                label_visibility="collapsed",
            )
            st.session_state.chain_gates[i]["type"] = new_type

            # Rotation angle for Rx/Ry/Rz
            if new_type in ("Rx", "Ry", "Rz"):
                angle_deg = st.slider(
                    "Rotation angle (°)",
                    min_value=0.0,
                    max_value=360.0,
                    value=float(np.degrees(gate_theta)),
                    step=1.0,
                    key=f"chain_gate_angle_{i}",
                )
                st.session_state.chain_gates[i]["theta"] = np.radians(angle_deg)
            else:
                st.session_state.chain_gates[i]["theta"] = 0.0

            # Remove button
            if len(st.session_state.chain_gates) > 1:
                if st.button("REMOVE", key=f"chain_remove_{i}",
                             use_container_width=True):
                    st.session_state.chain_gates.pop(i)
                    st.rerun()

    # Action buttons
    col_add, col_apply, col_reset = st.columns(3)
    with col_add:
        if st.button("+ ADD GATE", use_container_width=True):
            new_id = f"gate_{len(st.session_state.chain_gates)}"
            st.session_state.chain_gates.append(
                {"type": "X", "theta": 0.0, "id": new_id}
            )
            st.rerun()
    with col_apply:
        apply_clicked = st.button("APPLY CHAIN", use_container_width=True)
    with col_reset:
        reset_clicked = st.button("RESET CHAIN", use_container_width=True)
        if reset_clicked:
            st.session_state.chain_gates = [
                {"type": "X", "theta": 0.0, "id": "gate_0"},
            ]

    return {
        "chain_gates": list(st.session_state.chain_gates),
        "apply_clicked": apply_clicked,
        "reset_clicked": reset_clicked,
    }
```

- [ ] **Step 2: Update `ui/__init__.py` to export render_chain_controls**

Replace `ui/__init__.py`:

```python
from .styles import inject_styles
from .controls import render_controls, render_chain_controls
from .display import render_state_display
```

- [ ] **Step 3: Manual verification**

Import and call `render_chain_controls()` in a test script or temporarily in app.py. Verify: expanders render, gate type radio works, angle slider shows for Rx/Ry/Rz, ADD/REMOVE buttons work, RESET clears to single gate.

- [ ] **Step 4: Commit**

```bash
git add ui/controls.py ui/__init__.py
git commit -m "feat: add render_chain_controls with expander-based gate config"
```

---

### Task 6: Three.js Chain Animation Support

**Files:**
- Modify: `visualization/scene.py:317-418`

- [ ] **Step 1: Update scene_data handling in build_scene_html**

The `build_scene_html` function receives a `data` dict. The Three.js code needs to handle chain animation when `chain_frames` is present. Modify the animation section of the JS template in `scene.py`.

Replace the animation state and render loop sections (lines 317-418) in the JS template with code that checks for chain data:

```javascript
// ── Animation state ──────────────────────────────────
const frames = DATA.chain_frames && DATA.chain_frames.length > 0
    ? DATA.chain_frames : (DATA.frames || []);
const boundaries = DATA.chain_boundaries || [];
const chainLabels = DATA.chain_labels || [];
const chainDetails = DATA.chain_details || [];
const isChain = boundaries.length > 0;

let currentFrame = 0;
let playing = true;
let speed = DATA.speed || 1.0;
const frameInterval = 0.016;
let elapsed = 0;
let animDone = false;

// Track current gate segment for chain animation
let currentGateIdx = 0;

// ── Initialize ───────────────────────────────────────
if (DATA.bloch_vector) {
    updateArrow(DATA.bloch_vector[0], DATA.bloch_vector[1], DATA.bloch_vector[2]);
}
// For chain: show first gate's axis; for single: show DATA.axis
if (isChain && chainDetails.length > 0) {
    const d = chainDetails[0];
    updateAxisHighlight(d.axis[0], d.axis[1], d.axis[2], true);
} else if (DATA.axis) {
    updateAxisHighlight(DATA.axis[0], DATA.axis[1], DATA.axis[2], true);
}

function updateInfo() {
    let g;
    if (isChain && chainLabels.length > 0) {
        g = chainLabels[currentGateIdx] || '-';
    } else {
        g = DATA.gate_label || '-';
    }
    const bv = DATA.bloch_vector || [0,0,0];
    document.getElementById('info-gate').textContent = g;
    document.getElementById('info-bloch').textContent =
        '(' + bv.map(v => v.toFixed(3)).join(', ') + ')';
}
updateInfo();

// ── Chain gate segment tracking ──────────────────────
function getGateIndex(frameIdx) {
    if (!isChain || boundaries.length === 0) return 0;
    for (let i = boundaries.length - 1; i >= 0; i--) {
        if (frameIdx >= boundaries[i]) return i;
    }
    return 0;
}

// ── Trajectory per segment ───────────────────────────
function updateChainTrajectory(frameIdx) {
    while (trajGroup.children.length > 0) trajGroup.remove(trajGroup.children[0]);
    if (!frames || frames.length < 2) return;

    const segIdx = getGateIndex(frameIdx);
    const segStart = boundaries[segIdx] || 0;
    const segEnd = (segIdx + 1 < boundaries.length) ? boundaries[segIdx + 1] : frames.length;
    const shown = frames.slice(segStart, Math.min(frameIdx + 1, segEnd));
    if (shown.length < 2) return;

    const curve = new THREE.CatmullRomCurve3(
        shown.map(p => new THREE.Vector3(p[0], p[1], p[2])));
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.015, 8, false);
    const tube = new THREE.Mesh(tubeGeo, new THREE.MeshStandardMaterial({
        color: 0xff8c00, emissive: 0xff4400, emissiveIntensity: 0.8,
        roughness: 0.2, transparent: true, opacity: 0.85
    }));
    trajGroup.add(tube);
    for (let i = 0; i < shown.length; i += Math.max(1, Math.floor(shown.length / 20))) {
        const p = shown[i];
        const dotGeo = new THREE.SphereGeometry(0.02, 8, 8);
        const dot = new THREE.Mesh(dotGeo, matGlow);
        dot.position.set(p[0], p[1], p[2]);
        trajGroup.add(dot);
    }
}

// ── Controls via addEventListener ────────────────────
const btnPlay = document.getElementById('btn-play');
const btnPause = document.getElementById('btn-pause');
const btnReset = document.getElementById('btn-reset');
const spdSlider = document.getElementById('speed-slider');
const spdLabel = document.getElementById('speed-label');

btnPlay.addEventListener('click', function() {
    if (animDone) {
        currentFrame = 0;
        elapsed = 0;
        animDone = false;
        currentGateIdx = 0;
        playing = true;
        btnPlay.classList.add('active');
        if (frames.length > 0) {
            updateArrow(frames[0][0], frames[0][1], frames[0][2]);
            if (isChain) {
                updateChainTrajectory(0);
                if (chainDetails.length > 0) {
                    const d = chainDetails[0];
                    updateAxisHighlight(d.axis[0], d.axis[1], d.axis[2], true);
                }
            } else {
                updateTrajectory(frames, 0);
            }
        }
    } else {
        playing = !playing;
        btnPlay.classList.toggle('active', playing);
    }
});

btnPause.addEventListener('click', function() {
    playing = false;
    btnPlay.classList.remove('active');
});

btnReset.addEventListener('click', function() {
    currentFrame = 0;
    elapsed = 0;
    playing = false;
    animDone = false;
    currentGateIdx = 0;
    btnPlay.classList.remove('active');
    if (frames.length > 0) {
        const f = frames[0];
        updateArrow(f[0], f[1], f[2]);
        if (isChain) {
            updateChainTrajectory(0);
            if (chainDetails.length > 0) {
                const d = chainDetails[0];
                updateAxisHighlight(d.axis[0], d.axis[1], d.axis[2], true);
            }
        } else {
            updateTrajectory(frames, 0);
        }
    }
});

spdSlider.addEventListener('input', function() {
    speed = parseFloat(this.value);
    spdLabel.textContent = 'SPD ' + speed.toFixed(2) + 'x';
});

// Init state
btnPlay.classList.add('active');
spdSlider.value = DATA.speed || 1;
spdLabel.textContent = 'SPD ' + (DATA.speed || 1).toFixed(2) + 'x';

// ── Render loop ──────────────────────────────────────
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);
    const dt = Math.min(clock.getDelta(), 0.1);
    orbitCtrl.update();

    if (playing && frames.length > 1 && !animDone) {
        elapsed += dt * speed;
        const fps = 1 / frameInterval;
        currentFrame = Math.min(Math.floor(elapsed * fps), frames.length - 1);
        const f = frames[currentFrame];
        updateArrow(f[0], f[1], f[2]);

        if (isChain) {
            const newGateIdx = getGateIndex(currentFrame);
            if (newGateIdx !== currentGateIdx) {
                currentGateIdx = newGateIdx;
                // Update axis highlight for new gate segment
                if (currentGateIdx < chainDetails.length) {
                    const d = chainDetails[currentGateIdx];
                    updateAxisHighlight(d.axis[0], d.axis[1], d.axis[2], true);
                }
            }
            updateChainTrajectory(currentFrame);
            // Update gate label
            document.getElementById('info-gate').textContent =
                chainLabels[currentGateIdx] || '-';
        } else {
            updateTrajectory(frames, currentFrame);
        }

        // Update Bloch vector display
        document.getElementById('info-bloch').textContent =
            '(' + f[0].toFixed(3) + ', ' + f[1].toFixed(3) + ', ' + f[2].toFixed(3) + ')';

        if (currentFrame >= frames.length - 1) {
            animDone = true;
            playing = false;
            btnPlay.classList.remove('active');
        }
    }
    renderer.render(scene, camera);
}
animate();
```

- [ ] **Step 2: Verify the existing single-gate animation still works**

The code above checks `isChain` (derived from `boundaries.length > 0`). When `chain_frames` is empty/absent, `boundaries` is `[]`, so `isChain` is false and the original `updateTrajectory` path runs. Verify by running the app and applying a single gate.

- [ ] **Step 3: Manual verification of chain animation**

This will be fully testable after Task 7 integrates the chain into app.py. For now, verify the code compiles by running `python -c "from visualization.scene import build_scene_html"`.

- [ ] **Step 4: Commit**

```bash
git add visualization/scene.py
git commit -m "feat: Three.js chain animation with per-segment axis and trajectory"
```

---

### Task 7: App.py Chain Integration

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Add imports and chain session state init**

At the top of `app.py`, update the import (line 9):

```python
from quantum import BlochState, get_gate, generate_frames, generate_chain_frames
from ui import inject_styles, render_controls, render_chain_controls
```

Add chain session state init after the existing init block (after line 40):

```python
if "chain_frames" not in st.session_state:
    st.session_state.chain_frames = []
if "chain_boundaries" not in st.session_state:
    st.session_state.chain_boundaries = []
if "chain_labels" not in st.session_state:
    st.session_state.chain_labels = []
if "chain_details" not in st.session_state:
    st.session_state.chain_details = []
if "chain_final_state" not in st.session_state:
    st.session_state.chain_final_state = None
if "chain_trigger" not in st.session_state:
    st.session_state.chain_trigger = 0
```

- [ ] **Step 2: Add chain data to scene_data**

In the `scene_data` dict construction (around line 127-137), add chain fields:

```python
scene_data = {
    "bloch_vector": [x, y, z],
    "frames": st.session_state.frames,
    "axis": list(st.session_state.last_axis) if st.session_state.last_axis else [0, 0, 0],
    "angle": st.session_state.last_gate_angle,
    "gate_label": st.session_state.last_gate_label,
    "prob0": state.probabilities()[0],
    "prob1": state.probabilities()[1],
    "state_text": state.to_ket_text(),
    "speed": controls["speed"],
    "chain_frames": st.session_state.chain_frames,
    "chain_boundaries": st.session_state.chain_boundaries,
    "chain_labels": st.session_state.chain_labels,
    "chain_details": st.session_state.chain_details,
}
```

- [ ] **Step 3: Add chain section after the main layout**

After the existing layout block (after the `col_left`/`col_right` section, around line 184), add:

```python
# ── Multi-gate chain ──────────────────────────────────────
st.markdown("---")
chain_controls = render_chain_controls()

if chain_controls["apply_clicked"] and len(chain_controls["chain_gates"]) > 0:
    result = generate_chain_frames(
        st.session_state.bloch_state,
        chain_controls["chain_gates"],
    )
    st.session_state.chain_frames = result["frames"]
    st.session_state.chain_boundaries = result["boundaries"]
    st.session_state.chain_labels = result["labels"]
    st.session_state.chain_details = result["gate_details"]
    st.session_state.chain_final_state = result["final_state"]
    st.session_state.chain_trigger += 1
    st.rerun()

if chain_controls["reset_clicked"]:
    st.session_state.chain_frames = []
    st.session_state.chain_boundaries = []
    st.session_state.chain_labels = []
    st.session_state.chain_details = []
    st.session_state.chain_final_state = None
    st.session_state.chain_trigger += 1
    st.rerun()

# Display chain final state
if st.session_state.chain_final_state:
    final = st.session_state.chain_final_state
    fx, fy, fz = final.bloch_vector()
    fp0, fp1 = final.probabilities()
    st.markdown(
        f"""
        <div class="data-bar">
            <div class="data-item">
                <div class="data-label">Chain Final State</div>
                <div class="data-value"><span class="ket">{final.to_ket_text()}</span></div>
            </div>
            <div class="data-item">
                <div class="data-label">Bloch Vector</div>
                <div class="data-value">({fx:.4f}, {fy:.4f}, {fz:.4f})</div>
            </div>
            <div class="data-item">
                <div class="data-label">P(|0⟩)</div>
                <div class="data-value">{fp0*100:.1f}%</div>
            </div>
            <div class="data-item">
                <div class="data-label">P(|1⟩)</div>
                <div class="data-value">{fp1*100:.1f}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
```

- [ ] **Step 4: Manual verification**

Run `streamlit run app.py`. Scroll down to MULTI-GATE CHAIN. Add gates (e.g., H → Rx(90°) → Z), click APPLY CHAIN, verify the 3D sphere animates through all three gates sequentially with correct axis highlights and trajectory arcs. Verify the final state display shows the correct result.

- [ ] **Step 5: Commit**

```bash
git add app.py
git commit -m "feat: integrate multi-gate chain into main app"
```

---

### Task 8: Style Refinements

**Files:**
- Modify: `ui/styles.py`

- [ ] **Step 1: Add styles for chain section**

Append to the CSS string in `ui/styles.py` before the closing `"""`:

```css
/* ── Chain section ────────────────────────────────────── */
.chain-gate-expander {
    border: 1px solid #332211 !important;
    margin-bottom: 4px !important;
}
.chain-final-state {
    background: #0d0d0d;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #ff6b00;
    padding: 10px 14px;
    margin-top: 0.5rem;
}
```

Also ensure the expander styling works with the existing theme. The current `.stExpander` styles (lines 263-279) should already handle the chain expanders, but verify the chain section header `h3` renders correctly.

- [ ] **Step 2: Manual verification**

Run the app, check that the MULTI-GATE CHAIN section has consistent styling with the rest of the app — orange headers, dark backgrounds, no rounded corners, JetBrains Mono font.

- [ ] **Step 3: Commit**

```bash
git add ui/styles.py
git commit -m "style: add chain section CSS refinements"
```

---

### Task 9: Final Integration Test

**Files:** None (manual verification)

- [ ] **Step 1: Full Feature 1 test**

1. Run `streamlit run app.py`
2. Select "Custom" in INITIAL STATE
3. Drag θ to 45°, φ to 90° — verify sphere updates
4. Click APPLY with gate X — verify animation plays
5. Switch to |0⟩ — verify reset
6. Switch back to Custom — verify sliders still work

- [ ] **Step 2: Full Feature 2 test**

1. Scroll to MULTI-GATE CHAIN
2. Configure: Gate 1 = H, Gate 2 = Rx(90°), Gate 3 = Z
3. Click APPLY CHAIN
4. Verify: animation plays H rotation → Rx rotation → Z rotation sequentially
5. Verify: axis highlight changes per segment
6. Verify: trajectory arc resets per segment
7. Verify: gate label in info panel updates per segment
8. Verify: final state display shows correct result
9. Click RESET CHAIN — verify chain resets to single X gate

- [ ] **Step 3: Independence test**

1. Apply a single gate (top section)
2. Then apply a chain (bottom section)
3. Verify both work independently without interfering

- [ ] **Step 4: Final commit if any fixes needed**

```bash
git add -A
git commit -m "fix: integration test fixes"
```

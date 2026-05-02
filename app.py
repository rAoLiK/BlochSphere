"""Bloch Sphere — Interactive Single-Qubit Gate Evolution Demo.

Retro-futuristic 3D visualization using Streamlit + QuTiP + Three.js.
"""

import streamlit as st
import numpy as np

from quantum import BlochState, get_gate, generate_frames
from ui import inject_styles, render_controls, render_state_display
from visualization import build_scene_html

# ── Page config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bloch Sphere",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

# ── Session state init ──────────────────────────────────────────────
if "bloch_state" not in st.session_state:
    st.session_state.bloch_state = BlochState(label="|0⟩")
if "history" not in st.session_state:
    st.session_state.history = [st.session_state.bloch_state]
if "last_gate_label" not in st.session_state:
    st.session_state.last_gate_label = "-"
if "last_gate_angle" not in st.session_state:
    st.session_state.last_gate_angle = 0.0
if "last_axis" not in st.session_state:
    st.session_state.last_axis = None
if "frames" not in st.session_state:
    st.session_state.frames = []
if "anim_trigger" not in st.session_state:
    st.session_state.anim_trigger = 0


# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    "<h1>&#9883; BLOCH SPHERE</h1>"
    "<p style='color:#888;font-size:13px;letter-spacing:2px;margin-top:-12px;'>"
    "SINGLE-QUBIT GATE EVOLUTION — INTERACTIVE 3D</p>",
    unsafe_allow_html=True,
)

# ── Controls sidebar ────────────────────────────────────────────────
controls = render_controls()

# ── Handle initial state change ─────────────────────────────────────
if controls["initial_state"] != st.session_state.bloch_state.to_ket_text():
    # Check if it matches known labels
    label = controls["initial_state"]
    st.session_state.bloch_state = BlochState(label=label)
    st.session_state.history = [st.session_state.bloch_state]
    st.session_state.last_gate_label = "-"
    st.session_state.last_gate_angle = 0.0
    st.session_state.last_axis = None
    st.session_state.frames = []
    st.session_state.anim_trigger += 1

# ── Handle gate application ─────────────────────────────────────────
if controls["apply_clicked"]:
    gate_name = controls["gate"]
    theta = controls["theta"]
    gate = get_gate(gate_name, theta)
    result = generate_frames(
        st.session_state.bloch_state,
        gate,
        num_frames=80,
    )
    st.session_state.bloch_state = result["final_state"]
    st.session_state.history.append(st.session_state.bloch_state)
    st.session_state.last_gate_label = gate["label"]
    st.session_state.last_gate_angle = gate["angle"]
    st.session_state.last_axis = gate["axis"]
    st.session_state.frames = result["frames"]
    st.session_state.anim_trigger += 1

# ── Handle reset ────────────────────────────────────────────────────
if controls["reset_clicked"]:
    initial_label = controls["initial_state"]
    st.session_state.bloch_state = BlochState(label=initial_label)
    st.session_state.history = [st.session_state.bloch_state]
    st.session_state.last_gate_label = "-"
    st.session_state.last_gate_angle = 0.0
    st.session_state.last_axis = None
    st.session_state.frames = []
    st.session_state.anim_trigger += 1

# ── Main layout (two columns) ───────────────────────────────────────
col_left, col_right = st.columns([0.35, 0.65])

with col_right:
    state = st.session_state.bloch_state
    x, y, z = state.bloch_vector()

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
    }

    scene_html = build_scene_html(scene_data)
    # Force re-render by embedding trigger in HTML
    scene_html += f"\n<!-- trigger:{st.session_state.anim_trigger} -->\n"
    st.components.v1.html(
        scene_html,
        height=620,
    )

with col_left:
    state = st.session_state.bloch_state
    render_state_display(
        state_text=state.to_ket_text(),
        prob0=state.probabilities()[0],
        prob1=state.probabilities()[1],
        gate_label=st.session_state.last_gate_label,
        gate_angle=st.session_state.last_gate_angle,
        bloch_vector=state.bloch_vector(),
        rotation_axis=st.session_state.last_axis,
    )

    # Gate history
    if len(st.session_state.history) > 1:
        st.markdown("### GATE HISTORY")
        for i, hist_state in enumerate(st.session_state.history):
            if i == 0:
                st.caption(f"Start: {hist_state.to_ket_text()}")
            else:
                st.caption(
                    f"  {i}. [{st.session_state.last_gate_label}] "
                    f"→ {hist_state.to_ket_text()}"
                )

    # Usage guide
    with st.expander("HELP / ABOUT"):
        st.markdown(
            """
            **Bloch Sphere** visualizes single-qubit states as points
            on a unit sphere.

            - **|0⟩**: North pole — Z axis positive
            - **|1⟩**: South pole — Z axis negative
            - **|+⟩**: Equator on +X — equal superposition

            **Gates:**
            - **X/Y/Z**: Pauli gates — π rotation around respective axis
            - **H**: Hadamard — creates superposition
            - **Rx/Ry/Rz**: Parametric rotation — use the angle slider

            **Interaction:**
            - Drag to rotate the 3D view
            - Scroll to zoom in/out
            - Use the animation controls below the sphere
            """
        )

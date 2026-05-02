"""Bloch Sphere -- Interactive Single-Qubit Gate Evolution Demo.

Professional 3D visualization using Streamlit + QuTiP + Three.js.
"""

import streamlit as st
import numpy as np

from quantum import BlochState, get_gate, generate_frames
from ui import inject_styles, render_controls
from ui.display import render_state_display, render_gate_matrix
from visualization import build_scene_html

# ── Page config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bloch Sphere",
    page_icon="",
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
if "last_matrix_tex" not in st.session_state:
    st.session_state.last_matrix_tex = ""
if "frames" not in st.session_state:
    st.session_state.frames = []
if "anim_trigger" not in st.session_state:
    st.session_state.anim_trigger = 0


# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='margin-bottom:0;'>BLOCH SPHERE</h1>"
    "<p style='color:#666;font-size:0.78rem;letter-spacing:2px;margin-top:2px;"
    "margin-bottom:0.5rem;'>"
    "SINGLE-QUBIT GATE EVOLUTION &mdash; INTERACTIVE 3D VISUALIZATION"
    "</p>",
    unsafe_allow_html=True,
)

# ── Controls sidebar ────────────────────────────────────────────────
controls = render_controls()

# ── HELP in sidebar ─────────────────────────────────────────────────
with st.sidebar.expander("REFERENCE"):
    st.markdown(
        """
        **Bloch Sphere** visualizes single-qubit pure states as
        points on the unit sphere S<sup>2</sup>.

        * |0&rang; &mdash; North pole (+Z)
        * |1&rang; &mdash; South pole (-Z)
        * |+&rang; &mdash; Equator at +X

        **Pauli gates** rotate by &pi; around their axis.
        **H** creates equal superposition.
        **Rx/Ry/Rz** accept arbitrary rotation angles.

        Drag to rotate view, scroll to zoom.
        Use controls below the sphere for playback.
        """,
        unsafe_allow_html=True,
    )

# ── Handle initial state change ─────────────────────────────────────
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
    st.session_state.last_matrix_tex = gate["matrix_tex"]
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
    st.session_state.last_matrix_tex = ""
    st.session_state.frames = []
    st.session_state.anim_trigger += 1

# ── Main layout ─────────────────────────────────────────────────────
col_left, col_right = st.columns([0.38, 0.62])

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

    # Gate matrix for the last applied gate
    if st.session_state.last_matrix_tex:
        render_gate_matrix(
            st.session_state.last_gate_label,
            st.session_state.last_matrix_tex,
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
                    f"{hist_state.to_ket_text()}"
                )

    else:
        # Show the matrix for the currently selected gate (preview)
        gate_preview = get_gate(controls["gate"], controls["theta"])
        render_gate_matrix(
            gate_preview["label"],
            gate_preview["matrix_tex"],
        )

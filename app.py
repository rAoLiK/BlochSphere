"""Bloch Sphere -- Interactive Single-Qubit Gate Evolution Demo.

Professional 3D visualization using Streamlit + QuTiP + Three.js.
"""

import streamlit as st
import numpy as np

from quantum import BlochState, generate_chain_frames
from ui import inject_styles, render_controls, render_gate_chain
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
if "last_custom_key" not in st.session_state:
    st.session_state.last_custom_key = None
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

# ── Handle initial state change ─────────────────────────────────
if controls["initial_state"] == "Custom":
    custom_key = (controls["custom_theta"], controls["custom_phi"])
    if st.session_state.get("last_custom_key") != custom_key:
        st.session_state.bloch_state = BlochState(
            theta=controls["custom_theta"],
            phi=controls["custom_phi"],
        )
        st.session_state.last_custom_key = custom_key
        # Clear chain when initial state changes
        st.session_state.chain_frames = []
        st.session_state.chain_boundaries = []
        st.session_state.chain_labels = []
        st.session_state.chain_details = []
        st.session_state.chain_final_state = None
        st.session_state.chain_trigger += 1
else:
    if controls["initial_state"] != st.session_state.bloch_state.to_ket_text():
        label = controls["initial_state"]
        st.session_state.bloch_state = BlochState(label=label)
        st.session_state.last_custom_key = None
        st.session_state.chain_frames = []
        st.session_state.chain_boundaries = []
        st.session_state.chain_labels = []
        st.session_state.chain_details = []
        st.session_state.chain_final_state = None
        st.session_state.chain_trigger += 1

# ── Main layout ─────────────────────────────────────────────────────
col_left, col_right = st.columns([0.38, 0.62])

with col_right:
    state = st.session_state.bloch_state
    x, y, z = state.bloch_vector()

    scene_data = {
        "bloch_vector": [x, y, z],
        "frames": st.session_state.chain_frames,
        "boundaries": st.session_state.chain_boundaries,
        "labels": st.session_state.chain_labels,
        "details": st.session_state.chain_details,
        "speed": controls["speed"],
    }

    scene_html = build_scene_html(scene_data)
    scene_html += f"\n<!-- t:{st.session_state.chain_trigger} -->\n"
    st.components.v1.html(
        scene_html,
        height=620,
    )

with col_left:
    # Show current state info
    state = st.session_state.bloch_state
    render_state_display(
        state_text=state.to_ket_text(),
        prob0=state.probabilities()[0],
        prob1=state.probabilities()[1],
        gate_label=st.session_state.chain_labels[-1] if st.session_state.chain_labels else "-",
        gate_angle=0.0,
        bloch_vector=state.bloch_vector(),
        rotation_axis=None,
    )

    # Show chain final state if chain was applied
    if st.session_state.chain_final_state:
        final = st.session_state.chain_final_state
        render_state_display(
            state_text=final.to_ket_text(),
            prob0=final.probabilities()[0],
            prob1=final.probabilities()[1],
            gate_label=" → ".join(st.session_state.chain_labels) if st.session_state.chain_labels else "-",
            gate_angle=0.0,
            bloch_vector=final.bloch_vector(),
            rotation_axis=None,
        )

# ── Gate chain ──────────────────────────────────────────────────
st.markdown("---")
chain_controls = render_gate_chain()

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

"""Bloch Sphere -- Interactive Single-Qubit Gate Evolution Demo.

Professional 3D visualization using Streamlit + QuTiP + Three.js.
"""

import streamlit as st
import numpy as np

from quantum import BlochState, get_gate, generate_frames, generate_chain_frames
from ui import inject_styles, render_controls, render_chain_controls
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
if "history_labels" not in st.session_state:
    st.session_state.history_labels = ["-"]
if "initial_state_label" not in st.session_state:
    st.session_state.initial_state_label = "|0⟩"
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
        st.session_state.initial_state_label = "Custom"
        st.session_state.history = [st.session_state.bloch_state]
        st.session_state.history_labels = ["-"]
        st.session_state.last_gate_label = "-"
        st.session_state.last_gate_angle = 0.0
        st.session_state.last_axis = None
        st.session_state.last_matrix_tex = ""
        st.session_state.frames = []
        st.session_state.anim_trigger += 1
else:
    if controls["initial_state"] != st.session_state.initial_state_label:
        label = controls["initial_state"]
        st.session_state.bloch_state = BlochState(label=label)
        st.session_state.initial_state_label = label
        st.session_state.last_custom_key = None
        st.session_state.history = [st.session_state.bloch_state]
        st.session_state.history_labels = ["-"]
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
    st.session_state.history_labels.append(gate["label"])
    st.session_state.last_gate_label = gate["label"]
    st.session_state.last_gate_angle = gate["angle"]
    st.session_state.last_axis = gate["axis"]
    st.session_state.last_matrix_tex = gate["matrix_tex"]
    st.session_state.frames = result["frames"]
    st.session_state.chain_frames = []
    st.session_state.chain_boundaries = []
    st.session_state.chain_labels = []
    st.session_state.chain_details = []
    st.session_state.chain_final_state = None
    st.session_state.anim_trigger += 1

# ── Handle reset ────────────────────────────────────────────────────
if controls["reset_clicked"]:
    if controls["initial_state"] == "Custom":
        st.session_state.bloch_state = BlochState(
            theta=controls["custom_theta"],
            phi=controls["custom_phi"],
        )
    else:
        initial_label = controls["initial_state"]
        st.session_state.bloch_state = BlochState(label=initial_label)
    st.session_state.history = [st.session_state.bloch_state]
    st.session_state.history_labels = ["-"]
    st.session_state.last_gate_label = "-"
    st.session_state.last_gate_angle = 0.0
    st.session_state.last_axis = None
    st.session_state.last_matrix_tex = ""
    st.session_state.frames = []
    st.session_state.chain_frames = []
    st.session_state.chain_boundaries = []
    st.session_state.chain_labels = []
    st.session_state.chain_details = []
    st.session_state.chain_final_state = None
    st.session_state.chain_trigger += 1
    st.session_state.anim_trigger += 1

# ── Tab layout ──────────────────────────────────────────────────────
tab_single, tab_chain = st.tabs(["SINGLE GATE", "GATE CHAIN"])

# ── Single Gate Tab ─────────────────────────────────────────────────
with tab_single:
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
            "chain_frames": [],
            "chain_boundaries": [],
            "chain_labels": [],
            "chain_details": [],
        }

        scene_html = build_scene_html(scene_data)
        scene_html += f"\n<!-- t:{st.session_state.anim_trigger}_0 -->\n"
        st.components.v1.html(scene_html, height=560)

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

        if st.session_state.last_matrix_tex:
            render_gate_matrix(
                st.session_state.last_gate_label,
                st.session_state.last_matrix_tex,
            )

        if len(st.session_state.history) > 1:
            st.markdown("### GATE HISTORY")
            rows = []
            for i, hist_state in enumerate(st.session_state.history):
                ket = hist_state.to_ket_text()
                if i == 0:
                    rows.append(f'<div class="hist-row"><span class="hist-idx">0</span>'
                                f'<span class="hist-gate">INIT</span>'
                                f'<span class="hist-ket">{ket}</span></div>')
                else:
                    gate_name = st.session_state.history_labels[i]
                    rows.append(f'<div class="hist-row"><span class="hist-idx">{i}</span>'
                                f'<span class="hist-gate">{gate_name}</span>'
                                f'<span class="hist-ket">{ket}</span></div>')
            st.markdown(
                f'<div class="hist-container">{"".join(rows)}</div>',
                unsafe_allow_html=True,
            )
        else:
            gate_preview = get_gate(controls["gate"], controls["theta"])
            render_gate_matrix(
                gate_preview["label"],
                gate_preview["matrix_tex"],
            )

# ── Gate Chain Tab ──────────────────────────────────────────────────
with tab_chain:
    chain_controls = render_chain_controls()

    if chain_controls["apply_clicked"] and not controls["apply_clicked"] and len(chain_controls["chain_gates"]) > 0:
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

    # Chain 3D scene
    if st.session_state.chain_frames:
        state = st.session_state.bloch_state
        x, y, z = state.bloch_vector()
        scene_data = {
            "bloch_vector": [x, y, z],
            "frames": [],
            "axis": [0, 0, 0],
            "angle": 0,
            "gate_label": "-",
            "prob0": state.probabilities()[0],
            "prob1": state.probabilities()[1],
            "state_text": state.to_ket_text(),
            "speed": controls["speed"],
            "chain_frames": st.session_state.chain_frames,
            "chain_boundaries": st.session_state.chain_boundaries,
            "chain_labels": st.session_state.chain_labels,
            "chain_details": st.session_state.chain_details,
        }
        scene_html = build_scene_html(scene_data)
        scene_html += f"\n<!-- tc:{st.session_state.chain_trigger} -->\n"
        st.components.v1.html(scene_html, height=500)

        # Chain final state
        if st.session_state.chain_final_state:
            final = st.session_state.chain_final_state
            fx, fy, fz = final.bloch_vector()
            fp0, fp1 = final.probabilities()
            st.markdown(
                f'<div class="data-bar">'
                f'<div class="data-item"><div class="data-label">Final State</div>'
                f'<div class="data-value"><span class="ket">{final.to_ket_text()}</span></div></div>'
                f'<div class="data-item"><div class="data-label">Bloch</div>'
                f'<div class="data-value">({fx:.3f}, {fy:.3f}, {fz:.3f})</div></div>'
                f'<div class="data-item"><div class="data-label">P(|0⟩)</div>'
                f'<div class="data-value">{fp0*100:.1f}%</div></div>'
                f'<div class="data-item"><div class="data-label">P(|1⟩)</div>'
                f'<div class="data-value">{fp1*100:.1f}%</div></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

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


CHAIN_GATES = ["X", "Y", "Z", "H", "Rx", "Ry", "Rz"]


def render_chain_controls() -> dict:
    """Render multi-gate chain controls below the main layout.

    Returns dict with keys: chain_gates, apply_clicked, reset_clicked
    """
    if "chain_gates" not in st.session_state:
        st.session_state.chain_gates = [
            {"type": "X", "theta": 0.0, "id": "gate_0"},
        ]

    st.markdown("### MULTI-GATE CHAIN")

    for i, gate_cfg in enumerate(st.session_state.chain_gates):
        gate_type = gate_cfg["type"]
        gate_theta = gate_cfg["theta"]
        if gate_type in ("Rx", "Ry", "Rz"):
            title = f"GATE {i + 1} — {gate_type}({gate_theta:.2f} rad)"
        else:
            title = f"GATE {i + 1} — {gate_type}"

        with st.expander(title, expanded=False):
            new_type = st.radio(
                "Gate type",
                CHAIN_GATES,
                index=CHAIN_GATES.index(gate_type),
                horizontal=True,
                key=f"chain_gate_type_{i}",
                label_visibility="collapsed",
            )
            st.session_state.chain_gates[i]["type"] = new_type

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

            if len(st.session_state.chain_gates) > 1:
                if st.button("REMOVE", key=f"chain_remove_{i}",
                             use_container_width=True):
                    st.session_state.chain_gates.pop(i)
                    st.rerun()

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

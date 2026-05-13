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


def _gate_display_name(gate_cfg: dict) -> str:
    """Return display name for a gate config dict."""
    if gate_cfg["type"] in ("Rx", "Ry", "Rz"):
        return f"{gate_cfg['type']}({np.degrees(gate_cfg['theta']):.0f}°)"
    return gate_cfg["type"]


@st.dialog("GATE CONFIGURATION")
def _configure_gate(index: int):
    """Dialog for configuring a single gate in the chain."""
    gate = st.session_state.chain_gates[index]
    gate_type = gate["type"]
    gate_theta = gate["theta"]

    new_type = st.radio(
        "Gate Type",
        CHAIN_GATES,
        index=CHAIN_GATES.index(gate_type),
        horizontal=True,
    )

    new_theta = 0.0
    if new_type in ("Rx", "Ry", "Rz"):
        angle_deg = st.slider(
            "Rotation Angle (°)",
            min_value=0.0,
            max_value=360.0,
            value=float(np.degrees(gate_theta)),
            step=1.0,
        )
        new_theta = np.radians(angle_deg)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("CONFIRM", use_container_width=True):
            st.session_state.chain_gates[index]["type"] = new_type
            st.session_state.chain_gates[index]["theta"] = new_theta
            st.rerun()
    with col2:
        if st.button("CANCEL", use_container_width=True):
            st.rerun()


def render_chain_controls() -> dict:
    """Render the horizontal gate chain with dialog-based configuration.

    Returns dict with keys: chain_gates, apply_clicked, reset_clicked
    """
    if "chain_gates" not in st.session_state:
        st.session_state.chain_gates = [
            {"type": "X", "theta": 0.0, "id": "gate_0"},
        ]

    st.markdown("### MULTI-GATE CHAIN")

    # Build horizontal chain HTML
    nodes_html = []
    for i, gate_cfg in enumerate(st.session_state.chain_gates):
        name = _gate_display_name(gate_cfg)
        nodes_html.append(
            f'<span class="chain-node" data-idx="{i}">{name}</span>'
        )
        nodes_html.append('<span class="chain-arrow">&rarr;</span>')
    nodes_html.append('<span class="chain-add-node" data-action="add">+</span>')

    chain_html = f'<div class="chain-container">{"".join(nodes_html)}</div>'
    st.markdown(chain_html, unsafe_allow_html=True)

    # Hidden buttons below the chain for click detection
    num_items = len(st.session_state.chain_gates) + 1  # gates + add button
    cols = st.columns(num_items)
    for i in range(len(st.session_state.chain_gates)):
        with cols[i]:
            name = _gate_display_name(st.session_state.chain_gates[i])
            if st.button(name, key=f"chain_node_{i}", use_container_width=True):
                _configure_gate(i)

    # Add gate button
    with cols[len(st.session_state.chain_gates)]:
        if st.button("+", key="chain_add_gate", use_container_width=True):
            new_id = f"gate_{len(st.session_state.chain_gates)}"
            st.session_state.chain_gates.append(
                {"type": "X", "theta": 0.0, "id": new_id}
            )
            st.rerun()

    # Action buttons row
    st.markdown("")
    col_apply, col_reset = st.columns(2)
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

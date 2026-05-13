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
    """Return compact display name for a gate config."""
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


@st.dialog("QUANTUM STATE")
def _show_state_detail():
    """Dialog for showing intermediate quantum state details."""
    idx = st.session_state.get("_show_state_idx", 0)
    states = st.session_state.get("chain_intermediate_states", [])
    if idx < len(states):
        istate = states[idx]
        ket = istate.to_ket_text()
        bx, by, bz = istate.bloch_vector()
        p0, p1 = istate.probabilities()
        st.markdown(f"**State {idx}**")
        st.markdown(f'<span class="ket">{ket}</span>', unsafe_allow_html=True)
        st.markdown(f"**Bloch Vector:** ({bx:.4f}, {by:.4f}, {bz:.4f})")
        st.markdown(f"**P(|0⟩):** {p0*100:.1f}%  **P(|1⟩):** {p1*100:.1f}%")
    if st.button("CLOSE", use_container_width=True):
        st.rerun()


def render_chain_controls(initial_label: str = "|0⟩") -> dict:
    """Render horizontal gate chain with integrated intermediate states.

    Args:
        initial_label: Label for the initial state node at chain start.

    Returns dict with keys: chain_gates, apply_clicked, reset_clicked
    """
    if "chain_gates" not in st.session_state:
        st.session_state.chain_gates = [
            {"type": "X", "theta": 0.0, "id": "gate_0"},
        ]

    gates = st.session_state.chain_gates
    n = len(gates)

    st.markdown("### MULTI-GATE CHAIN")

    # ── Top row: initial label → gate nodes → final label ──
    # Layout: [INIT] [G0] [→] [G1] [→] ... [GN] [+ADD] [FINAL]
    # Count: 1 + n + (n-1) + 1 + 1 = 2n + 2 columns
    top_cols = 1 + n + max(n - 1, 0) + 1 + 1
    cols = st.columns(top_cols)

    # Initial state label
    with cols[0]:
        st.button(initial_label, key="chain_init_label", use_container_width=True, disabled=True)

    # Gate nodes and arrows
    btn_idx = 1
    for i in range(n):
        with cols[btn_idx]:
            name = _gate_display_name(gates[i])
            if st.button(name, key=f"chain_node_{i}", use_container_width=True):
                _configure_gate(i)
        btn_idx += 1
        if i < n - 1:
            with cols[btn_idx]:
                st.markdown('<div style="text-align:center;color:#ff8c00;font-size:1.1rem;'
                            'padding:4px 0;">&rarr;</div>', unsafe_allow_html=True)
            btn_idx += 1

    # Add gate button
    with cols[btn_idx]:
        if st.button("+", key="chain_add_gate", use_container_width=True):
            new_id = f"gate_{n}"
            st.session_state.chain_gates.append(
                {"type": "X", "theta": 0.0, "id": new_id}
            )
            st.rerun()
    btn_idx += 1

    # Final state label
    with cols[btn_idx]:
        final_label = "FINAL"
        if st.session_state.chain_final_state:
            final_label = st.session_state.chain_final_state.to_ket_text()
            if len(final_label) > 8:
                final_label = "FINAL"
        st.button(final_label, key="chain_final_label", use_container_width=True, disabled=True)

    # ── Bottom row: intermediate state numbers ──
    # Only show if chain has been applied
    states = st.session_state.get("chain_intermediate_states", [])
    if states:
        # Aligned with top row: [state0] [→gap] [state1] [→gap] ... [stateN+1]
        num_states = len(states)
        # We need to place state buttons at the arrow positions + start/end
        # Layout mirrors top row: [s0] [s1] [gap] [s2] [gap] ... [sN]
        state_cols = st.columns(top_cols)
        # State 0 at position 0 (under INIT)
        with state_cols[0]:
            if st.button("0", key="inter_state_0", use_container_width=True):
                st.session_state["_show_state_idx"] = 0
                _show_state_detail()
        # States 1..n-1 at arrow positions (between gate nodes)
        state_idx = 1
        col_pos = 1  # after INIT
        for i in range(n):
            col_pos += 1  # skip gate node column
            if i < n - 1:
                # This is an arrow column — place state button here
                with state_cols[col_pos - 1]:
                    if st.button(str(state_idx), key=f"inter_state_{state_idx}",
                                 use_container_width=True):
                        st.session_state["_show_state_idx"] = state_idx
                        _show_state_detail()
                state_idx += 1
        # Final state at the last position
        with state_cols[btn_idx]:
            if st.button(str(num_states - 1), key=f"inter_state_{num_states - 1}",
                         use_container_width=True):
                st.session_state["_show_state_idx"] = num_states - 1
                _show_state_detail()

    # ── Action buttons ──
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

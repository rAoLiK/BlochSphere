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


def _build_chain_html(chain_gates: list[dict]) -> str:
    """Build horizontal chain flow HTML: |ψ₀⟩ → [G1] → [G2] → ... → |ψf⟩"""
    parts = ['<span class="chain-node chain-state">|ψ₀⟩</span>']
    for i, g in enumerate(chain_gates):
        label = g["type"]
        if g["type"] in ("Rx", "Ry", "Rz"):
            label += f'({g["theta"]:.2f})'
        parts.append('<span class="chain-arrow">→</span>')
        parts.append(f'<span class="chain-node chain-gate" data-gate="{i}">{label}</span>')
    parts.append('<span class="chain-arrow">→</span>')
    parts.append('<span class="chain-node chain-state">|ψf⟩</span>')
    return '<div class="chain-flow">' + "".join(parts) + '</div>'


def _compute_intermediate_states(bloch_state, chain_gates: list[dict]) -> list[dict]:
    """Compute quantum state after each gate in the chain."""
    from quantum import BlochState, get_gate
    states = [{"idx": 0, "gate": "-", "ket": bloch_state.to_ket_text(),
               "vec": bloch_state.bloch_vector()}]
    current = bloch_state
    for i, g in enumerate(chain_gates):
        gate = get_gate(g["type"], g.get("theta", 0.0))
        current = current.apply_gate(gate["matrix"])
        states.append({"idx": i + 1, "gate": gate["label"],
                        "ket": current.to_ket_text(), "vec": current.bloch_vector()})
    return states


@st.dialog("GATE CONFIGURATION")
def _gate_config_dialog(gate_idx: int):
    """Popup dialog for configuring a single gate in the chain."""
    cfg = st.session_state.chain_gates[gate_idx]
    st.markdown(f"**GATE {gate_idx + 1}**")

    new_type = st.radio(
        "Type", CHAIN_GATES, index=CHAIN_GATES.index(cfg["type"]),
        horizontal=True, key=f"dlg_gate_type_{gate_idx}",
    )
    new_theta = cfg["theta"]
    if new_type in ("Rx", "Ry", "Rz"):
        angle_deg = st.slider(
            "Angle (°)", 0.0, 360.0,
            value=float(np.degrees(cfg["theta"])), step=1.0,
            key=f"dlg_gate_angle_{gate_idx}",
        )
        new_theta = np.radians(angle_deg)

    if st.button("CONFIRM", use_container_width=True, key=f"dlg_confirm_{gate_idx}"):
        st.session_state.chain_gates[gate_idx]["type"] = new_type
        st.session_state.chain_gates[gate_idx]["theta"] = new_theta
        st.rerun()


def render_chain_controls() -> dict:
    """Render multi-gate chain controls below the main layout.

    Returns dict with keys: chain_gates, apply_clicked, reset_clicked
    """
    if "chain_gates" not in st.session_state:
        st.session_state.chain_gates = [
            {"type": "X", "theta": 0.0, "id": "gate_0"},
        ]

    st.markdown("### GATE CHAIN")

    # ── Horizontal chain flow ─────────────────────────
    chain_html = _build_chain_html(st.session_state.chain_gates)
    st.markdown(chain_html, unsafe_allow_html=True)

    # ── Gate selector (pill buttons) ──────────────────
    gate_labels = []
    for i, g in enumerate(st.session_state.chain_gates):
        lbl = g["type"]
        if g["type"] in ("Rx", "Ry", "Rz"):
            lbl += f'({g["theta"]:.2f})'
        gate_labels.append(f"{i+1}. {lbl}")

    selected = st.radio(
        "Select gate to configure", gate_labels,
        horizontal=True, label_visibility="collapsed",
        key="chain_gate_selector",
    )
    sel_idx = gate_labels.index(selected)

    # ── Selected gate config (opens dialog) ───────────
    cfg = st.session_state.chain_gates[sel_idx]
    cfg_label = cfg["type"]
    if cfg["type"] in ("Rx", "Ry", "Rz"):
        cfg_label += f'({cfg["theta"]:.2f} rad)'

    col_cfg, col_del = st.columns([3, 1])
    with col_cfg:
        st.markdown(
            f'<div class="gate-sel-info">GATE {sel_idx+1}: '
            f'<span class="gate-sel-label">{cfg_label}</span></div>',
            unsafe_allow_html=True,
        )
    with col_del:
        if len(st.session_state.chain_gates) > 1:
            if st.button("REMOVE", key="chain_remove_sel",
                         use_container_width=True):
                st.session_state.chain_gates.pop(sel_idx)
                st.rerun()

    if st.button("CONFIGURE GATE", use_container_width=True,
                 key="chain_open_config"):
        _gate_config_dialog(sel_idx)

    # ── Action buttons ────────────────────────────────
    col_add, col_apply, col_reset = st.columns(3)
    with col_add:
        if st.button("+ ADD GATE", use_container_width=True,
                      key="chain_add_gate"):
            new_id = f"gate_{len(st.session_state.chain_gates)}"
            st.session_state.chain_gates.append(
                {"type": "X", "theta": 0.0, "id": new_id}
            )
            st.rerun()
    with col_apply:
        apply_clicked = st.button("APPLY CHAIN", use_container_width=True,
                                  key="chain_apply")
    with col_reset:
        reset_clicked = st.button("RESET CHAIN", use_container_width=True,
                                  key="chain_reset")
        if reset_clicked:
            st.session_state.chain_gates = [
                {"type": "X", "theta": 0.0, "id": "gate_0"},
            ]

    # ── Intermediate states (compact scrollable) ──────
    from quantum import BlochState
    init_label = st.session_state.get("initial_state_label", "|0⟩")
    if init_label == "Custom":
        t = st.session_state.get("last_custom_key")
        if t:
            init_state = BlochState(theta=t[0], phi=t[1])
        else:
            init_state = BlochState(label="|0⟩")
    else:
        init_state = BlochState(label=init_label)

    intermediates = _compute_intermediate_states(
        init_state, st.session_state.chain_gates
    )

    rows = []
    for s in intermediates:
        x, y, z = s["vec"]
        p0 = (1 + z) / 2 * 100
        gate_badge = (f'<span class="istate-gate">{s["gate"]}</span>'
                      if s["gate"] != "-" else '<span class="istate-init">INIT</span>')
        rows.append(
            f'<div class="istate-row">'
            f'<span class="istate-idx">{s["idx"]}</span>'
            f'{gate_badge}'
            f'<span class="istate-ket">{s["ket"]}</span>'
            f'<span class="istate-vec">({x:.2f},{y:.2f},{z:.2f})</span>'
            f'<span class="istate-prob">|0⟩{p0:.0f}%</span>'
            f'</div>'
        )
    st.markdown("##### STATE EVOLUTION")
    st.markdown(
        f'<div class="istate-container">{"".join(rows)}</div>',
        unsafe_allow_html=True,
    )

    return {
        "chain_gates": list(st.session_state.chain_gates),
        "apply_clicked": apply_clicked,
        "reset_clicked": reset_clicked,
    }

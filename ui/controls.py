"""Sidebar control widgets for Bloch Sphere app."""

import math
import streamlit as st
import numpy as np


INITIAL_STATES = ["|0⟩", "|1⟩", "|+⟩", "|−⟩", "|+i⟩", "|−i⟩", "Custom"]
GATES = ["X", "Y", "Z", "H", "Rx", "Ry", "Rz"]
THEMES = {"Dark": "dark", "Light": "light"}
MAX_GATES_PER_ROW = 6


def render_controls() -> dict:
    """Render sidebar controls and return selections as a dict.

    Returns keys: initial_state, custom_theta, custom_phi, gate, theta,
                  apply_clicked, reset_clicked, playing, speed, theme
    """
    result = {}

    # ── Theme toggle ──────────────────────────────────────
    st.sidebar.markdown("### THEME")
    theme_choice = st.sidebar.radio(
        "Color theme",
        list(THEMES.keys()),
        horizontal=True,
        label_visibility="collapsed",
        key="theme_selector",
    )
    result["theme"] = THEMES[theme_choice]

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
        result["theta"] = 0.0

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


def _gate_label(g: dict) -> str:
    """Short display label for a gate dict."""
    lbl = g["type"]
    if g["type"] in ("Rx", "Ry", "Rz"):
        lbl += f'({g["theta"]:.2f})'
    return lbl


def render_chain_evolution():
    """Render the state evolution table for the current chain configuration."""
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


def render_chain_controls() -> dict:
    """Render multi-gate chain controls below the main layout.

    Grid layout: max 6 gates per row, wraps automatically.
    Each gate is a popover — click to configure type/angle inline.
    Returns dict with keys: chain_gates, apply_clicked, reset_clicked
    """
    # ── Process deferred remove (from popover) ────────
    remove_id = st.session_state.pop("_chain_remove_id", None)
    if remove_id is not None:
        st.session_state.chain_gates = [
            g for g in st.session_state.chain_gates if g["id"] != remove_id
        ]

    st.markdown("### GATE CHAIN")

    gates = st.session_state.chain_gates
    n = len(gates)
    M = MAX_GATES_PER_ROW
    num_rows = math.ceil(n / M) if n > 0 else 1

    # ── Grid chain flow: max M gates per row ───────────
    for row in range(num_rows):
        row_start = row * M
        row_end = min(row_start + M, n)
        row_gates = gates[row_start:row_end]
        is_first = (row == 0)
        is_last = (row == num_rows - 1)

        col_spec = [0.5] + [1] * len(row_gates) + [0.5]
        cols = st.columns(col_spec)

        # Start element
        with cols[0]:
            if is_first:
                st.button("|ψ₀⟩", disabled=True, use_container_width=True,
                          key=f"chain_start_{row}")
            else:
                st.button("↓", disabled=True, use_container_width=True,
                          key=f"chain_down_start_{row}")

        # Gate popovers
        for j, g in enumerate(row_gates):
            with cols[1 + j]:
                label = _gate_label(g)
                with st.popover(f"**{label}**", use_container_width=True, type="primary"):
                    new_type = st.radio(
                        "Type", CHAIN_GATES,
                        index=CHAIN_GATES.index(g["type"]),
                        horizontal=True,
                        key=f"pop_type_{g['id']}",
                    )
                    new_theta = g["theta"]
                    if new_type in ("Rx", "Ry", "Rz"):
                        angle_deg = st.slider(
                            "Angle (°)", 0.0, 360.0,
                            value=float(np.degrees(g["theta"])),
                            step=1.0,
                            key=f"pop_angle_{g['id']}",
                        )
                        new_theta = np.radians(angle_deg)
                    changed = (new_type != g["type"] or
                               abs(new_theta - g["theta"]) > 1e-6)
                    if changed:
                        g["type"] = new_type
                        g["theta"] = new_theta
                        st.rerun()
                    if n > 1:
                        if st.button("REMOVE", key=f"pop_rm_{g['id']}",
                                     use_container_width=True):
                            st.session_state["_chain_remove_id"] = g["id"]
                            st.rerun()

        # End element
        with cols[-1]:
            if is_last:
                st.button("|ψf⟩", disabled=True, use_container_width=True,
                          key=f"chain_end_{row}")
            else:
                st.button("↓", disabled=True, use_container_width=True,
                          key=f"chain_down_end_{row}")

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

    return {
        "chain_gates": list(st.session_state.chain_gates),
        "apply_clicked": apply_clicked,
        "reset_clicked": reset_clicked,
    }

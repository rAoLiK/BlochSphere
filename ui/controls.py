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

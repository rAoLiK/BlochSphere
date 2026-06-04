"""State data display and gate matrix component for Bloch Sphere app."""

import streamlit as st
import numpy as np


def render_state_display(state_text: str, prob0: float, prob1: float,
                         gate_label: str, gate_angle: float,
                         bloch_vector: tuple, rotation_axis: tuple | None = None):
    """Render the data panel with current quantum state information."""

    x, y, z = bloch_vector

    st.markdown("### STATE INFORMATION")

    # Data bar — vertical layout
    st.markdown(
        f"""
        <div class="data-bar data-bar-vertical">
            <div class="data-item">
                <span class="data-label">State</span>
                <span class="data-value"><span class="ket">{state_text}</span></span>
            </div>
            <div class="data-item">
                <span class="data-label">Gate</span>
                <span class="data-value">{gate_label}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Bloch</span>
                <span class="data-value">({x:.3f}, {y:.3f}, {z:.3f})</span>
            </div>
            <div class="data-item">
                <span class="data-label">Norm</span>
                <span class="data-value">{np.sqrt(x**2 + y**2 + z**2):.3f}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Probability display: stacked bar
    p0_pct = prob0 * 100
    p1_pct = prob1 * 100
    st.markdown(
        f"""
        <div class="prob-container">
            <div class="prob-header">Measurement Probabilities</div>
            <div class="prob-bar-outer">
                <div class="prob-bar-0" style="width:{p0_pct:.2f}%;">
                    <span class="prob-bar-label">|0&rang; {p0_pct:.1f}%</span>
                </div>
                <div class="prob-bar-1" style="width:{p1_pct:.2f}%;">
                    <span class="prob-bar-label-dim">{p1_pct:.1f}% |1&rang;</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_gate_matrix(gate_name: str, matrix_tex: str):
    """Display the matrix form of the active gate (LaTeX only)."""
    if not matrix_tex:
        return

    st.markdown("### GATE MATRIX")
    st.markdown('<div class="matrix-display">', unsafe_allow_html=True)
    st.latex(matrix_tex)
    st.markdown('</div>', unsafe_allow_html=True)

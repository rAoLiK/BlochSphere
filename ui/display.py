"""State data display and gate matrix component for Bloch Sphere app."""

import streamlit as st
import numpy as np


def render_state_display(state_text: str, prob0: float, prob1: float,
                         gate_label: str, gate_angle: float,
                         bloch_vector: tuple, rotation_axis: tuple | None = None):
    """Render the data panel with current quantum state information."""

    x, y, z = bloch_vector

    st.markdown("### STATE INFORMATION")

    # Data bar
    st.markdown(
        f"""
        <div class="data-bar">
            <div class="data-item">
                <div class="data-label">Quantum State</div>
                <div class="data-value"><span class="ket">{state_text}</span></div>
            </div>
            <div class="data-item">
                <div class="data-label">Gate Applied</div>
                <div class="data-value">{gate_label}</div>
            </div>
            <div class="data-item">
                <div class="data-label">Bloch Vector</div>
                <div class="data-value">({x:.4f}, {y:.4f}, {z:.4f})</div>
            </div>
            <div class="data-item">
                <div class="data-label">Vector Norm</div>
                <div class="data-value">{np.sqrt(x**2 + y**2 + z**2):.4f}</div>
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

"""State data display and gate matrix component for Bloch Sphere app."""

import streamlit as st
import numpy as np


def render_state_display(state_text: str, prob0: float, prob1: float,
                         gate_label: str, gate_angle: float,
                         bloch_vector: tuple, rotation_axis: tuple | None = None):
    """Render the data panel with current quantum state information."""

    x, y, z = bloch_vector
    p0_pct = prob0 * 100
    p1_pct = prob1 * 100

    st.markdown("### STATE INFORMATION")

    # Data bar
    st.markdown(
        f"""
        <div class="data-bar">
            <div class="data-item">
                <div class="data-label">Quantum State</div>
                <div class="data-value">{state_text}</div>
            </div>
            <div class="data-item">
                <div class="data-label">P(|0⟩)</div>
                <div class="data-value">{p0_pct:.1f}%</div>
            </div>
            <div class="data-item">
                <div class="data-label">P(|1⟩)</div>
                <div class="data-value">{p1_pct:.1f}%</div>
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

    # Probability bars
    st.markdown(
        f"""
        <div style="display:flex; gap:6px; margin-top:4px; font-size:10px;
                    color:#777; text-transform:uppercase; letter-spacing:1px;">
            <div style="flex:{max(p0_pct, 0.5):.0f}; background:#ff6b00; height:3px;
                        transition: flex 0.3s;"></div>
            <div style="flex:{max(p1_pct, 0.5):.0f}; background:#2a2a2a; height:3px;
                        transition: flex 0.3s;"></div>
        </div>
        <div style="display:flex; gap:6px; font-size:10px; color:#555; margin-bottom:0.5rem;">
            <span>|0⟩ {p0_pct:.1f}%</span>
            <span style="margin-left:auto;">{p1_pct:.1f}% |1⟩</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_gate_matrix(gate_name: str, matrix_tex: str):
    """Display the matrix form of the currently selected gate."""
    if not matrix_tex:
        return

    st.markdown("### GATE MATRIX")
    st.markdown(
        f"""
        <div class="matrix-display">
            <div style="color:#777; font-size:0.65rem; text-transform:uppercase;
                        letter-spacing:1px; margin-bottom:4px;">
                {gate_name}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.latex(matrix_tex)

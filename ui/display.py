"""State data display component for Bloch Sphere app."""

import streamlit as st
import numpy as np


def render_state_display(state_text: str, prob0: float, prob1: float,
                         gate_label: str, gate_angle: float,
                         bloch_vector: tuple, rotation_axis: tuple | None = None):
    """Render the bottom data bar with current quantum state information."""

    x, y, z = bloch_vector
    p0_pct = prob0 * 100
    p1_pct = prob1 * 100

    st.markdown(
        f"""
        <div class="data-bar">
            <div class="data-item">
                <div class="data-label">Quantum State |ψ⟩</div>
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
                <div class="data-label">Gate</div>
                <div class="data-value">{gate_label}</div>
            </div>
            <div class="data-item">
                <div class="data-label">Bloch Vector (x, y, z)</div>
                <div class="data-value">({x:.4f}, {y:.4f}, {z:.4f})</div>
            </div>
            <div class="data-item">
                <div class="data-label">Norm |a|</div>
                <div class="data-value">{np.sqrt(x**2 + y**2 + z**2):.4f}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Probability bars
    st.markdown(
        f"""
        <div style="display:flex; gap:8px; margin-top:4px; font-size:11px;
                    color:#888; text-transform:uppercase; letter-spacing:1px;">
            <div style="flex:{p0_pct:.0f}; background:#ff6b00; height:4px;"></div>
            <div style="flex:{p1_pct:.0f}; background:#332211; height:4px;"></div>
        </div>
        <div style="display:flex; gap:8px; font-size:10px; color:#555;
                    margin-bottom:8px;">
            <span>|0⟩ {p0_pct:.1f}%</span>
            <span style="margin-left:auto;">{p1_pct:.1f}% |1⟩</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

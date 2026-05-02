"""Retro-futuristic black-orange styling for the Bloch Sphere app.

Inject via st.markdown with unsafe_allow_html=True.
"""

import streamlit as st

CSS = """
/* ── Global ───────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

* { border-radius: 0 !important; }

body, .stApp {
    background-color: #0a0a0a;
    color: #e0e0e0;
}

.stApp {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
}

/* ── Main container ───────────────────────────────────── */
.main .block-container {
    padding: 1rem 2rem;
    max-width: none;
}

/* ── Header ──────────────────────────────────────────── */
h1, h2, h3, h4 {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    color: #ff6b00 !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 2px solid #ff6b00;
    padding-bottom: 6px;
}

h1 { font-size: 1.6rem !important; }
h3 { font-size: 1.0rem !important; border-bottom-width: 1px; }

/* ── Sidebar ──────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #0d0d0d;
    border-right: 2px solid #ff6b00;
}
[data-testid="stSidebar"] .block-container {
    padding: 1.2rem 1rem;
}
[data-testid="stSidebar"] h3 {
    color: #ff8c00 !important;
    font-size: 0.85rem !important;
    margin-top: 1.2rem;
}

/* ── Buttons ──────────────────────────────────────────── */
.stButton > button {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    background-color: #0a0a0a !important;
    color: #ff6b00 !important;
    border: 2px solid #ff6b00 !important;
    padding: 8px 20px !important;
    font-size: 14px !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #ff6b00 !important;
    color: #0a0a0a !important;
}
.stButton > button:active {
    background-color: #cc5500 !important;
    border-color: #cc5500 !important;
}

/* ── Select / Dropdown ────────────────────────────────── */
.stSelectbox [data-baseweb="select"] {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    background-color: #0a0a0a !important;
    border: 2px solid #ff6b00 !important;
}
.stSelectbox [data-baseweb="select"] * {
    color: #ff6b00 !important;
    background-color: #0a0a0a !important;
    border-color: #ff6b00 !important;
}

/* ── Radio / segmented ────────────────────────────────── */
.stRadio [role="radiogroup"] {
    gap: 4px;
}
.stRadio label {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    background: #0a0a0a !important;
    border: 2px solid #332211 !important;
    color: #ff8c00 !important;
    padding: 6px 12px !important;
    font-size: 13px !important;
    letter-spacing: 1px;
    margin-bottom: 2px !important;
}
.stRadio label:hover {
    border-color: #ff6b00 !important;
    color: #ff6b00 !important;
}
.stRadio label[data-selected="true"] {
    border-color: #ff6b00 !important;
    background: #1a0a00 !important;
    color: #ffaa00 !important;
}

/* ── Slider ───────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] {
    margin-top: 4px;
}
.stSlider [data-baseweb="slider"] [role="slider"] {
    background-color: #ff6b00 !important;
    border: 2px solid #ff6b00 !important;
}
.stSlider [data-baseweb="slider"] div[data-testid="stTickBar"] {
    background: #332211 !important;
    height: 4px !important;
}

/* ── Metric / data display ────────────────────────────── */
[data-testid="stMetric"] {
    background: #0d0d0d;
    border-left: 3px solid #ff6b00;
    padding: 8px 12px;
}
[data-testid="stMetric"] label {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    color: #888 !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    color: #ffaa00 !important;
    font-size: 1.1rem !important;
}

/* ── Data bar at bottom ───────────────────────────────── */
.data-bar {
    background: #0d0d0d;
    border: 2px solid #332211;
    padding: 12px 16px;
    margin-top: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
}
.data-item {
    flex: 1;
    min-width: 180px;
}
.data-label {
    color: #888;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 2px;
}
.data-value {
    color: #ffaa00;
    font-size: 0.95rem;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
}

/* ── Expander ─────────────────────────────────────────── */
.stExpander {
    border: 2px solid #332211 !important;
}
.stExpander summary {
    color: #ff8c00 !important;
}
.stExpander [data-testid="stExpanderDetails"] {
    background: #0d0d0d !important;
}

/* ── Divider ──────────────────────────────────────────── */
hr {
    border-color: #332211 !important;
    margin: 0.8rem 0 !important;
}

/* ── Streamlit overrides ──────────────────────────────── */
footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { background: #0a0a0a; }

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #332211; }
::-webkit-scrollbar-thumb:hover { background: #ff6b00; }

/* ── Code / latex ─────────────────────────────────────── */
code, .katex {
    color: #ffaa00 !important;
}
"""


def inject_styles():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

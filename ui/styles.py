"""Professional black-orange styling for the Bloch Sphere app."""

import streamlit as st

CSS = """
/* ── Global ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

* { border-radius: 0 !important; }

body, .stApp {
    background-color: #0a0a0a;
    color: #d0d0d0;
}

.stApp {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    line-height: 1.5;
}

/* ── Main container ─────────────────────────────────── */
.main .block-container {
    padding: 0.8rem 1.6rem;
    max-width: none;
}

/* ── Header ────────────────────────────────────────── */
h1, h2, h3, h4, h5 {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    color: #ff6b00 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding-bottom: 0.15rem !important;
    margin-bottom: 0.25rem !important;
}

h1 {
    font-size: 2.2rem !important;
    border-bottom: 2px solid #ff6b00;
}

h3 {
    font-size: 0.85rem !important;
    color: #ff8c00 !important;
    margin-top: 1rem;
    border-bottom: 1px solid #332211;
}

/* ── Sidebar ────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #0d0d0d;
    border-right: 2px solid #332211;
}
[data-testid="stSidebar"] .block-container {
    padding: 1rem 0.8rem;
}
[data-testid="stSidebar"] h3 {
    color: #ff8c00 !important;
    font-size: 0.76rem !important;
    margin-top: 0.9rem;
    margin-bottom: 0.2rem !important;
    padding-bottom: 0.12rem !important;
    border-bottom: 1px solid #332211;
    letter-spacing: 1px;
}

/* ── Sidebar spacing fix: prevent divider/control overlap ── */
[data-testid="stSidebar"] .block-container .stMarkdown {
    margin-bottom: 0;
}
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stButton {
    margin-top: 0.15rem;
    margin-bottom: 0.15rem;
}

/* ── Buttons ────────────────────────────────────────── */
.stButton > button {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    background-color: #0a0a0a !important;
    color: #ff6b00 !important;
    border: 2px solid #ff6b00 !important;
    padding: 6px 16px !important;
    font-size: 13px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
    width: 100% !important;
    line-height: 1.3 !important;
}
.stButton > button:hover {
    background-color: #ff6b00 !important;
    color: #0a0a0a !important;
}
.stButton > button:active {
    background-color: #cc5500 !important;
    border-color: #cc5500 !important;
}

/* ── Select / Dropdown ──────────────────────────────── */
.stSelectbox [data-baseweb="select"] {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    background-color: #0a0a0a !important;
    border: 2px solid #443322 !important;
}
.stSelectbox [data-baseweb="select"] * {
    color: #ff8c00 !important;
    background-color: #0a0a0a !important;
    border-color: #443322 !important;
}
.stSelectbox [data-baseweb="select"]:focus-within {
    border-color: #ff6b00 !important;
}

/* ── Radio / segmented ──────────────────────────────── */
.stRadio [role="radiogroup"] {
    gap: 3px;
    flex-wrap: wrap;
}
.stRadio label {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    background: #0a0a0a !important;
    border: 2px solid #332211 !important;
    color: #cc8833 !important;
    padding: 4px 10px !important;
    font-size: 12px !important;
    letter-spacing: 0.5px;
    margin-bottom: 2px !important;
    line-height: 1.4 !important;
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

/* ── Slider ─────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] {
    margin-top: 2px;
}
.stSlider [data-baseweb="slider"] [role="slider"] {
    background-color: #ff6b00 !important;
    border: 2px solid #ff6b00 !important;
}
.stSlider [data-baseweb="slider"] > div:first-child {
    background: #332211 !important;
    height: 4px !important;
}

/* ── Caption ────────────────────────────────────────── */
.stCaption, .stCaptionContainer {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    color: #777 !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.5px;
    line-height: 1.4 !important;
    margin-top: 0.15rem !important;
}

/* ── Data bar ───────────────────────────────────────── */
.data-bar {
    background: #0d0d0d;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #ff6b00;
    padding: 10px 14px;
    margin-top: 0.4rem;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}
.data-item {
    flex: 1;
    min-width: 150px;
}
.data-label {
    color: #777;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1px;
}
.data-value {
    color: #ffaa00;
    font-size: 0.88rem;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    line-height: 1.35;
}

/* ── Probability display ────────────────────────────── */
.prob-container {
    margin-top: 0.5rem;
    background: #0d0d0d;
    border: 1px solid #2a2a2a;
    padding: 12px 14px;
}
.prob-header {
    color: #777;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.prob-bar-outer {
    height: 18px;
    background: #1a1a1a;
    border: 1px solid #333;
    position: relative;
    display: flex;
}
.prob-bar-0 {
    background: #ff6b00;
    transition: width 0.35s ease;
    display: flex; align-items: center;
    justify-content: flex-start; padding-left: 6px;
    overflow: visible; white-space: nowrap;
}
.prob-bar-1 {
    background: transparent;
    transition: width 0.35s ease;
    display: flex; align-items: center;
    justify-content: flex-end; padding-right: 6px;
    overflow: visible; white-space: nowrap;
}
.prob-bar-label {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 10px;
    color: #fff;
    text-shadow: 0 0 4px rgba(0,0,0,0.8);
    letter-spacing: 0.5px;
}
.prob-bar-label-dim {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 10px;
    color: #888;
    letter-spacing: 0.5px;
}

/* ── Ket notation fix ───────────────────────────────── */
.ket {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-feature-settings: "zero";
    font-variant-numeric: tabular-nums;
    letter-spacing: 0;
}

/* ── Gate matrix ────────────────────────────────────── */
.matrix-display {
    margin-top: 0.4rem;
}
.matrix-display .katex {
    color: #ffaa00 !important;
    font-size: 0.95rem !important;
}

/* ── Expander ───────────────────────────────────────── */
.stExpander {
    border: 1px solid #2a2a2a !important;
    margin-top: 0.5rem !important;
}
.stExpander summary {
    color: #ff8c00 !important;
    font-size: 0.76rem !important;
    letter-spacing: 1px;
}
.stExpander [data-testid="stExpanderDetails"] {
    background: #0d0d0d !important;
    font-size: 0.74rem !important;
    line-height: 1.45 !important;
}
.stExpander [data-testid="stExpanderDetails"] p {
    margin: 0.2rem 0 !important;
}

/* ── Divider ────────────────────────────────────────── */
hr, [data-testid="stDivider"] {
    border-color: #2a2a2a !important;
    margin: 0.4rem 0 !important;
}

/* ── Streamlit overrides ────────────────────────────── */
footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { background: #0a0a0a; }

/* ── Scrollbar ──────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; }
::-webkit-scrollbar-thumb:hover { background: #ff6b00; }

/* ── LaTeX / Code ───────────────────────────────────── */
.katex { color: #ffaa00 !important; }
code { color: #ffaa00 !important; }

/* ── Prevent text overflow ──────────────────────────── */
.stMarkdown {
    overflow-wrap: break-word;
    word-break: break-word;
}

/* ── Fix monospace rendering ────────────────────────── */
.stApp, .stMarkdown, [data-testid="stSidebar"] {
    font-kerning: normal;
    font-variant-ligatures: none;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ── Chain section ────────────────────────────────────── */
.chain-gate-expander {
    border: 1px solid #332211 !important;
    margin-bottom: 4px !important;
}
.chain-final-state {
    background: #0d0d0d;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #ff6b00;
    padding: 10px 14px;
    margin-top: 0.5rem;
}
"""


def inject_styles():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

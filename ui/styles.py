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

/* ── Headings ───────────────────────────────────────── */
h1, h2, h3, h4, h5 {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    color: #ff6b00 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

h1 {
    font-size: 1.5rem !important;
    border-bottom: 2px solid #ff6b00;
    padding-bottom: 0.08rem;
    margin-bottom: 0.2rem;
}

h3 {
    font-size: 0.82rem !important;
    color: #ff8c00 !important;
    margin-top: 0.8rem;
    margin-bottom: 0.15rem;
    border-bottom: 1px solid #332211;
    padding-bottom: 0.08rem;
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
    margin-bottom: 0.12rem;
    border-bottom: 1px solid #332211;
    padding-bottom: 0.06rem;
}

/* ── Sidebar REFERENCE expander ─────────────────────── */
[data-testid="stSidebar"] .stExpander {
    border: 1px solid #2a2a2a !important;
    margin-top: 0.8rem !important;
}
[data-testid="stSidebar"] .stExpander summary {
    color: #ff8c00 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stSidebar"] .stExpander [data-testid="stExpanderDetails"] {
    background: #0d0d0d !important;
    font-size: 0.7rem !important;
    line-height: 1.35 !important;
}
[data-testid="stSidebar"] .stExpander p {
    margin: 0.2rem 0 !important;
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
    border: 2px solid #332211 !important;
}
.stSelectbox [data-baseweb="select"] * {
    color: #ff8c00 !important;
    background-color: #0a0a0a !important;
    border-color: #332211 !important;
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
    line-height: 1.35 !important;
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
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1px;
}
.data-value {
    color: #ffaa00;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    line-height: 1.3;
}

/* ── Probability display ────────────────────────────── */
.prob-container {
    margin-top: 0.4rem;
    display: flex;
    align-items: stretch;
    gap: 3px;
    height: 28px;
}
.prob-bar-p0 {
    background: #ff6b00;
    transition: flex 0.4s;
    display: flex;
    align-items: center;
    padding-left: 8px;
}
.prob-bar-p1 {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    transition: flex 0.4s;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 8px;
}
.prob-bar-label {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 11px;
    letter-spacing: 0.5px;
    white-space: nowrap;
}
.prob-bar-label.p0 { color: #0a0a0a; font-weight: 700; }
.prob-bar-label.p1 { color: #777; }

/* ── Expander ───────────────────────────────────────── */
.stExpander {
    border: 1px solid #2a2a2a !important;
    margin-top: 0.5rem !important;
}
.stExpander summary {
    color: #ff8c00 !important;
    font-size: 0.76rem !important;
}
.stExpander [data-testid="stExpanderDetails"] {
    background: #0d0d0d !important;
    font-size: 0.76rem !important;
    line-height: 1.35 !important;
}
.stExpander [data-testid="stExpanderDetails"] p {
    margin: 0.25rem 0 !important;
}

/* ── Divider ────────────────────────────────────────── */
hr, [data-testid="stDivider"] {
    border-color: #2a2a2a !important;
    margin: 0.5rem 0 !important;
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
.katex { color: #ffaa00 !important; font-size: 0.95rem !important; }
code { color: #ffaa00 !important; }

/* ── Sidebar text spacing ───────────────────────────── */
[data-testid="stSidebar"] .stMarkdown p {
    margin: 0.2rem 0 !important;
    line-height: 1.35 !important;
}

/* ── Prevent text overlap ───────────────────────────── */
.stMarkdown {
    overflow-wrap: break-word;
    word-break: break-word;
}

/* ── Ket notation alignment fix ─────────────────────── */
.stApp, .stMarkdown, [data-testid="stSidebar"], .data-value {
    font-kerning: normal;
}
"""


def inject_styles():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

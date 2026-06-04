"""Theme-aware styling for the Bloch Sphere app.

Two themes:
  - dark:  black-orange retro-futuristic (original)
  - light: warm gray + low-saturation red (muted rose accents)

All colors are CSS custom properties so the entire UI switches with one attribute.
"""

import streamlit as st

# ── Font imports ─────────────────────────────────────────────────────
FONTS = (
    "@import url('https://fonts.googleapis.com/css2"
    "?family=Inter:wght@400;500;600;700"
    "&family=JetBrains+Mono:wght@400;500;700&display=swap');"
)

# ── CSS custom properties per theme ─────────────────────────────────
THEME_VARS = {
    "dark": {
        "--bg-root":        "#0a0a0a",
        "--bg-surface":     "#0d0d0d",
        "--bg-raised":      "#131313",
        "--bg-overlay":     "rgba(10,10,10,0.94)",
        "--text-primary":   "#e0e0e0",
        "--text-secondary": "#999999",
        "--text-muted":     "#666666",
        "--text-disabled":  "#444444",
        "--accent":         "#ff6b00",
        "--accent-hover":   "#ff8c00",
        "--accent-glow":    "#ffaa00",
        "--accent-dim":     "#cc5500",
        "--accent-bg":      "#1a0a00",
        "--accent-border":  "#332211",
        "--border":         "#2a2a2a",
        "--border-light":   "#1e1e1e",
        "--bar-fill":       "#ff6b00",
        "--bar-track":      "#1a1a1a",
        "--shadow":         "rgba(255,107,0,0.08)",
        "--shadow-strong":  "rgba(255,107,0,0.18)",
        "--header-border":  "#ff6b00",
        "--scrollbar":      "#2a2a2a",
        "--scrollbar-hover":"#ff6b00",
    },
    "light": {
        "--bg-root":        "#e4dfda",
        "--bg-surface":     "#eae6e1",
        "--bg-raised":      "#e0dbd5",
        "--bg-overlay":     "rgba(234,230,225,0.96)",
        "--text-primary":   "#2c2424",
        "--text-secondary": "#5c5050",
        "--text-muted":     "#8a7c7c",
        "--text-disabled":  "#b8acac",
        "--accent":         "#a0403a",
        "--accent-hover":   "#b54a44",
        "--accent-glow":    "#c46860",
        "--accent-dim":     "#8a3630",
        "--accent-bg":      "#f0e2e0",
        "--accent-border":  "#d8c0bc",
        "--border":         "#cdc4be",
        "--border-light":   "#d8d0ca",
        "--bar-fill":       "#a0403a",
        "--bar-track":      "#d8d0ca",
        "--shadow":         "rgba(160,64,58,0.06)",
        "--shadow-strong":  "rgba(160,64,58,0.14)",
        "--header-border":  "#a0403a",
        "--scrollbar":      "#c0b6ae",
        "--scrollbar-hover":"#a0403a",
    },
}


def _build_theme_css(theme: str) -> str:
    """Return the full CSS string for the given theme ('dark' or 'light')."""
    v = THEME_VARS[theme]
    is_light = theme == "light"

    # ── Light-mode overrides (text color only) ──────────────────
    light_overrides = ""
    if is_light:
        light_overrides = """
/* Light mode: force text dark */
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stCaptionContainer,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] [data-baseweb],
[data-testid="stSidebar"] [data-baseweb] *,
.main .block-container *,
.main .block-container p,
.main .block-container span,
.main .block-container label,
.main .block-container .stMarkdown,
.main .block-container .stMarkdown p {
    color: var(--text-primary) !important;
}
"""

    return f"""{FONTS}

/* ════════════════════════════════════════════════════════
   Theme: {theme}
   ════════════════════════════════════════════════════════ */

:root {{
    --font-ui:    'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono:  'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace;

    --text-xs:    0.68rem;
    --text-sm:    0.76rem;
    --text-base:  0.84rem;
    --text-lg:    1.00rem;
    --text-xl:    1.30rem;
    --text-2xl:   1.50rem;

    --leading-tight:  1.3;
    --leading-normal: 1.5;
    --leading-loose:  1.65;

    --tracking-tight:  0.3px;
    --tracking-normal: 0.5px;
    --tracking-wide:   1.0px;
    --tracking-wider:  1.5px;

    --radius-sm:  4px;
    --radius-md:  6px;
    --radius-lg:  8px;

    {chr(10).join(f'    {k}: {v};' for k, v in v.items())}
}}

/* ── Global ──────────────────────────────────────────── */
/* border-radius only on containers, not spinners/icons */
.stButton > button,
[data-testid="stDownloadButton"] button,
[data-testid="stDownloadButton"] a,
.stTextInput > div,
.stSelectbox > div,
.stSlider,
.stRadio > div,
.stExpander,
.stTabs,
[data-baseweb="tab"],
[data-baseweb="popover"],
[data-baseweb="modal"],
.stAlert,
.stToast {{
    border-radius: var(--radius-sm) !important;
}}

body, .stApp {{
    background-color: var(--bg-root);
    color: var(--text-primary);
    font-family: var(--font-ui);
    font-size: var(--text-base);
    line-height: var(--leading-normal);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

.stApp {{ overflow-x: hidden; }}

/* ── Main container — compact ────────────────────────── */
.main .block-container {{
    padding: 0.5rem 1.4rem 0.6rem;
    max-width: none;
}}

/* ── Headings ────────────────────────────────────────── */
h1, h2, h3, h4, h5 {{
    font-family: var(--font-mono) !important;
    color: var(--accent) !important;
    text-transform: uppercase;
    letter-spacing: var(--tracking-wider);
    padding-bottom: 0.1rem !important;
    margin-bottom: 0.15rem !important;
}}

h1 {{
    font-size: var(--text-2xl) !important;
    font-weight: 700;
    letter-spacing: 2px;
    border-bottom: 2px solid var(--header-border);
    margin-bottom: 0 !important;
}}

h3 {{
    font-size: var(--text-sm) !important;
    color: var(--accent-hover) !important;
    font-weight: 600;
    margin-top: 0.6rem;
    border-bottom: 1px solid var(--border);
}}

h5 {{
    font-size: var(--text-sm) !important;
    color: var(--accent-hover) !important;
    margin-top: 0.5rem;
}}

/* ── Header subtitle ─────────────────────────────────── */
.header-sub {{
    color: var(--text-muted);
    font-family: var(--font-ui);
    font-size: 0.64rem;
    letter-spacing: var(--tracking-wider);
    margin-top: 1px;
    margin-bottom: 0.3rem;
    text-transform: uppercase;
}}

/* ── Sidebar — compact ───────────────────────────────── */
[data-testid="stSidebar"] {{
    background-color: var(--bg-surface);
    border-right: 2px solid var(--border);
}}
[data-testid="stSidebar"] .block-container {{
    padding: 0.6rem 0.7rem;
}}
[data-testid="stSidebar"] h3 {{
    color: var(--accent-hover) !important;
    font-size: 0.68rem !important;
    font-weight: 600;
    margin-top: 0.6rem;
    margin-bottom: 0.1rem !important;
    padding-bottom: 0.08rem !important;
    border-bottom: 1px solid var(--border);
    letter-spacing: var(--tracking-wide);
}}
[data-testid="stSidebar"] .block-container .stMarkdown {{
    margin-bottom: 0;
}}
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stButton {{
    margin-top: 0.1rem;
    margin-bottom: 0.1rem;
}}

/* ── Buttons ─────────────────────────────────────────── */
.stButton > button {{
    font-family: var(--font-mono) !important;
    font-weight: 500;
    background-color: var(--bg-root) !important;
    color: var(--accent) !important;
    border: 1.5px solid var(--accent) !important;
    border-radius: var(--radius-md) !important;
    padding: 5px 14px !important;
    font-size: var(--text-sm) !important;
    text-transform: uppercase !important;
    letter-spacing: var(--tracking-wider) !important;
    transition: all 0.18s ease !important;
    cursor: pointer !important;
    width: 100% !important;
    line-height: var(--leading-tight) !important;
}}
.stButton > button:hover {{
    background-color: var(--accent) !important;
    color: var(--bg-root) !important;
    box-shadow: 0 2px 10px var(--shadow-strong) !important;
    transform: translateY(-1px);
}}
.stButton > button:active {{
    background-color: var(--accent-dim) !important;
    border-color: var(--accent-dim) !important;
    transform: translateY(0);
}}

/* ── Select / Dropdown ───────────────────────────────── */
.stSelectbox [data-baseweb="select"] {{
    font-family: var(--font-ui) !important;
    font-size: var(--text-base);
    background-color: var(--bg-surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
}}
.stSelectbox [data-baseweb="select"] * {{
    color: var(--accent-hover) !important;
    background-color: var(--bg-surface) !important;
    border-color: var(--border) !important;
}}
.stSelectbox [data-baseweb="select"]:focus-within {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--shadow) !important;
}}

/* ── Radio / segmented ───────────────────────────────── */
.stRadio [role="radiogroup"] {{
    gap: 3px;
    flex-wrap: wrap;
}}
.stRadio label {{
    font-family: var(--font-mono) !important;
    font-weight: 500;
    background: var(--bg-surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-secondary) !important;
    padding: 3px 10px !important;
    font-size: 11px !important;
    letter-spacing: var(--tracking-normal);
    margin-bottom: 1px !important;
    line-height: var(--leading-tight) !important;
    transition: all 0.15s ease;
}}
.stRadio label:hover {{
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}}
.stRadio label[data-selected="true"] {{
    border-color: var(--accent) !important;
    background: var(--accent-bg) !important;
    color: var(--accent-glow) !important;
    box-shadow: 0 1px 4px var(--shadow);
}}

/* ── Slider ──────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] {{
    margin-top: 1px;
}}
.stSlider [data-baseweb="slider"] [role="slider"] {{
    background-color: var(--accent) !important;
    border: 2px solid var(--accent) !important;
}}
.stSlider [data-baseweb="slider"] > div:first-child {{
    background: var(--accent-border) !important;
    height: 4px !important;
    border-radius: 2px !important;
}}

/* ── Caption ─────────────────────────────────────────── */
.stCaption, .stCaptionContainer {{
    font-family: var(--font-ui) !important;
    color: var(--text-muted) !important;
    font-size: var(--text-xs) !important;
    letter-spacing: var(--tracking-normal);
    line-height: var(--leading-normal) !important;
    margin-top: 0.1rem !important;
}}

/* ── Data bar ────────────────────────────────────────── */
.data-bar {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius-md) !important;
    padding: 8px 12px;
    margin-top: 0.3rem;
}}
.data-bar-vertical {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}
.data-bar-vertical .data-item {{
    display: flex;
    align-items: baseline;
    gap: 8px;
}}
.data-bar-vertical .data-label {{
    min-width: 42px;
    flex-shrink: 0;
}}
.data-item {{
    flex: 1;
    min-width: 120px;
}}
.data-label {{
    color: var(--text-muted);
    font-family: var(--font-ui);
    font-size: 0.58rem;
    text-transform: uppercase;
    letter-spacing: var(--tracking-wider);
    margin-bottom: 1px;
    font-weight: 600;
}}
.data-value {{
    color: var(--accent-glow);
    font-size: var(--text-sm);
    font-family: var(--font-mono);
    line-height: var(--leading-tight);
    font-weight: 500;
}}

/* ── Probability display ─────────────────────────────── */
.prob-container {{
    margin-top: 0.3rem;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md) !important;
    padding: 8px 12px;
}}
.prob-header {{
    color: var(--text-muted);
    font-family: var(--font-ui);
    font-size: 0.58rem;
    text-transform: uppercase;
    letter-spacing: var(--tracking-wider);
    margin-bottom: 6px;
    font-weight: 600;
}}
.prob-bar-outer {{
    height: 16px;
    background: var(--bar-track);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm) !important;
    position: relative;
    display: flex;
    overflow: hidden;
}}
.prob-bar-0 {{
    background: var(--bar-fill);
    transition: width 0.35s ease;
    display: flex; align-items: center;
    justify-content: flex-start; padding-left: 6px;
    overflow: visible; white-space: nowrap;
}}
.prob-bar-1 {{
    background: transparent;
    transition: width 0.35s ease;
    display: flex; align-items: center;
    justify-content: flex-end; padding-right: 6px;
    overflow: visible; white-space: nowrap;
}}
.prob-bar-label {{
    font-family: var(--font-mono);
    font-size: 9px;
    font-weight: 500;
    color: #fff;
    text-shadow: 0 0 4px rgba(0,0,0,0.6);
    letter-spacing: var(--tracking-normal);
}}
.prob-bar-label-dim {{
    font-family: var(--font-mono);
    font-size: 9px;
    font-weight: 500;
    color: var(--text-muted);
    letter-spacing: var(--tracking-normal);
}}

/* ── Ket notation ────────────────────────────────────── */
.ket {{
    font-family: var(--font-mono);
    font-feature-settings: "zero";
    font-variant-numeric: tabular-nums;
    letter-spacing: 0;
    font-weight: 500;
}}

/* ── Gate matrix ─────────────────────────────────────── */
.matrix-display {{
    margin-top: 0.3rem;
}}
.matrix-display .katex {{
    color: var(--accent-glow) !important;
    font-size: 0.9rem !important;
}}

/* ── Expander ────────────────────────────────────────── */
.stExpander {{
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    margin-top: 0.3rem !important;
}}
.stExpander summary,
.stExpander[open] summary {{
    color: var(--accent-hover) !important;
    font-family: var(--font-mono) !important;
    font-size: var(--text-sm) !important;
    font-weight: 600;
    letter-spacing: var(--tracking-wide);
}}
.stExpander [data-testid="stExpanderDetails"] {{
    background: var(--bg-surface) !important;
    font-size: var(--text-sm) !important;
    line-height: var(--leading-loose) !important;
}}
.stExpander [data-testid="stExpanderDetails"] p {{
    margin: 0.15rem 0 !important;
}}

/* ── Divider ─────────────────────────────────────────── */
hr, [data-testid="stDivider"] {{
    border-color: var(--border) !important;
    margin: 0.3rem 0 !important;
}}

/* ── Streamlit overrides ─────────────────────────────── */
footer {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}
#MainMenu {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: var(--bg-root); }}

/* ── Dialog backdrop — frosted glass ─────────────────── */
[data-baseweb="modal-backdrop"],
div[data-baseweb="modal-backdrop"] {{
    background-color: rgba(0,0,0,0.12) !important;
    backdrop-filter: blur(10px) saturate(1.2) !important;
    -webkit-backdrop-filter: blur(10px) saturate(1.2) !important;
}}

/* ── Scrollbar ───────────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: var(--bg-root); }}
::-webkit-scrollbar-thumb {{ background: var(--scrollbar); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--scrollbar-hover); }}

/* ── LaTeX / Code ────────────────────────────────────── */
.katex {{ color: var(--accent-glow) !important; }}
code {{ color: var(--accent-glow) !important; }}

/* ── Prevent text overflow ───────────────────────────── */
.stMarkdown {{
    overflow-wrap: break-word;
    word-break: break-word;
}}

/* ── Gate history ────────────────────────────────────── */
.hist-container {{
    max-height: 360px;
    overflow-y: auto;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius-md) !important;
    background: var(--bg-surface);
    padding: 0;
    margin-top: 0.3rem;
}}
.hist-container::-webkit-scrollbar {{ width: 4px; }}
.hist-container::-webkit-scrollbar-track {{ background: var(--bg-surface); }}
.hist-container::-webkit-scrollbar-thumb {{ background: var(--border); }}
.hist-container::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

.hist-row {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 2px 10px;
    border-bottom: 1px solid var(--border-light);
    font-family: var(--font-mono);
    font-size: 0.7rem;
    line-height: 1.5;
}}
.hist-row:last-child {{ border-bottom: none; }}
.hist-row:nth-child(odd) {{ background: var(--bg-raised); }}

.hist-idx {{
    color: var(--text-disabled);
    min-width: 18px;
    text-align: right;
    font-variant-numeric: tabular-nums;
    font-size: var(--text-xs);
}}
.hist-gate {{
    color: var(--accent-hover);
    font-weight: 700;
    min-width: 40px;
    letter-spacing: var(--tracking-normal);
}}
.hist-ket {{
    color: var(--accent-glow);
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

/* ── Chain: disabled state buttons (|ψ₀⟩, |ψf⟩, ↓) ──── */
.stButton > button:disabled {{
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    color: var(--accent) !important;
    background: var(--accent-bg) !important;
    border: 1.5px solid var(--accent) !important;
    border-radius: var(--radius-sm) !important;
    letter-spacing: var(--tracking-normal) !important;
    opacity: 1 !important;
    cursor: default !important;
    text-transform: none !important;
}}

/* ── Popover trigger styled as gate node ─────────────── */
[data-baseweb="popover"] > div > button,
[data-baseweb="popover"] button[data-baseweb="button"] {{
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    padding: 4px 10px !important;
    background: var(--accent) !important;
    color: var(--bg-root) !important;
    border: 1.5px solid var(--accent) !important;
    border-radius: var(--radius-sm) !important;
    letter-spacing: var(--tracking-normal) !important;
    text-transform: none !important;
    white-space: nowrap !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
    width: 100%;
    overflow: hidden;
}}
[data-baseweb="popover"] > div > button:hover,
[data-baseweb="popover"] button[data-baseweb="button"]:hover {{
    box-shadow: 0 2px 8px var(--shadow-strong) !important;
    transform: translateY(-1px);
}}
[data-baseweb="popover"] > div > button::after,
[data-baseweb="popover"] button[data-baseweb="button"]::after {{
    content: ' ▾';
    font-size: 0.55em;
    opacity: 0.7;
    margin-left: 2px;
}}
[data-baseweb="popover"] > [data-baseweb="popover"] {{
    background: var(--bg-surface) !important;
}}
.gate-sel-info {{
    font-family: var(--font-ui);
    font-size: var(--text-sm);
    color: var(--text-secondary);
    padding: 4px 0;
}}
.gate-sel-label {{
    color: var(--accent-hover);
    font-family: var(--font-mono);
    font-weight: 700;
}}

/* ── State evolution (compact) ───────────────────────── */
.istate-container {{
    max-height: 420px;
    overflow-y: auto;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius-md) !important;
    background: var(--bg-surface);
    margin-top: 0.3rem;
}}
.istate-container::-webkit-scrollbar {{ width: 4px; }}
.istate-container::-webkit-scrollbar-track {{ background: var(--bg-surface); }}
.istate-container::-webkit-scrollbar-thumb {{ background: var(--border); }}
.istate-container::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

.istate-row {{
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 1px 8px;
    border-bottom: 1px solid var(--border-light);
    font-family: var(--font-mono);
    font-size: 0.64rem;
    line-height: 1.5;
}}
.istate-row:last-child {{ border-bottom: none; }}
.istate-row:nth-child(even) {{ background: var(--bg-raised); }}

.istate-idx {{
    color: var(--text-disabled);
    min-width: 14px;
    text-align: right;
    font-variant-numeric: tabular-nums;
}}
.istate-init {{
    color: var(--text-muted);
    min-width: 30px;
    font-size: 0.58rem;
    letter-spacing: var(--tracking-normal);
}}
.istate-gate {{
    color: var(--bg-root);
    background: var(--accent);
    padding: 0 4px;
    min-width: 30px;
    text-align: center;
    font-weight: 700;
    font-size: 0.58rem;
    border-radius: var(--radius-sm) !important;
}}
.istate-ket {{
    color: var(--accent-glow);
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.istate-vec {{
    color: var(--text-muted);
    font-size: 0.58rem;
    white-space: nowrap;
}}
.istate-prob {{
    color: var(--accent-hover);
    font-size: 0.58rem;
    min-width: 44px;
    text-align: right;
    white-space: nowrap;
    font-weight: 500;
}}

/* ── Tabs ────────────────────────────────────────────── */
.stTabs [data-baseweb="tab"] {{
    font-family: var(--font-mono) !important;
    font-size: var(--text-sm) !important;
    letter-spacing: var(--tracking-wide);
    padding: 4px 12px !important;
    color: var(--text-secondary) !important;
}}
.stTabs [aria-selected="true"] {{
    color: var(--accent) !important;
}}
.stTabs [data-baseweb="tab-border"] {{
    background-color: var(--accent) !important;
}}

/* ── Accent-colored elements ────────────────────────── */
[data-testid="stSidebar"] h3,
.main h1, .main h2, .main h3, .main h4, .main h5,
.header-sub,
.gate-sel-label,
.data-label,
.prob-header {{
    color: var(--accent) !important;
}}

/* Secondary/muted text */
.data-label,
.prob-header,
.istate-idx,
.istate-init,
.istate-vec,
.hist-idx,
.caption,
.stCaption,
.stCaptionContainer {{
    color: var(--text-muted) !important;
}}

/* Data values accent-glow */
.data-value,
.ket,
.hist-ket,
.istate-ket,
.istate-prob {{
    color: var(--accent-glow) !important;
}}

/* ── Buttons ────────────────────────────────────────── */
.stButton > button:not(:disabled) {{
    background-color: var(--bg-surface) !important;
    color: var(--accent) !important;
}}
.stButton > button:not(:disabled):hover,
.stButton > button:not(:disabled):active {{
    background-color: var(--accent) !important;
    color: #ffffff !important;
    border-color: var(--accent) !important;
}}
.stButton > button:not(:disabled):focus {{
    outline: none !important;
    box-shadow: none !important;
}}
.stButton > button:disabled {{
    color: var(--accent) !important;
    background: var(--accent-bg) !important;
    border-color: var(--accent) !important;
    opacity: 1 !important;
}}

/* Download button — nuclear reset */
[data-testid="stDownloadButton"] button,
[data-testid="stDownloadButton"] a {{
    all: unset !important;
    background: var(--bg-surface) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 0.25rem !important;
    padding: 0.375rem 1rem !important;
    font-family: inherit !important;
    font-size: inherit !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    box-sizing: border-box !important;
}}
[data-testid="stDownloadButton"] button:hover,
[data-testid="stDownloadButton"] button:active,
[data-testid="stDownloadButton"] a:hover,
[data-testid="stDownloadButton"] a:active {{
    all: unset !important;
    background: var(--accent) !important;
    color: #ffffff !important;
    border: 1px solid var(--accent) !important;
    border-radius: 0.25rem !important;
    padding: 0.375rem 1rem !important;
    font-family: inherit !important;
    font-size: inherit !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    box-sizing: border-box !important;
}}
[data-testid="stDownloadButton"] button:focus,
[data-testid="stDownloadButton"] a:focus {{
    outline: none !important;
    box-shadow: none !important;
}}

/* Radio buttons */
.stRadio label {{
    color: var(--text-secondary) !important;
}}
.stRadio label[data-selected="true"] {{
    border-color: var(--accent) !important;
    background: var(--accent-bg) !important;
    color: var(--accent) !important;
}}

/* Selectbox */
.stSelectbox [data-baseweb="select"] * {{
    color: var(--text-primary) !important;
}}
.stSelectbox [data-baseweb="select"] {{
    background-color: var(--bg-surface) !important;
}}

/* Slider */
.stSlider [data-baseweb="slider"] > div:first-child {{
    background: var(--border) !important;
}}

/* Popover trigger */
[data-baseweb="popover"] > div > button,
[data-baseweb="popover"] button[data-baseweb="button"] {{
    background: var(--accent) !important;
    color: var(--bg-root) !important;
    border: 1.5px solid var(--accent) !important;
    box-shadow: none !important;
}}
[data-baseweb="popover"] > div > button:hover,
[data-baseweb="popover"] button[data-baseweb="button"]:hover {{
    background: var(--accent-dim) !important;
    color: #ffffff !important;
    border-color: var(--accent-dim) !important;
    box-shadow: 0 2px 8px var(--shadow-strong) !important;
}}

/* Gate badges */
.istate-gate,
.chain-gate {{
    color: #ffffff !important;
}}

/* Expander */
.stExpander summary,
.stExpander summary *,
.stExpander summary h1,
.stExpander summary h2,
.stExpander summary h3,
.stExpander summary h4,
.stExpander summary h5,
.stExpander summary p,
.stExpander summary span,
.stExpander summary div,
.stExpander[open] summary,
.stExpander[open] summary *,
.stExpander[open] summary h1,
.stExpander[open] summary h2,
.stExpander[open] summary h3,
.stExpander[open] summary h4,
.stExpander[open] summary h5,
.stExpander[open] summary p,
.stExpander[open] summary span,
.stExpander[open] summary div {{
    color: var(--accent) !important;
    background-color: transparent !important;
}}
.stExpander [data-testid="stExpanderDetails"],
.stExpander [data-testid="stExpanderDetails"] p,
.stExpander [data-testid="stExpanderDetails"] li,
.stExpander [data-testid="stExpanderDetails"] strong {{
    color: var(--text-primary) !important;
}}
.stExpander [data-testid="stExpanderDetails"] code {{
    color: var(--accent-glow) !important;
}}

/* ── Dropdown / Popover portals ─────────────────────── */
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="select"] [data-baseweb="popover"],
[data-baseweb="select"] [data-baseweb="menu"],
ul[data-baseweb="menu"],
div[data-baseweb="popover"] {{
    background-color: var(--bg-surface) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}}
[data-baseweb="popover"] li,
[data-baseweb="menu"] li,
[data-baseweb="popover"] [role="option"],
[data-baseweb="menu"] [role="option"],
ul[data-baseweb="menu"] li,
[data-baseweb="select"] [role="option"],
[data-baseweb="select"] li {{
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
}}
[data-baseweb="popover"] li:hover,
[data-baseweb="menu"] li:hover,
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="select"] [role="option"]:hover,
[data-baseweb="select"] li:hover,
[data-baseweb="popover"] [aria-selected="true"],
[data-baseweb="menu"] [aria-selected="true"],
[data-baseweb="select"] [aria-selected="true"] {{
    background-color: var(--accent-bg) !important;
    color: var(--accent) !important;
}}
[data-baseweb="popover"] [data-highlighted="true"],
[data-baseweb="menu"] [data-highlighted="true"] {{
    background-color: var(--accent-bg) !important;
    color: var(--accent) !important;
}}
.stSelectbox [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="select"] input,
.stSelectbox [data-baseweb="select"] [class*="ValueContainer"],
.stSelectbox [data-baseweb="select"] [class*="singleValue"],
.stSelectbox [data-baseweb="select"] [class*="placeholder"] {{
    color: var(--text-primary) !important;
    background-color: var(--bg-surface) !important;
}}

/* ── Dialog / Modal ─────────────────────────────────── */
[data-baseweb="modal"],
[data-baseweb="modal"] [role="dialog"],
[data-testid="stDialog"],
[data-testid="stDialog"] [role="dialog"],
[data-baseweb="modal"] [data-baseweb="modal-content"],
div[data-baseweb="modal"] {{
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
}}
[data-baseweb="modal"] *,
[data-testid="stDialog"] *,
[data-baseweb="modal"] p,
[data-baseweb="modal"] label,
[data-baseweb="modal"] span,
[data-baseweb="modal"] div,
[data-baseweb="modal"] strong,
[data-baseweb="modal"] em,
[data-testid="stDialog"] p,
[data-testid="stDialog"] label,
[data-testid="stDialog"] span,
[data-testid="stDialog"] div {{
    color: var(--text-primary) !important;
}}
[data-baseweb="modal"] h1,
[data-baseweb="modal"] h2,
[data-baseweb="modal"] h3,
[data-baseweb="modal"] h4,
[data-baseweb="modal"] h5,
[data-testid="stDialog"] h1,
[data-testid="stDialog"] h2,
[data-testid="stDialog"] h3,
[data-testid="stDialog"] h4,
[data-testid="stDialog"] h5 {{
    color: var(--accent) !important;
}}
[data-baseweb="modal-backdrop"],
div[data-baseweb="modal-backdrop"] {{
    background-color: rgba(180,170,160,0.25) !important;
    backdrop-filter: blur(14px) saturate(1.1) !important;
}}
[data-baseweb="modal"] .stButton > button,
[data-testid="stDialog"] .stButton > button {{
    background-color: var(--bg-surface) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
}}
[data-baseweb="modal"] .stButton > button:hover,
[data-testid="stDialog"] .stButton > button:hover {{
    background-color: var(--accent) !important;
    color: #ffffff !important;
}}
[data-baseweb="modal"] .stRadio label,
[data-testid="stDialog"] .stRadio label {{
    background: var(--bg-root) !important;
    color: var(--text-secondary) !important;
    border-color: var(--border) !important;
}}
[data-baseweb="modal"] .stRadio label[data-selected="true"],
[data-testid="stDialog"] .stRadio label[data-selected="true"] {{
    background: var(--accent-bg) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
}}
[data-baseweb="modal"] .stSlider [data-baseweb="slider"] > div:first-child,
[data-testid="stDialog"] .stSlider [data-baseweb="slider"] > div:first-child {{
    background: var(--border) !important;
}}
[data-baseweb="modal"]::-webkit-scrollbar,
[data-testid="stDialog"]::-webkit-scrollbar {{
    width: 5px;
}}
[data-baseweb="modal"]::-webkit-scrollbar-track,
[data-testid="stDialog"]::-webkit-scrollbar-track {{
    background: var(--bg-surface);
}}
[data-baseweb="modal"]::-webkit-scrollbar-thumb,
[data-testid="stDialog"]::-webkit-scrollbar-thumb {{
    background: var(--scrollbar);
    border-radius: 3px;
}}

/* ── Popover / portal containers ────────────────────── */
[data-baseweb="layer"],
[data-baseweb="popover"] [data-baseweb="popover"],
div[data-baseweb="popover"] {{
    background-color: var(--bg-surface) !important;
}}
[data-baseweb="popover"] [data-baseweb="popover"] p,
[data-baseweb="popover"] [data-baseweb="popover"] span,
[data-baseweb="popover"] [data-baseweb="popover"] label,
[data-baseweb="popover"] [data-baseweb="popover"] div,
[data-baseweb="popover"] [data-baseweb="popover"] strong {{
    color: var(--text-primary) !important;
}}
[data-baseweb="popover"] [data-baseweb="popover"] label {{
    background: var(--bg-root) !important;
    color: var(--text-secondary) !important;
    border-color: var(--border) !important;
}}
[data-baseweb="popover"] [data-baseweb="popover"] label[data-selected="true"] {{
    background: var(--accent-bg) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
}}
[data-baseweb="popover"] [data-baseweb="popover"] [data-baseweb="slider"] {{
    background: var(--border) !important;
}}
[data-baseweb="popover"] [data-baseweb="popover"] .stButton > button:not(:disabled) {{
    background-color: var(--bg-root) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
}}
[data-baseweb="popover"] [data-baseweb="popover"] .stButton > button:not(:disabled):hover {{
    background-color: var(--accent) !important;
    color: #ffffff !important;
}}

/* Popover: radio buttons */
[data-baseweb="popover"] .stRadio label,
[data-baseweb="popover"] [data-baseweb="popover"] .stRadio label {{
    background: var(--bg-root) !important;
    color: var(--text-secondary) !important;
    border-color: var(--border) !important;
}}
[data-baseweb="popover"] .stRadio label[data-selected="true"],
[data-baseweb="popover"] [data-baseweb="popover"] .stRadio label[data-selected="true"] {{
    background: var(--accent-bg) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
}}

/* Popover: slider */
[data-baseweb="popover"] .stSlider [data-baseweb="slider"] > div:first-child,
[data-baseweb="popover"] [data-baseweb="popover"] .stSlider [data-baseweb="slider"] > div:first-child {{
    background: var(--border) !important;
}}

/* Popover: caption / markdown text */
[data-baseweb="popover"] .stCaption,
[data-baseweb="popover"] [data-baseweb="popover"] .stCaption,
[data-baseweb="popover"] p,
[data-baseweb="popover"] [data-baseweb="popover"] p,
[data-baseweb="popover"] span,
[data-baseweb="popover"] [data-baseweb="popover"] span,
[data-baseweb="popover"] label,
[data-baseweb="popover"] [data-baseweb="popover"] label {{
    color: var(--text-primary) !important;
}}

/* Tooltip */
[data-baseweb="tooltip"],
[data-baseweb="tooltip"] * {{
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    border-color: var(--border) !important;
}}

/* Toast */
[data-baseweb="notification"],
[data-baseweb="toast"] {{
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
}}

{light_overrides}
"""


def inject_styles(theme: str = "dark"):
    """Inject the full CSS for the given theme into the Streamlit page."""
    if theme not in THEME_VARS:
        theme = "dark"
    css = _build_theme_css(theme)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    if theme == "light":
        st.html("""
<style id="light-popover-css">
[data-baseweb="popover"][data-baseweb="popover"][data-baseweb="popover"] {
    background-color: #eae6e1 !important;
}
[data-baseweb="layer"][data-baseweb="layer"] {
    background-color: #eae6e1 !important;
}
</style>
<script>
(function() {
    var BG = '#eae6e1';
    var TXT = '#2c2424';
    var ACC = '#a0403a';
    var ABG = '#f0e2e0';
    var BDR = '#cdc4be';
    var ROOT_BG = '#e4dfda';

    function s(el, prop, val) {
        el.style.setProperty(prop, val, 'important');
    }

    function stylePopover(container) {
        if (!container || container._styled) return;
        container._styled = true;
        s(container, 'background-color', BG);
        s(container, 'color', TXT);
        s(container, 'border-color', BDR);

        var all = container.getElementsByTagName('*');
        for (var i = 0; i < all.length; i++) {
            var c = all[i];
            if (c.tagName === 'INPUT' || c.tagName === 'TEXTAREA') continue;
            var inR = c.closest && c.closest('[data-baseweb="radio"]');
            var inS = c.closest && c.closest('[data-baseweb="slider"]');
            if (!inR && !inS && !c.matches('button')) {
                s(c, 'background-color', 'transparent');
            }
            s(c, 'color', TXT);
        }

        var radios = container.querySelectorAll('[data-baseweb="radio"]');
        for (var j = 0; j < radios.length; j++) {
            s(radios[j], 'background-color', ROOT_BG);
            s(radios[j], 'color', TXT);
            s(radios[j], 'border-color', BDR);
        }
        var checked = container.querySelectorAll('[data-baseweb="radio"][aria-checked="true"]');
        for (var k = 0; k < checked.length; k++) {
            s(checked[k], 'background-color', ABG);
            s(checked[k], 'color', ACC);
            s(checked[k], 'border-color', ACC);
        }

        var sliders = container.querySelectorAll('[data-baseweb="slider"]');
        for (var m = 0; m < sliders.length; m++) {
            var track = sliders[m].querySelector('div');
            if (track) s(track, 'background-color', BDR);
        }
    }

    function scan() {
        document.querySelectorAll('[data-baseweb="popover"]').forEach(function(p) {
            if (p.querySelector('[data-baseweb="radio"]') || p.querySelector('[data-baseweb="slider"]'))
                stylePopover(p);
        });
        document.querySelectorAll('[data-baseweb="layer"]').forEach(stylePopover);
    }

    scan();
    new MutationObserver(scan).observe(document.body, {childList: true, subtree: true});
    setInterval(scan, 500);
})();
</script>""", unsafe_allow_javascript=True)

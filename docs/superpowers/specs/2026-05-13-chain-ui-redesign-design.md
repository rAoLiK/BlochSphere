# Multi-Gate Chain UI Redesign

## Overview

Replace the current expander-based chain controls with a horizontal node-chain layout. Gate names serve as clickable nodes connected by arrows, simulating a physics process flow. Gate configuration uses `@st.dialog` popups. Intermediate quantum states are displayed below the chain as numbered expandable entries.

All UI text is in English.

## Layout

```
MULTI-GATE CHAIN

[ H ] → [ Rx(1.57) ] → [ Z ] → [ + ]    [APPLY] [RESET]

── Intermediate States ──────────────────────
[0] |0⟩                         ← click to expand
[1] 0.707|0⟩ + 0.707|1⟩
[2] ...
```

## Components

### 1. Horizontal Chain (HTML/CSS)

Rendered as an HTML string via `st.markdown(unsafe_allow_html=True)`.

Each gate is a clickable `<span>` with class `chain-node`:
- Black background, orange border, JetBrains Mono font
- Gate name centered (e.g., `H`, `Rx(1.57)`)
- On click: triggers `@st.dialog` via a hidden Streamlit button overlaid on the node

Nodes are connected by `→` arrows (CSS `::after` pseudo-element or `&rarr;` entity).

The last node is a `+` button (dashed border) to add a new gate.

APPLY CHAIN and RESET CHAIN are standard `st.button()` on the same row.

### 2. Gate Configuration Dialog (@st.dialog)

```python
@st.dialog("GATE CONFIGURATION")
def configure_gate(index: int):
    gate = st.session_state.chain_gates[index]
    new_type = st.radio("Gate Type", CHAIN_GATES, ...)
    if new_type in ("Rx", "Ry", "Rz"):
        angle = st.slider("Angle (°)", 0, 360, ...)
    col1, col2 = st.columns(2)
    if col1.button("CONFIRM"):
        # update session_state.chain_gates[index]
        st.rerun()
    if col2.button("CANCEL"):
        st.rerun()
```

Triggered by clicking a gate node. The dialog reads/writes `st.session_state.chain_gates[i]`.

### 3. Intermediate States

Below the chain, render a row of numbered buttons: `[0] [1] [2] ...`

Each number maps to the quantum state AFTER that many gates have been applied:
- `0` = initial state (before any gate)
- `1` = after gate 1
- `N` = after gate N

Clicking a number expands an `st.expander` showing:
- Ket notation text
- Bloch vector (x, y, z)
- Measurement probabilities P(|0⟩), P(|1⟩)

Data source: `generate_chain_frames` already computes per-gate `final_state`. We extract intermediate states from the chain computation.

### 4. Session State

Existing keys unchanged:
- `chain_gates`: list of `{"type", "theta", "id"}` dicts
- `chain_frames`, `chain_boundaries`, `chain_labels`, `chain_details`
- `chain_final_state`, `chain_trigger`

New key:
- `chain_intermediate_states`: list of `BlochState` objects (one per gate boundary, including initial state)

Computed when APPLY CHAIN is clicked, alongside `generate_chain_frames`.

## Data Flow

```
User clicks gate node → @st.dialog opens
  → User configures type/angle → CONFIRM
  → session_state.chain_gates[i] updated

User clicks APPLY CHAIN
  → generate_chain_frames(bloch_state, chain_gates)
  → Extract intermediate states from per-gate final_state
  → Store in session_state
  → st.rerun()

User clicks numbered button [N]
  → st.expander shows intermediate state N details
```

## Style

All CSS follows existing retro-futuristic black-orange theme:
- Chain nodes: `border: 2px solid #ff6b00`, `background: #0a0a0a`, `color: #ff6b00`
- Arrows: `color: #ff8c00`, `→` entity
- Add node: `border: 2px dashed #666`, `color: #666`
- Intermediate state buttons: same style as existing buttons
- Dialog: inherits Streamlit dialog styling with CSS overrides for theme consistency

## File Changes

| File | Change |
|------|--------|
| `ui/controls.py` | Replace `render_chain_controls()` with new HTML chain + dialog logic |
| `ui/styles.py` | Add CSS for chain nodes, arrows, add button, intermediate states |
| `app.py` | Extract intermediate states from chain computation |

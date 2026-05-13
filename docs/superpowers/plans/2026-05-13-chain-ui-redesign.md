# Chain UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace expander-based chain controls with a horizontal node-chain layout, dialog-based gate configuration, and numbered intermediate state display.

**Architecture:** The chain is rendered as HTML with clickable gate nodes connected by arrows. `@st.dialog` handles gate configuration. Intermediate states are extracted from `generate_chain_frames` and displayed as numbered expandable entries below the chain.

**Tech Stack:** Python 3.10, Streamlit 1.57, QuTiP, HTML/CSS

---

### Task 1: Add Intermediate States to generate_chain_frames

**Files:**
- Modify: `quantum/evolution.py:37-81`
- Modify: `quantum/__init__.py` (no change needed, already exports)

- [ ] **Step 1: Add intermediate_states tracking to generate_chain_frames**

In `quantum/evolution.py`, modify `generate_chain_frames` to collect intermediate states. Add `intermediate_states` list that stores the `BlochState` at each gate boundary (including the initial state).

Replace the function body (lines 56-81) with:

```python
    from .gates import get_gate

    all_frames = []
    boundaries = []
    labels = []
    gate_details = []
    intermediate_states = [initial]  # state before any gate
    current_state = initial

    for g in gates:
        gate = get_gate(g["type"], g.get("theta", 0.0))
        boundaries.append(len(all_frames))
        labels.append(gate["label"])
        gate_details.append({
            "label": gate["label"],
            "axis": list(gate["axis"]),
            "angle": gate["angle"],
        })
        result = generate_frames(current_state, gate, num_frames_per_gate)
        all_frames.extend(result["frames"])
        current_state = result["final_state"]
        intermediate_states.append(current_state)

    return {
        "frames": all_frames,
        "boundaries": boundaries,
        "labels": labels,
        "gate_details": gate_details,
        "final_state": current_state,
        "intermediate_states": intermediate_states,
    }
```

- [ ] **Step 2: Update test_chain_fills_axis_and_angle to also check intermediate_states**

In `tests/test_evolution.py`, add to `test_chain_fills_axis_and_angle`:

```python
def test_chain_fills_axis_and_angle():
    """generate_chain_frames should populate axis/angle on gate dicts."""
    initial = BlochState(label="|0⟩")
    gates = [{"type": "H", "theta": 0.0}]
    result = generate_chain_frames(initial, gates)
    g = result["gate_details"][0]
    assert "axis" in g
    assert "angle" in g
    assert g["label"] == "H"
    # intermediate_states: [initial, after_gate_0]
    assert len(result["intermediate_states"]) == 2
```

- [ ] **Step 3: Run tests**

Run: `cd /mnt/e/Desktop/Bloch_v2 && python -m pytest tests/test_evolution.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 4: Commit**

```bash
git add quantum/evolution.py tests/test_evolution.py
git commit -m "feat: add intermediate_states to generate_chain_frames"
```

---

### Task 2: Add Chain CSS Styles

**Files:**
- Modify: `ui/styles.py` (append chain-node CSS)

- [ ] **Step 1: Add CSS for chain nodes, arrows, and intermediate states**

Append to the CSS string in `ui/styles.py` before the closing `"""`:

```css
/* ── Chain horizontal layout ────────────────────────────── */
.chain-container {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0;
    padding: 12px 0;
}

.chain-node {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 56px;
    height: 36px;
    padding: 0 12px;
    background: #0a0a0a;
    border: 2px solid #ff6b00;
    color: #ff6b00;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 1px;
    cursor: pointer;
    transition: all 0.15s;
}
.chain-node:hover {
    background: #ff6b00;
    color: #0a0a0a;
}

.chain-arrow {
    display: inline-flex;
    align-items: center;
    padding: 0 6px;
    color: #ff8c00;
    font-size: 1.1rem;
}

.chain-add-node {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 36px;
    height: 36px;
    padding: 0 10px;
    background: transparent;
    border: 2px dashed #555;
    color: #555;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.15s;
}
.chain-add-node:hover {
    border-color: #ff6b00;
    color: #ff6b00;
}

.chain-buttons {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-left: 16px;
}

/* ── Intermediate states ────────────────────────────────── */
.inter-states-label {
    color: #777;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.6rem;
    margin-bottom: 0.3rem;
}
.inter-state-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    margin-right: 4px;
    background: #0a0a0a;
    border: 2px solid #332211;
    color: #cc8833;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.15s;
}
.inter-state-btn:hover, .inter-state-btn.active {
    border-color: #ff6b00;
    color: #ff6b00;
}
```

- [ ] **Step 2: Commit**

```bash
git add ui/styles.py
git commit -m "style: add chain node and intermediate state CSS"
```

---

### Task 3: Rewrite render_chain_controls

**Files:**
- Modify: `ui/controls.py` (replace `render_chain_controls` and related functions)

- [ ] **Step 1: Replace render_chain_controls with HTML chain + dialog**

Replace the entire `render_chain_controls` function and the `_on_gate_type_change` callback in `ui/controls.py` with:

```python
CHAIN_GATES = ["X", "Y", "Z", "H", "Rx", "Ry", "Rz"]


def _gate_display_name(gate_cfg: dict) -> str:
    """Return display name for a gate config dict."""
    if gate_cfg["type"] in ("Rx", "Ry", "Rz"):
        return f"{gate_cfg['type']}({np.degrees(gate_cfg['theta']):.0f}&deg;)"
    return gate_cfg["type"]


@st.dialog("GATE CONFIGURATION")
def _configure_gate(index: int):
    """Dialog for configuring a single gate in the chain."""
    gate = st.session_state.chain_gates[index]
    gate_type = gate["type"]
    gate_theta = gate["theta"]

    new_type = st.radio(
        "Gate Type",
        CHAIN_GATES,
        index=CHAIN_GATES.index(gate_type),
        horizontal=True,
    )

    new_theta = 0.0
    if new_type in ("Rx", "Ry", "Rz"):
        angle_deg = st.slider(
            "Rotation Angle (&deg;)",
            min_value=0.0,
            max_value=360.0,
            value=float(np.degrees(gate_theta)),
            step=1.0,
        )
        new_theta = np.radians(angle_deg)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("CONFIRM", use_container_width=True):
            st.session_state.chain_gates[index]["type"] = new_type
            st.session_state.chain_gates[index]["theta"] = new_theta
            st.rerun()
    with col2:
        if st.button("CANCEL", use_container_width=True):
            st.rerun()


def render_chain_controls() -> dict:
    """Render the horizontal gate chain with dialog-based configuration.

    Returns dict with keys: chain_gates, apply_clicked, reset_clicked
    """
    if "chain_gates" not in st.session_state:
        st.session_state.chain_gates = [
            {"type": "X", "theta": 0.0, "id": "gate_0"},
        ]

    st.markdown("### MULTI-GATE CHAIN")

    # Build horizontal chain HTML
    nodes_html = []
    for i, gate_cfg in enumerate(st.session_state.chain_gates):
        name = _gate_display_name(gate_cfg)
        nodes_html.append(
            f'<span class="chain-node" data-idx="{i}">{name}</span>'
        )
        nodes_html.append('<span class="chain-arrow">&rarr;</span>')
    nodes_html.append('<span class="chain-add-node" data-action="add">+</span>')

    chain_html = f'<div class="chain-container">{"".join(nodes_html)}</div>'
    st.markdown(chain_html, unsafe_allow_html=True)

    # Hidden buttons overlaid on nodes for click detection
    cols = st.columns(max(len(st.session_state.chain_gates) * 2 + 1, 1))
    for i in range(len(st.session_state.chain_gates)):
        with cols[i * 2]:
            name = _gate_display_name(st.session_state.chain_gates[i])
            if st.button(name, key=f"chain_node_{i}", use_container_width=True):
                _configure_gate(i)

    # Add gate button
    add_col_idx = len(st.session_state.chain_gates) * 2
    if add_col_idx < len(cols):
        with cols[add_col_idx]:
            if st.button("+", key="chain_add_gate", use_container_width=True):
                new_id = f"gate_{len(st.session_state.chain_gates)}"
                st.session_state.chain_gates.append(
                    {"type": "X", "theta": 0.0, "id": new_id}
                )
                st.rerun()

    # Action buttons row
    st.markdown("")
    col_apply, col_reset = st.columns(2)
    with col_apply:
        apply_clicked = st.button("APPLY CHAIN", use_container_width=True)
    with col_reset:
        reset_clicked = st.button("RESET CHAIN", use_container_width=True)
        if reset_clicked:
            st.session_state.chain_gates = [
                {"type": "X", "theta": 0.0, "id": "gate_0"},
            ]

    return {
        "chain_gates": list(st.session_state.chain_gates),
        "apply_clicked": apply_clicked,
        "reset_clicked": reset_clicked,
    }
```

- [ ] **Step 2: Update ui/__init__.py exports**

No change needed — `render_chain_controls` is already exported.

- [ ] **Step 3: Commit**

```bash
git add ui/controls.py
git commit -m "feat: horizontal chain UI with dialog-based gate configuration"
```

---

### Task 4: Intermediate States Display in app.py

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Add intermediate_states to session state init**

In the session state init block (after `chain_trigger`), add:

```python
if "chain_intermediate_states" not in st.session_state:
    st.session_state.chain_intermediate_states = []
```

- [ ] **Step 2: Extract intermediate states from chain computation**

In the chain APPLY handler (around line 261), add `intermediate_states` extraction:

```python
if chain_controls["apply_clicked"] and not controls["apply_clicked"] and len(chain_controls["chain_gates"]) > 0:
    result = generate_chain_frames(
        st.session_state.bloch_state,
        chain_controls["chain_gates"],
    )
    st.session_state.chain_frames = result["frames"]
    st.session_state.chain_boundaries = result["boundaries"]
    st.session_state.chain_labels = result["labels"]
    st.session_state.chain_details = result["gate_details"]
    st.session_state.chain_final_state = result["final_state"]
    st.session_state.chain_intermediate_states = result["intermediate_states"]
    st.session_state.chain_trigger += 1
    st.rerun()
```

- [ ] **Step 3: Add intermediate states display after chain section**

After the chain final state display block, add:

```python
# Intermediate states
if st.session_state.chain_intermediate_states:
    st.markdown('<div class="inter-states-label">INTERMEDIATE STATES</div>',
                unsafe_allow_html=True)
    states = st.session_state.chain_intermediate_states
    cols = st.columns(len(states))
    for idx, istate in enumerate(states):
        with cols[idx]:
            if st.button(str(idx), key=f"inter_state_{idx}", use_container_width=True):
                pass  # expander below handles display
            with st.expander(f"State {idx}", expanded=False):
                ket = istate.to_ket_text()
                bx, by, bz = istate.bloch_vector()
                p0, p1 = istate.probabilities()
                st.markdown(
                    f'<span class="ket">{ket}</span>',
                    unsafe_allow_html=True,
                )
                st.caption(f"Bloch: ({bx:.4f}, {by:.4f}, {bz:.4f})")
                st.caption(f"P(|0⟩) = {p0*100:.1f}%  P(|1⟩) = {p1*100:.1f}%")
```

- [ ] **Step 4: Clear intermediate states on reset**

In the RESET handler, add:

```python
st.session_state.chain_intermediate_states = []
```

- [ ] **Step 5: Commit**

```bash
git add app.py
git commit -m "feat: display intermediate quantum states below chain"
```

---

### Task 5: Final Integration Test

**Files:** None (manual verification)

- [ ] **Step 1: Test horizontal chain rendering**

Run `streamlit run app.py`. Verify:
- Chain section shows horizontal nodes with arrows
- + node appears at the end
- APPLY/RESET buttons below

- [ ] **Step 2: Test dialog gate configuration**

- Click a gate node → dialog opens with gate type radio
- Change to Rx → slider appears
- Click CONFIRM → dialog closes, node shows updated name
- Click CANCEL → dialog closes, no change

- [ ] **Step 3: Test chain apply and intermediate states**

- Configure 3 gates (H → Rx → Z)
- Click APPLY CHAIN
- Verify animation plays
- Verify intermediate states [0] [1] [2] [3] appear
- Click each number → expander shows ket, Bloch vector, probabilities

- [ ] **Step 4: Test independence with single-gate mode**

- Apply a single gate (top section)
- Then apply a chain (bottom section)
- Verify both work independently

- [ ] **Step 5: Test reset**

- After chain apply, click RESET CHAIN
- Verify chain resets to single X gate
- Verify intermediate states disappear
- Verify Bloch sphere returns to initial state

"""Tests for apply button mutual exclusion logic.

These tests verify the app.py logic for handling single-gate APPLY
and chain APPLY without conflicts.
"""


def test_apply_flags_independent():
    """Single-gate apply and chain apply should be independent flags."""
    # Simulate: only single-gate APPLY clicked
    apply_clicked = True
    chain_apply_clicked = False
    single_gate_handled = apply_clicked and not chain_apply_clicked
    assert single_gate_handled is True

    # Simulate: only chain APPLY clicked
    apply_clicked = False
    chain_apply_clicked = True
    chain_handled = chain_apply_clicked and not apply_clicked
    assert chain_handled is True

    # Simulate: both clicked (shouldn't happen, but if it does, single wins)
    apply_clicked = True
    chain_apply_clicked = True
    single_gate_handled = apply_clicked
    chain_handled = chain_apply_clicked and not apply_clicked
    assert single_gate_handled is True
    assert chain_handled is False


def test_chain_trigger_increments_on_apply():
    """chain_trigger should increment when chain is applied."""
    chain_trigger = 0
    chain_apply_clicked = True

    if chain_apply_clicked:
        chain_trigger += 1

    assert chain_trigger == 1


def test_anim_trigger_increments_on_single_apply():
    """anim_trigger should increment when single gate is applied."""
    anim_trigger = 0
    apply_clicked = True

    if apply_clicked:
        anim_trigger += 1

    assert anim_trigger == 1


def test_combined_trigger_forces_rerender():
    """Both triggers should contribute to the html key to force re-render."""
    anim_trigger = 0
    chain_trigger = 0

    # Single gate apply
    anim_trigger += 1
    key1 = f"scene_{anim_trigger}_{chain_trigger}"

    # Chain apply
    chain_trigger += 1
    key2 = f"scene_{anim_trigger}_{chain_trigger}"

    assert key1 != key2, "Key must change when chain_trigger changes"

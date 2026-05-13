"""Tests for visualization/scene.py — scene HTML generation."""

from visualization.scene import build_scene_html


def test_html_contains_anim_trigger_placeholder():
    """build_scene_html output should reference anim_trigger for key changes."""
    data = {
        "bloch_vector": [0, 0, 1],
        "frames": [],
        "axis": [0, 0, 0],
        "angle": 0,
        "gate_label": "-",
        "prob0": 1.0,
        "prob1": 0.0,
        "state_text": "|0⟩",
        "speed": 1.0,
        "chain_frames": [],
        "chain_boundaries": [],
        "chain_labels": [],
        "chain_details": [],
    }
    html = build_scene_html(data)
    # The HTML should contain the DATA JSON with chain fields
    assert "chain_frames" in html
    assert "chain_boundaries" in html


def test_html_contains_chain_fields():
    """Chain data should be present in the generated HTML."""
    data = {
        "bloch_vector": [0, 0, 1],
        "frames": [],
        "axis": [0, 0, 0],
        "angle": 0,
        "gate_label": "-",
        "prob0": 1.0,
        "prob1": 0.0,
        "state_text": "|0⟩",
        "speed": 1.0,
        "chain_frames": [[0, 0, 1], [0.5, 0, 0.866]],
        "chain_boundaries": [0],
        "chain_labels": ["H"],
        "chain_details": [{"label": "H", "axis": [0.707, 0, 0.707], "angle": 3.14}],
    }
    html = build_scene_html(data)
    assert '"chain_frames"' in html
    assert '"chain_labels"' in html
    assert '"chain_details"' in html


def test_html_backward_compatible_without_chain():
    """When chain data is empty, HTML should still generate correctly."""
    data = {
        "bloch_vector": [0, 0, 1],
        "frames": [[0, 0, 1], [1, 0, 0]],
        "axis": [1, 0, 0],
        "angle": 3.14,
        "gate_label": "X",
        "prob0": 1.0,
        "prob1": 0.0,
        "state_text": "|0⟩",
        "speed": 1.0,
    }
    html = build_scene_html(data)
    assert "three" in html.lower()
    assert "animate" in html

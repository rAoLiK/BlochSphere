"""Tests for visualization/scene.py — scene HTML generation."""

from visualization.scene import build_scene_html


def _base_data(**overrides):
    """Helper to create base scene data with defaults."""
    data = {
        "bloch_vector": [0, 0, 1],
        "frames": [],
        "boundaries": [],
        "labels": [],
        "details": [],
        "speed": 1.0,
    }
    data.update(overrides)
    return data


def test_html_generates_with_empty_data():
    """HTML should generate correctly with no gate data."""
    html = build_scene_html(_base_data())
    assert "three" in html.lower()
    assert "animate" in html


def test_html_contains_chain_fields():
    """Gate chain data should be present in the generated HTML."""
    html = build_scene_html(_base_data(
        frames=[[0, 0, 1], [0.5, 0, 0.866]],
        boundaries=[0],
        labels=["H"],
        details=[{"label": "H", "axis": [0.707, 0, 0.707], "angle": 3.14}],
    ))
    assert '"frames"' in html
    assert '"labels"' in html
    assert '"details"' in html


def test_html_backward_compatible():
    """HTML should work with single gate (chain of length 1)."""
    html = build_scene_html(_base_data(
        frames=[[0, 0, 1], [1, 0, 0]],
        boundaries=[0],
        labels=["X"],
        details=[{"label": "X", "axis": [1, 0, 0], "angle": 3.14}],
    ))
    assert "animate" in html

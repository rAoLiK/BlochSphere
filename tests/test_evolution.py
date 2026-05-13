import numpy as np
from quantum.state import BlochState
from quantum.gates import get_gate
from quantum.evolution import generate_chain_frames


def test_chain_single_gate():
    """Chain with one gate should match single gate result."""
    initial = BlochState(label="|0⟩")
    gates = [{"type": "X", "theta": 0.0}]
    result = generate_chain_frames(initial, gates)
    assert len(result["frames"]) == 81
    assert len(result["boundaries"]) == 1
    assert result["boundaries"][0] == 0
    assert result["labels"] == ["X"]
    x, y, z = result["final_state"].bloch_vector()
    assert abs(z + 1.0) < 1e-10


def test_chain_multiple_gates():
    """Chain with two gates should concatenate frames."""
    initial = BlochState(label="|0⟩")
    gates = [
        {"type": "X", "theta": 0.0},
        {"type": "Z", "theta": 0.0},
    ]
    result = generate_chain_frames(initial, gates)
    assert len(result["frames"]) == 162
    assert result["boundaries"] == [0, 81]
    assert result["labels"] == ["X", "Z"]


def test_chain_rx_gate_with_angle():
    """Chain with Rx gate should use the specified angle."""
    initial = BlochState(label="|0⟩")
    gates = [{"type": "Rx", "theta": np.pi}]
    result = generate_chain_frames(initial, gates, num_frames_per_gate=10)
    x, y, z = result["final_state"].bloch_vector()
    assert abs(z + 1.0) < 1e-6


def test_chain_preserves_state_continuity():
    """Each gate should start where the previous one ended."""
    initial = BlochState(label="|0⟩")
    gates = [
        {"type": "X", "theta": 0.0},
        {"type": "Y", "theta": 0.0},
    ]
    result = generate_chain_frames(initial, gates, num_frames_per_gate=10)
    boundary = result["boundaries"][1]
    f0_end = result["frames"][boundary - 1]
    f1_start = result["frames"][boundary]
    for a, b in zip(f0_end, f1_start):
        assert abs(a - b) < 1e-10


def test_chain_fills_axis_and_angle():
    """generate_chain_frames should populate axis/angle on gate dicts."""
    initial = BlochState(label="|0⟩")
    gates = [{"type": "H", "theta": 0.0}]
    result = generate_chain_frames(initial, gates)
    g = result["gate_details"][0]
    assert "axis" in g
    assert "angle" in g
    assert g["label"] == "H"
    assert len(result["intermediate_states"]) == 2


def test_chain_intermediate_states():
    """generate_chain_frames should return intermediate states including initial."""
    initial = BlochState(label="|0⟩")
    gates = [{"type": "X", "theta": 0.0}, {"type": "Z", "theta": 0.0}]
    result = generate_chain_frames(initial, gates)
    # 3 states: initial, after X, after Z
    assert len(result["intermediate_states"]) == 3
    # First state is |0⟩
    x0, y0, z0 = result["intermediate_states"][0].bloch_vector()
    assert abs(z0 - 1.0) < 1e-10
    # After X: |1⟩
    x1, y1, z1 = result["intermediate_states"][1].bloch_vector()
    assert abs(z1 + 1.0) < 1e-10

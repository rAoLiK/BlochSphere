import numpy as np
from qutip import Qobj, sigmax, sigmay, sigmaz, identity

from .state import BlochState


def generate_frames(initial: BlochState, gate: dict, num_frames: int = 60) -> dict:
    """Generate animation frames for a gate applied to an initial state.

    Returns dict with:
        frames: list of (x, y, z) tuples for each interpolation step
        axis: rotation axis (ax, ay, az)
        total_angle: total rotation angle in radians
        final_state: final BlochState after gate application
    """
    axis = gate["axis"]
    total_angle = gate["angle"]

    frames = []
    for i in range(num_frames + 1):
        t = i / num_frames
        theta = total_angle * t
        partial_gate = _build_partial_rotation(axis, theta)
        intermediate = initial.apply_gate(partial_gate)
        frames.append(intermediate.bloch_vector())

    final_state = initial.apply_gate(gate["matrix"])

    return {
        "frames": frames,
        "axis": axis,
        "total_angle": total_angle,
        "final_state": final_state,
    }


def generate_chain_frames(initial: BlochState, gates: list[dict],
                          num_frames_per_gate: int = 80) -> dict:
    """Compute animation frames for a chain of gates applied sequentially.

    Args:
        initial: Starting quantum state.
        gates: List of dicts with 'type' and 'theta' keys.
        num_frames_per_gate: Number of interpolation frames per gate.

    Returns:
        dict with keys:
            frames: list of (x, y, z) tuples for the full chain
            boundaries: list of frame start indices for each gate
            labels: list of gate label strings
            gate_details: list of gate dicts with axis/angle for Three.js
            final_state: BlochState after all gates applied
            intermediate_states: list of BlochState at each gate boundary
    """
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


def _build_partial_rotation(axis: tuple[float, float, float], theta: float) -> Qobj:
    """Build R_n(theta) = exp(-i theta/2 (n·σ))."""
    nx, ny, nz = axis
    I = identity(2)
    mat = np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * (nx * sigmax() + ny * sigmay() + nz * sigmaz())
    return Qobj(mat)

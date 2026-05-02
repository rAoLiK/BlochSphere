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
    sign = gate.get("sign", 1)

    frames = []
    for i in range(num_frames + 1):
        t = i / num_frames
        theta = total_angle * t
        partial_gate = _build_partial_rotation(axis, theta, sign)
        intermediate = initial.apply_gate(partial_gate)
        frames.append(intermediate.bloch_vector())

    final_state = initial.apply_gate(gate["matrix"])

    return {
        "frames": frames,
        "axis": axis,
        "total_angle": total_angle,
        "final_state": final_state,
    }


def _build_partial_rotation(axis: tuple[float, float, float], theta: float,
                            sign: int = 1) -> Qobj:
    """Build R_n(theta) = exp(sign * i * theta/2 * (n.sigma))."""
    nx, ny, nz = axis
    I = identity(2)
    mat = np.cos(theta / 2) * I + sign * 1j * np.sin(theta / 2) * (
        nx * sigmax() + ny * sigmay() + nz * sigmaz())
    return Qobj(mat)

import numpy as np
from qutip import Qobj, sigmax, sigmay, sigmaz, identity


def _rotation_gate(axis: tuple[float, float, float], theta: float, label: str) -> dict:
    """Build a rotation gate R_n(theta) = exp(-i theta/2 (n·σ))."""
    nx, ny, nz = axis
    I = identity(2)
    matrix = np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * (nx * sigmax() + ny * sigmay() + nz * sigmaz())
    return {
        "matrix": Qobj(matrix),
        "axis": axis,
        "angle": theta,
        "label": label,
    }


def gate_x() -> dict:
    return _rotation_gate((1, 0, 0), np.pi, "X")


def gate_y() -> dict:
    return _rotation_gate((0, 1, 0), np.pi, "Y")


def gate_z() -> dict:
    return _rotation_gate((0, 0, 1), np.pi, "Z")


def gate_h() -> dict:
    """Hadamard: rotation by π around (x+z)/√2."""
    n = 1 / np.sqrt(2)
    return _rotation_gate((n, 0, n), np.pi, "H")


def gate_rx(theta: float) -> dict:
    return _rotation_gate((1, 0, 0), theta, f"Rx({theta:.2f})")


def gate_ry(theta: float) -> dict:
    return _rotation_gate((0, 1, 0), theta, f"Ry({theta:.2f})")


def gate_rz(theta: float) -> dict:
    return _rotation_gate((0, 0, 1), theta, f"Rz({theta:.2f})")


def get_gate(name: str, theta: float = 0.0) -> dict:
    """Dispatch to the appropriate gate function."""
    gates = {
        "X": gate_x,
        "Y": gate_y,
        "Z": gate_z,
        "H": gate_h,
        "Rx": lambda: gate_rx(theta),
        "Ry": lambda: gate_ry(theta),
        "Rz": lambda: gate_rz(theta),
    }
    if name not in gates:
        raise ValueError(f"Unknown gate: {name}")
    return gates[name]()

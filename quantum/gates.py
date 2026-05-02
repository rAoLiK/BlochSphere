import numpy as np
from qutip import Qobj, sigmax, sigmay, sigmaz, identity


def _rotation_gate(axis: tuple[float, float, float], theta: float,
                   label: str, matrix_tex: str, sign: int = 1) -> dict:
    """Build R_n(theta) = exp(sign * i * theta/2 * (n.sigma)).

    sign=+1: clockwise rotation when viewed from +axis toward origin
    sign=-1: counter-clockwise rotation when viewed from +axis toward origin
    """
    nx, ny, nz = axis
    I = identity(2)
    matrix = np.cos(theta / 2) * I + sign * 1j * np.sin(theta / 2) * (
        nx * sigmax() + ny * sigmay() + nz * sigmaz())
    return {
        "matrix": Qobj(matrix),
        "axis": axis,
        "angle": theta,
        "label": label,
        "matrix_tex": matrix_tex,
        "sign": sign,
    }


# X, Z: clockwise (+1) from +axis toward origin
# Y:    counter-clockwise (-1) from +axis toward origin (per table)

def gate_x() -> dict:
    return _rotation_gate(
        (1, 0, 0), np.pi, "X",
        r"X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}",
        sign=+1)


def gate_y() -> dict:
    return _rotation_gate(
        (0, 1, 0), np.pi, "Y",
        r"Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}",
        sign=-1)


def gate_z() -> dict:
    return _rotation_gate(
        (0, 0, 1), np.pi, "Z",
        r"Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}",
        sign=+1)


def gate_h() -> dict:
    n = 1 / np.sqrt(2)
    return _rotation_gate(
        (n, 0, n), np.pi, "H",
        r"H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}",
        sign=-1)


def gate_rx(theta: float) -> dict:
    t = theta
    return _rotation_gate(
        (1, 0, 0), t, f"Rx({t:.2f})",
        rf"R_x({t:.2f}) = \begin{{pmatrix}} "
        rf"\cos({t/2:.2f}) & i\sin({t/2:.2f}) \\ "
        rf"i\sin({t/2:.2f}) & \cos({t/2:.2f}) \end{{pmatrix}}",
        sign=+1)


def gate_ry(theta: float) -> dict:
    t = theta
    return _rotation_gate(
        (0, 1, 0), t, f"Ry({t:.2f})",
        rf"R_y({t:.2f}) = \begin{{pmatrix}} "
        rf"\cos({t/2:.2f}) & -\sin({t/2:.2f}) \\ "
        rf"\sin({t/2:.2f}) & \cos({t/2:.2f}) \end{{pmatrix}}",
        sign=-1)


def gate_rz(theta: float) -> dict:
    t = theta
    return _rotation_gate(
        (0, 0, 1), t, f"Rz({t:.2f})",
        rf"R_z({t:.2f}) = \begin{{pmatrix}} "
        rf"e^{{i{t/2:.2f}}} & 0 \\ 0 & e^{{-i{t/2:.2f}}} \end{{pmatrix}}",
        sign=+1)


def get_gate(name: str, theta: float = 0.0) -> dict:
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

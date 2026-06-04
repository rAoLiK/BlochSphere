import numpy as np
from qutip import Qobj, sigmax, sigmay, sigmaz, identity


def _rotation_gate(axis: tuple[float, float, float], theta: float,
                   label: str, matrix_tex: str) -> dict:
    """Build a gate dict via R_n(θ) = cos(θ/2)·I − i·sin(θ/2)·(n·σ).

    Used for parametric rotation gates (Rx, Ry, Rz).  Fixed gates
    (X, Y, Z, H) use :func:`_textbook_gate` instead to avoid an
    extraneous global phase factor of −i.
    """
    nx, ny, nz = axis
    I = identity(2)
    matrix = np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * (
        nx * sigmax() + ny * sigmay() + nz * sigmaz())
    return {
        "matrix": Qobj(matrix),
        "axis": axis,
        "angle": theta,
        "label": label,
        "matrix_tex": matrix_tex,
    }


def _textbook_gate(matrix, axis: tuple[float, float, float], angle: float,
                   label: str, matrix_tex: str) -> dict:
    """Build a gate dict from a literal (textbook) unitary matrix."""
    return {
        "matrix": Qobj(matrix),
        "axis": axis,
        "angle": angle,
        "label": label,
        "matrix_tex": matrix_tex,
    }


def gate_x() -> dict:
    return _textbook_gate(
        [[0, 1], [1, 0]],
        (1, 0, 0), np.pi, "X",
        r"X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}"
    )


def gate_y() -> dict:
    return _textbook_gate(
        [[0, -1j], [1j, 0]],
        (0, 1, 0), np.pi, "Y",
        r"Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}"
    )


def gate_z() -> dict:
    return _textbook_gate(
        [[1, 0], [0, -1]],
        (0, 0, 1), np.pi, "Z",
        r"Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}"
    )


def gate_h() -> dict:
    n = 1 / np.sqrt(2)
    return _textbook_gate(
        n * np.array([[1, 1], [1, -1]]),
        (n, 0, n), np.pi, "H",
        r"H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}"
    )


def gate_rx(theta: float) -> dict:
    t = theta
    return _rotation_gate(
        (1, 0, 0), t, f"Rx({t:.2f})",
        r"R_x(\theta) = \begin{pmatrix} "
        r"\cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} \\ "
        r"-i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{pmatrix}"
    )


def gate_ry(theta: float) -> dict:
    t = theta
    return _rotation_gate(
        (0, 1, 0), t, f"Ry({t:.2f})",
        r"R_y(\theta) = \begin{pmatrix} "
        r"\cos\frac{\theta}{2} & -\sin\frac{\theta}{2} \\ "
        r"\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{pmatrix}"
    )


def gate_rz(theta: float) -> dict:
    t = theta
    return _rotation_gate(
        (0, 0, 1), t, f"Rz({t:.2f})",
        r"R_z(\theta) = \begin{pmatrix} "
        r"e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}"
    )


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

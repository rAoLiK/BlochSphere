import numpy as np
from qutip import Qobj, basis, sigmax, sigmay, sigmaz


class BlochState:
    """Single-qubit pure state on the Bloch sphere."""

    def __init__(self, ket: Qobj | None = None, label: str = "|0⟩"):
        if ket is not None:
            self.ket = ket
        elif label == "|0⟩":
            self.ket = basis(2, 0)
        elif label == "|1⟩":
            self.ket = basis(2, 1)
        elif label == "|+⟩":
            self.ket = (basis(2, 0) + basis(2, 1)).unit()
        else:
            raise ValueError(f"Unknown initial state label: {label}")

    def bloch_vector(self) -> tuple[float, float, float]:
        """Return (x, y, z) Bloch coordinates via Pauli expectation values."""
        ket = self.ket
        x = float((ket.dag() * sigmax() * ket).real)
        y = float((ket.dag() * sigmay() * ket).real)
        z = float((ket.dag() * sigmaz() * ket).real)
        return (x, y, z)

    def probabilities(self) -> tuple[float, float]:
        """Return (p0, p1) — measurement probabilities."""
        alpha = self.ket[0, 0]
        beta = self.ket[1, 0]
        return (float(abs(alpha) ** 2), float(abs(beta) ** 2))

    def to_ket_text(self) -> str:
        """Formatted Dirac notation string."""
        alpha = complex(self.ket[0, 0])
        beta = complex(self.ket[1, 0])
        a_mag, a_phase = abs(alpha), np.angle(alpha)
        b_mag, b_phase = abs(beta), np.angle(beta)

        parts = []
        threshold = 1e-10

        if a_mag > threshold:
            a_str = f"{a_mag:.3f}"
            if abs(a_phase) > threshold:
                a_str += f"e^{{i{a_phase:.2f}}}"
            parts.append(f"{a_str}|0⟩")

        if b_mag > threshold:
            b_str = f"{b_mag:.3f}"
            rel_phase = b_phase - a_phase
            if abs(rel_phase) > threshold:
                b_str += f"e^{{i{rel_phase:.2f}}}"
            parts.append(f"{b_str}|1⟩")

        if not parts:
            return "0"
        return " + ".join(parts).replace("+ -", "- ")

    def apply_gate(self, gate_matrix: Qobj) -> "BlochState":
        """Apply a unitary gate and return a new BlochState."""
        new_ket = gate_matrix * self.ket
        return BlochState(ket=new_ket)

    @staticmethod
    def from_bloch_vector(x: float, y: float, z: float) -> "BlochState":
        """Construct state from Bloch vector coordinates."""
        r = np.sqrt(x**2 + y**2 + z**2)
        if r > 1.0:
            r = 1.0
        theta = np.arccos(np.clip(z / r, -1, 1)) if r > 1e-10 else 0
        phi = np.arctan2(y, x) if r > 1e-10 else 0
        alpha = np.cos(theta / 2)
        beta = np.exp(1j * phi) * np.sin(theta / 2)
        ket = Qobj([[alpha], [beta]])
        return BlochState(ket=ket)

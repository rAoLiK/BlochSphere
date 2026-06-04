import numpy as np
from qutip import Qobj, basis, sigmax, sigmay, sigmaz


class BlochState:
    """Single-qubit pure state on the Bloch sphere."""

    def __init__(self, ket: Qobj | None = None, label: str = "|0⟩",
                 theta: float | None = None, phi: float | None = None):
        """
        Construct a single-qubit pure state.

        Parameters
        ----------
        ket : Qobj, optional
            Explicit ket vector. Takes priority over all other parameters.
        label : str
            Predefined state label (``"|0⟩"``, ``"|1⟩"``, ``"|+⟩"``).
            Ignored when *ket* or *theta*/*phi* are given.
        theta : float, optional
            Bloch-sphere colatitude in radians, measured from +Z (north pole).
        phi : float, optional
            Bloch-sphere azimuthal angle in radians, measured from +X in the
            X-Y plane.  Must be supplied together with *theta*.
        """
        if (theta is None) != (phi is None):
            raise ValueError("theta and phi must both be provided, or neither")
        if ket is not None:
            self.ket = ket
        elif theta is not None and phi is not None:
            self.ket = self._polar_to_ket(theta, phi)
        elif label == "|0⟩":
            self.ket = basis(2, 0)
        elif label == "|1⟩":
            self.ket = basis(2, 1)
        elif label == "|+⟩":
            self.ket = (basis(2, 0) + basis(2, 1)).unit()
        elif label == "|−⟩":
            self.ket = (basis(2, 0) - basis(2, 1)).unit()
        elif label == "|+i⟩":
            self.ket = (basis(2, 0) + 1j * basis(2, 1)).unit()
        elif label == "|−i⟩":
            self.ket = (basis(2, 0) - 1j * basis(2, 1)).unit()
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
        """Formatted Dirac notation — displays the raw amplitudes as-is."""
        alpha = complex(self.ket[0, 0])
        beta = complex(self.ket[1, 0])

        parts = []
        threshold = 1e-10

        if abs(alpha) > threshold:
            parts.append(self._format_amp(alpha, "|0⟩"))

        if abs(beta) > threshold:
            parts.append(self._format_amp(beta, "|1⟩"))

        if not parts:
            return "0"
        return " + ".join(parts).replace("+ -", "- ")

    @staticmethod
    def _format_amp(z: complex, ket: str) -> str:
        """Format a complex amplitude with its ket label."""
        mag = abs(z)
        phase = np.angle(z)
        if abs(phase) < 1e-10:
            return f"{mag:.3f}{ket}"
        if abs(phase - np.pi) < 1e-10 or abs(phase + np.pi) < 1e-10:
            return f"-{mag:.3f}{ket}"
        if abs(phase - np.pi / 2) < 1e-10:
            return f"i{mag:.3f}{ket}"
        if abs(phase + np.pi / 2) < 1e-10:
            return f"-i{mag:.3f}{ket}"
        return f"{mag:.3f}e^{{i{phase:.2f}}}{ket}"

    def apply_gate(self, gate_matrix: Qobj) -> "BlochState":
        """Apply a unitary gate and return a new BlochState."""
        new_ket = gate_matrix * self.ket
        return BlochState(ket=new_ket)

    @staticmethod
    def _polar_to_ket(theta: float, phi: float) -> Qobj:
        """Convert Bloch-sphere polar angles to a qubit ket vector.

        Parameters
        ----------
        theta : float
            Colatitude from +Z in radians.
        phi : float
            Azimuthal angle from +X in the X-Y plane, in radians.

        Returns
        -------
        Qobj
            A 2-element column ket.
        """
        alpha = np.cos(theta / 2)
        beta = np.exp(1j * phi) * np.sin(theta / 2)
        return Qobj([[alpha], [beta]])

    @staticmethod
    def from_bloch_vector(x: float, y: float, z: float) -> "BlochState":
        """Construct state from Bloch vector coordinates."""
        r = np.sqrt(x**2 + y**2 + z**2)
        if r > 1.0:
            r = 1.0
        theta = np.arccos(np.clip(z / r, -1, 1)) if r > 1e-10 else 0
        phi = np.arctan2(y, x) if r > 1e-10 else 0
        ket = BlochState._polar_to_ket(theta, phi)
        return BlochState(ket=ket)

import pytest
import numpy as np
from quantum.state import BlochState
from quantum.gates import get_gate


def test_partial_theta_raises():
    """Providing theta without phi must raise ValueError."""
    with pytest.raises(ValueError, match="theta and phi must both be provided"):
        BlochState(theta=0.5)


def test_partial_phi_raises():
    """Providing phi without theta must raise ValueError."""
    with pytest.raises(ValueError, match="theta and phi must both be provided"):
        BlochState(phi=1.0)


def test_custom_state_north_pole():
    """theta=0 should give |0> (north pole)."""
    s = BlochState(theta=0.0, phi=0.0)
    x, y, z = s.bloch_vector()
    assert abs(x) < 1e-10
    assert abs(y) < 1e-10
    assert abs(z - 1.0) < 1e-10


def test_custom_state_south_pole():
    """theta=pi should give |1> (south pole)."""
    s = BlochState(theta=np.pi, phi=0.0)
    x, y, z = s.bloch_vector()
    assert abs(x) < 1e-10
    assert abs(y) < 1e-10
    assert abs(z + 1.0) < 1e-10


def test_custom_state_equator():
    """theta=pi/2, phi=0 should give |+> (equator at +X)."""
    s = BlochState(theta=np.pi / 2, phi=0.0)
    x, y, z = s.bloch_vector()
    assert abs(x - 1.0) < 1e-10
    assert abs(y) < 1e-10
    assert abs(z) < 1e-10


def test_custom_state_equator_phi():
    """theta=pi/2, phi=pi/2 should give +Y on equator."""
    s = BlochState(theta=np.pi / 2, phi=np.pi / 2)
    x, y, z = s.bloch_vector()
    assert abs(x) < 1e-10
    assert abs(y - 1.0) < 1e-10
    assert abs(z) < 1e-10


def test_custom_state_unit_norm():
    """Any pure state should have Bloch vector norm ~1."""
    for theta in [0.3, 1.0, 2.5]:
        for phi in [0.0, 1.5, 3.14]:
            s = BlochState(theta=theta, phi=phi)
            x, y, z = s.bloch_vector()
            norm = np.sqrt(x**2 + y**2 + z**2)
            assert abs(norm - 1.0) < 1e-10


def test_custom_state_probabilities():
    """theta=pi/2 should give 50/50 probabilities."""
    s = BlochState(theta=np.pi / 2, phi=0.0)
    p0, p1 = s.probabilities()
    assert abs(p0 - 0.5) < 1e-10
    assert abs(p1 - 0.5) < 1e-10


# ── Gate phase tests ─────────────────────────────────────────────


def test_z_gate_on_zero():
    """Z|0⟩ = |0⟩."""
    s = BlochState(label="|0⟩")
    result = s.apply_gate(get_gate("Z")["matrix"])
    assert result.to_ket_text() == "1.000|0⟩"


def test_z_gate_on_one():
    """Z|1⟩ = -|1⟩ — phase must be visible."""
    s = BlochState(label="|1⟩")
    result = s.apply_gate(get_gate("Z")["matrix"])
    assert result.to_ket_text() == "-1.000|1⟩"


def test_x_gate_on_zero():
    """X|0⟩ = |1⟩."""
    s = BlochState(label="|0⟩")
    result = s.apply_gate(get_gate("X")["matrix"])
    assert result.to_ket_text() == "1.000|1⟩"


def test_x_gate_on_one():
    """X|1⟩ = |0⟩."""
    s = BlochState(label="|1⟩")
    result = s.apply_gate(get_gate("X")["matrix"])
    assert result.to_ket_text() == "1.000|0⟩"


def test_h_gate_on_zero():
    """H|0⟩ = (|0⟩ + |1⟩)/√2."""
    s = BlochState(label="|0⟩")
    result = s.apply_gate(get_gate("H")["matrix"])
    assert result.to_ket_text() == "0.707|0⟩ + 0.707|1⟩"


def test_h_gate_on_one():
    """H|1⟩ = (|0⟩ - |1⟩)/√2."""
    s = BlochState(label="|1⟩")
    result = s.apply_gate(get_gate("H")["matrix"])
    assert result.to_ket_text() == "0.707|0⟩ - 0.707|1⟩"


def test_z_gate_on_plus():
    """Z|+⟩ = |−⟩ = (|0⟩ - |1⟩)/√2."""
    s = BlochState(label="|+⟩")
    result = s.apply_gate(get_gate("Z")["matrix"])
    assert result.to_ket_text() == "0.707|0⟩ - 0.707|1⟩"


# ── to_ket_text phase display tests ──────────────────────────────


def test_ket_text_imaginary_beta():
    """State (|0⟩ + i|1⟩)/√2 should show i prefix."""
    ket = (1 / np.sqrt(2)) * BlochState(label="|0⟩").ket + \
          (1j / np.sqrt(2)) * BlochState(label="|1⟩").ket
    s = BlochState(ket=ket)
    assert s.to_ket_text() == "0.707|0⟩ + i0.707|1⟩"


def test_ket_text_negative_imaginary_beta():
    """State (|0⟩ - i|1⟩)/√2 should show -i prefix."""
    ket = (1 / np.sqrt(2)) * BlochState(label="|0⟩").ket + \
          (-1j / np.sqrt(2)) * BlochState(label="|1⟩").ket
    s = BlochState(ket=ket)
    assert s.to_ket_text() == "0.707|0⟩ - i0.707|1⟩"


# ── Parametric gate consistency ──────────────────────────────────


def test_rx_pi_matches_x_bloch():
    """Rx(π)|0⟩ and X|0⟩ should land on the same Bloch point."""
    s0 = BlochState(label="|0⟩")
    rx_result = s0.apply_gate(get_gate("Rx", np.pi)["matrix"])
    x_result = s0.apply_gate(get_gate("X")["matrix"])
    assert np.allclose(rx_result.bloch_vector(), x_result.bloch_vector(), atol=1e-10)


# ── Eigenvalue phase tests ───────────────────────────────────────


def test_x_eigenvalue_plus():
    """X|+⟩ = +|+⟩ (eigenvalue +1)."""
    s = BlochState(label="|+⟩")
    r = s.apply_gate(get_gate("X")["matrix"])
    assert r.to_ket_text() == "0.707|0⟩ + 0.707|1⟩"


def test_x_eigenvalue_minus():
    """X|−⟩ = −|−⟩ = |+⟩ (eigenvalue -1; −|−⟩ and |+⟩ differ by global phase)."""
    s = BlochState(label="|−⟩")
    r = s.apply_gate(get_gate("X")["matrix"])
    # -|-⟩ normalized by β (angle 0) gives -0.707|0⟩ + 0.707|1⟩
    assert r.to_ket_text() == "-0.707|0⟩ + 0.707|1⟩"


def test_y_eigenvalue_plus():
    """Y|+i⟩ = +|+i⟩ (eigenvalue +1)."""
    s = BlochState(label="|+i⟩")
    r = s.apply_gate(get_gate("Y")["matrix"])
    assert r.to_ket_text() == "0.707|0⟩ + i0.707|1⟩"


def test_y_eigenvalue_minus():
    """Y|−i⟩ = −|−i⟩ (eigenvalue -1, sign visible)."""
    s = BlochState(label="|−i⟩")
    r = s.apply_gate(get_gate("Y")["matrix"])
    assert r.to_ket_text() == "-0.707|0⟩ + i0.707|1⟩"

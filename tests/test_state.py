import numpy as np
from quantum.state import BlochState


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

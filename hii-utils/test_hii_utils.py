"""Unit tests hor hii_utils module"""

import pytest
import hii_utils
import numpy as np
import astropy.units as u

def test_alpha_B():
    """Test that we get the right value of the recombination coefficient at T = 15,000 K."""
    assert np.isclose(
        hii_utils.alpha_B(1.5e4 * u.K),
        2.54e-13 * (1.5 ** -0.82) * u.cm**3 / u.s
    )

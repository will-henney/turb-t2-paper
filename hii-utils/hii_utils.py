"""
Utility functions for global modeling of H II regions.

William Henney (2024)

"""

import numpy as np
import astropy.units as u
from astropy.constants import c, m_e, m_p, k_B, e, eps0

def hello() -> str:
    return "Hello from hii-utils!"

def alpha_B(T):
    """
    Approximate Case B recombination coefficient for hydrogen.

    This is the best power law for T ~ 10^4 K, but will be inaccurate for T < 3000 K or T > 30,000 K.
    See, for instance Draine (2011) Chapter 14
    """
    T4 = T.to(u.K).value / 1e4
    return 2.54e-13 * T4**(-0.82) * u.cm**3 / u.s

def ionization_equilibrium():
    pass

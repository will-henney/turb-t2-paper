import marimo

__generated_with = "0.9.27"
app = marimo.App()


@app.cell
def __():
    import plasmapy
    return (plasmapy,)


@app.cell
def __(mo):
    mo.md(r"""There does not seem to bee any slowness in importing plasmapy any more""")
    return


@app.cell
def __():
    import hii_utils
    import plasmapy.formulary as pf
    import astropy.units as u
    import astropy.constants as const
    import numpy as np
    return const, hii_utils, np, pf, u


@app.cell
def __(mo):
    mo.md(r"""## Calculate various parameters for a typical H II region""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Fiducial parameters

        As with my other notes, we will normalise to an electron density of 100 pcc and temperature of 10,000 K. We set the size scale to 10 pc (later, we can try and relate this to the ionization parameter)
        """
    )
    return


@app.cell
def __(u):
    L = 10.0 * u.pc
    n = 100.0 * u.cm ** -3
    T = 1.0e4 * u.K
    species = ("p+", "p+")
    return L, T, n, species


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Magnetic field

        Set the magnetic field to try and give a plasma beta of unity. Note that the `n` parameter in the `beta()` function is the total particle density, which is $2 n_e$ if fully ionized pure hydrogen.
        """
    )
    return


@app.cell
def __(T, n, pf, u):
    B = 83.3* u.microgauss
    pf.beta(T, 2*n, B)
    return (B,)


@app.cell
def __(mo):
    mo.md(r"""That is close enough to unity. But note that it is slightly different from the 78.2 microG that I derived in my notes, which is probably due to the correction for Helium, which I am ignoring here.""")
    return


@app.cell
def __(mo):
    mo.md(r"""### Collisional quantities""")
    return


@app.cell
def __(L, T, mo, n, pf, species):
    mo.md("The Knudsen number Kn is:")
    pf.Knudsen_number(L, T, n, species)
    return


@app.cell
def __(mo):
    mo.md(r"""#### Mean free path, thermal speed, and collisional frequencies""")
    return


@app.cell
def __(mo):
    mo.md(r"""Mean free path comes out the same for electrons and protons""")
    return


@app.cell
def __(T, n, pf, species):
    ion_mfp = pf.mean_free_path(T, n, species)
    ion_mfp.cgs
    return (ion_mfp,)


@app.cell
def __(mo):
    mo.md(r"""But it is slightly different for Helium ions""")
    return


@app.cell
def __(T, n, pf):
    pf.mean_free_path(T, n, ("He++", "p+")).cgs
    return


@app.cell
def __(mo):
    mo.md(r"""And it is a *lot* bigger for high-velocity protons (for example, from stellar wind)""")
    return


@app.cell
def __(T, n, pf, species, u):
    pf.mean_free_path(T, n, species, V=1000 * u.km/u.s).cgs
    return


@app.cell
def __(mo):
    mo.md(r"""Calculate the thermal speed. This is the 3d rms speed, but I am not sure if this is exactly what we should be using.""")
    return


@app.cell
def __(T, pf, u):
    v_rms = pf.thermal_speed(T, "p", method="rms", ndim=3)
    v_rms.to(u.km/u.s)
    return (v_rms,)


@app.cell
def __(mo):
    mo.md(r"""OK, I have investigated more and it turns out it uses the most probable speed from 3d Maxwellian by default, which is slightly lower""")
    return


@app.cell
def __(T, pf, u):
    v_therm_ion = pf.thermal_speed(T, "p", ndim=3)
    v_therm_ion.to(u.km/u.s)
    return (v_therm_ion,)


@app.cell
def __(mo):
    mo.md(r"""Now get the collisional time. Supposedly, we should use the MaxwellianCollisionFrequencies class, but that is a bit of a pain since it requires sending the Coulomb logarithm. But first we will try the old deprecated version:""")
    return


@app.cell
def __(T, n, pf):
    nu_i_old = pf.fundamental_ion_collision_freq(T, n, "p")
    nu_i_old
    return (nu_i_old,)


@app.cell
def __(mo):
    mo.md(r"""And now we calculate the Coulomb logarithm and use the new way of doing it""")
    return


@app.cell
def __(T, n, pf, species):
    pf.Coulomb_logarithm(T, n, species)
    return


@app.cell
def __(T, n, pf, species, u):
    freqs = pf.MaxwellianCollisionFrequencies(
        "p", "p", T_a=T, n_a=n, T_b=T, n_b=n,
        Coulomb_log=pf.Coulomb_logarithm(T, n, species) * u.dimensionless_unscaled,
    )
    return (freqs,)


@app.cell
def __(freqs):
    nu_i = freqs.Maxwellian_avg_ii_collision_freq
    nu_i
    return (nu_i,)


@app.cell
def __(mo):
    mo.md(r"""There is also a simpler tyoe of collision frequency that comes out differently""")
    return


@app.cell
def __(freqs):
    nu_Lorentz = freqs.Lorentz_collision_frequency
    nu_Lorentz
    return (nu_Lorentz,)


@app.cell
def __(T, n, pf, species):
    nu_Lorentz_old = pf.collision_frequency(T, n, species)
    nu_Lorentz_old
    return (nu_Lorentz_old,)


@app.cell
def __(mo):
    mo.md(r"""Or converted into a time:""")
    return


@app.cell
def __(nu_Lorentz_old):
    tau_i = 1/nu_Lorentz_old
    tau_i.cgs
    return (tau_i,)


@app.cell
def __(ion_mfp, nu_Lorentz_old, u):
    (ion_mfp * nu_Lorentz_old).to(u.km/u.s)
    return


@app.cell
def __(mo):
    mo.md(r"""OK, so that varies a lot, depending on whether we use the Lorentz or Maxwellian and whether we use the class (new) or the function (old). Looking at the source code for mean_free_path, it uses the Lorentz function version, so we will do the same for consistency.""")
    return


@app.cell
def __(np, u, v_therm_ion):
    np.sqrt(2) * v_therm_ion.to(u.km/u.s)
    return


@app.cell
def __(mo):
    mo.md(r"""So that is consistent, yay!  The reason for the sqrt(2) factor is that it is the relative speed between two protons.""")
    return


@app.cell
def __(mo):
    mo.md(r"""#### Viscosity""")
    return


@app.cell
def __(mo):
    mo.md(r"""By default, the transport coefficients are calculated in the Braginskii model""")
    return


@app.cell
def __(T, n, pf):
    pf.ion_viscosity(T, n, T, n, "p")
    return


@app.cell
def __(mo):
    mo.md(r"""But there is the option to use the more accurate Ji and Held (2013) model, although in our case this makes little difference.""")
    return


@app.cell
def __(mo):
    mo.md(r"""But we can also a more recent theory from Ji & Held (2013), which changes the numbers very slightly. The main difference is that it better accounts for the electron-ion collisions, and apparently it has more effect in the magnetic case, which we will  see below.""")
    return


@app.cell
def __(T, n, pf):
    pf.ion_viscosity(T, n, T, n, "p", model="Ji-Held")
    return


@app.cell
def __(mo):
    mo.md(r"""Note that viscosity is a tensor, which may become important once we introduce a magnetic field.""")
    return


@app.cell
def __(mo):
    mo.md(r"""#### Anisotropy with magnetic field""")
    return


@app.cell
def __(B, T, n, pf):
    hall = pf.Hall_parameter(n, T, B, "p", "p")
    hall
    return (hall,)


@app.cell
def __(mo):
    mo.md(r"""The Hall parameter is the product of Larmor frequency and collision time: $x = \omega_L \, \tau = (V / r_L)\, (\lambda / V) = \lambda / r_L$. so it is the ratio of the mean free path to the Larmor radius. This is very similar to the magnetic Prandtl number, which I calculated in the notes. It is linearly proportional to the B field:""")
    return


@app.cell
def __(B, T, n, pf):
    pf.Hall_parameter(n, T, 0.1 * B, "p", "p")
    return


@app.cell
def __(B, T, n, pf):
    pf.ion_viscosity(T, n, T, n, "p", B=B, model="Ji-Held")
    return


@app.cell
def __(B, T, n, pf):
    viscosity = pf.ion_viscosity(T, n, T, n, "p", B=B)
    viscosity
    return (viscosity,)


@app.cell
def __(mo):
    mo.md(r"""These are now the tensor viscosity results with a more realistic magnetic field""")
    return


@app.cell
def __(viscosity):
    viscosity[0] / viscosity[3]
    return


@app.cell
def __(mo):
    mo.md(r"""Why is there such a large difference between these components? I need to better understand the relation with the parallel, perpendicular, and cross components.""")
    return


@app.cell
def __(B, T, n, pf):
    pf.electron_viscosity(T, n, T, n, "p", B=B)
    return


@app.cell
def __(mo):
    mo.md(r"""So the electron viscosity (for the *ions*) is 100  times lower than the ion viscosity, so we can ignore it.""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        #### Kinematic viscosity

        The kinematic viscosity is equal to the dynamic viscosity divided by the mass density.
        """
    )
    return


@app.cell
def __(const, n, viscosity):
    kinematic_viscosity = viscosity / (n * const.m_p)
    kinematic_viscosity.cgs
    return (kinematic_viscosity,)


@app.cell
def __(mo):
    mo.md(r"""This should be equal to the mean-free path times the ion thermal speed.""")
    return


@app.cell
def __(mo):
    mo.md(r"""Let's make the comparison:""")
    return


@app.cell
def __(ion_mfp, v_therm_ion):
    (ion_mfp * v_therm_ion).cgs
    return


@app.cell
def __(mo):
    mo.md(r"""Hurray, that is very close to what I was expecting for the parallel viscosity. Some texts have a factor of 1/3 in this equation, but if I used that, then we would have a bigger discrepancy.""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Reynolds number

        This is what we finally want to calculate.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"""Consider pure hydrogen and fully ionized to calculate the isothermal sound speed.""")
    return


@app.cell
def __(T, const, np, u):
    sound_speed = np.sqrt(2 * const.k_B * T / const.m_p)
    sound_speed.to(u.km / u.s)
    return (sound_speed,)


@app.cell
def __(mo):
    mo.md(
        r"""
        This is actually numerically equal to the ion thermal speed. 

        I use the parallel component of the dynamic viscosity.
        """
    )
    return


@app.cell
def __(L, const, n, pf, v_therm_ion, viscosity):
    Re = pf.Reynolds_number(
        rho = const.m_p * n,
        U = v_therm_ion,
        L = L,
        mu = viscosity[0],
    )
    Re
    return (Re,)


@app.cell
def __(mo):
    mo.md(r"""The integral scale Re for H II regions will be a bit smaller since the injection scale will be smaller than the Stromgren radius. But it will still be of order 1e9.""")
    return


@app.cell
def __():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

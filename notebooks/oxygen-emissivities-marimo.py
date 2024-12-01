import marimo

__generated_with = "0.9.27"
app = marimo.App(width="medium")


@app.cell
def __():
    # '%matplotlib inline\n' command supported automatically in marimo
    import numpy as np
    import pyneb as pn
    from matplotlib import pyplot as plt
    import seaborn as sns
    import polars as pl
    return np, pl, plt, pn, sns


@app.cell
def __(mo):
    mo.md(r"""## Set up oxygen ion spectra with PyNeb""")
    return


@app.cell
def __(mo):
    mo.md(r"""Recombination of O++ gives the O II spectrum.""")
    return


@app.cell
def __(pn):
    oiir = pn.RecAtom("O", 2)
    return (oiir,)


@app.cell
def __(mo):
    mo.md(r"""Collisional excitation of O++ gives the [O III] spectrum""")
    return


@app.cell
def __(pn):
    oiiic = pn.Atom("O", 3)
    return (oiiic,)


@app.cell
def __(oiiic):
    oiiic.getTransition(5007)
    return


@app.cell
def __(pn):
    pn.atomicData.getDataFile('O2', 'rec')
    return


@app.cell
def __(mo):
    mo.md(r"""O II recombination line data is from Storey+ [2017MNRAS.470..379S](https://ui.adsabs.harvard.edu/abs/2017MNRAS.470..379S/abstract)""")
    return


@app.cell
def __(pn):
    pn.atomicData.getAllAtoms(coll=False, rec=True)
    return


@app.cell
def __(oiir):
    [_ for _ in oiir.labels if _.startswith("43")]
    return


@app.cell
def __(oiir):
    oiir.getTransition('4649.13')
    return


@app.cell
def __(np, oiir):
    oiir.getEmissivity(tem=np.linspace(5000, 10000, 6), den=1e4, label='4650.84')
    return


@app.cell
def __(mo):
    mo.md(r"""## Plot emissivities versus T for recombination and collisional lines""")
    return


@app.cell
def __(np):
    temperatures = np.geomspace(3000.0, 100_000.0, 200)
    return (temperatures,)


@app.cell
def __(np, oiir):
    V1_mult = ('4638.86', '4641.81', '4649.13', '4650.84', '4661.63', '4673.73', '4676.23', '4696.35')

    def oii_multiplet_sum_emissivity(tem, den, multiplet=V1_mult):
        result = None
        for label in multiplet:
            em = oiir.getEmissivity(tem=tem, den=den, label=label)
            if result is None:
                result = em
            else:
                result = result + em
        return result

    def normalize(tem, em, T0=10000.0):
        em0 = np.interp(T0, tem, em)
        return em / em0
    return V1_mult, normalize, oii_multiplet_sum_emissivity


@app.cell
def __():
    V15_mult = "4590.97", #"4596.18", "4595.96"
    V3d_4f = "4303.82", "4609.44", "4087.15", "4089.29"
    return V15_mult, V3d_4f


@app.cell
def __(V15_mult, oii_multiplet_sum_emissivity):
    oii_multiplet_sum_emissivity([1000, 3000, 5000, 8000, 1e4], 1e4, multiplet=V15_mult)
    return


@app.cell
def __(sns):
    sns.set_context("talk")
    sns.set_color_codes("deep")
    return


@app.cell
def __(
    V15_mult,
    V3d_4f,
    normalize,
    oii_multiplet_sum_emissivity,
    oiiic,
    plt,
    sns,
    temperatures,
):
    fig, ax = plt.subplots(figsize=(7, 7))
    density = 1e2
    T0 = 10_000.0

    em = oii_multiplet_sum_emissivity(temperatures, density)
    em = normalize(temperatures, em)
    ax.plot(temperatures, em, label="O II V1", ls="-", lw=4)

    em = oii_multiplet_sum_emissivity(temperatures, density, multiplet=V15_mult)
    em = normalize(temperatures, em)
    ax.plot(temperatures, em, label="O II V15", ls="--", lw=4)

    em = oii_multiplet_sum_emissivity(temperatures, density, multiplet=V3d_4f)
    em = normalize(temperatures, em)
    ax.plot(temperatures, em, label="O II 3d-4f", ls=":", lw=4)

    em = oiiic.getEmissivity(tem=temperatures, den=density, wave=5007)
    em = normalize(temperatures, em)
    ax.plot(temperatures, em, label="[O III] 5007", ls="-", lw=2.5)

    em = oiiic.getEmissivity(tem=temperatures, den=density, wave=4363)
    em = normalize(temperatures, em)
    ax.plot(temperatures, em, label="[O III] 4363", ls="-.", lw=2.5)

    for slope in [-1, 0, 1, 2, 3, 4, 5, 6, 7]:
        ax.plot(temperatures, (temperatures / T0)**slope, label=None, lw=1, alpha=0.2, color="k")

    annotate_kws = dict(fontsize="small", horizontalalignment="center", verticalalignment="center_baseline")
    ax.annotate("$T^{-1}$", (4e4, (4e4/T0)**-1), **annotate_kws)
    ax.annotate("$T^{2}$", (4e4, (4e4/T0)**2), **annotate_kws)
    ax.annotate("$T^{7}$", (2e4, (2e4/T0)**7), **annotate_kws)
    ax.legend(fontsize="small")
    ax.set(
        xscale="log",
        yscale="log",
        ylim=[1e-2, 1e3],
        xlim=[None, None],
        xlabel="Temperature, K",
        ylabel="Relative emissivity",
    )
    sns.despine()
    fig.tight_layout()
    fig.savefig("oplusplus-emissivity-vs-t-loglog.pdf")
    fig
    return T0, annotate_kws, ax, density, em, fig, slope


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Compare with formulae in Peimbert & Peimbert (2013)

        These are equations (1, 2, 3)
        """
    )
    return


@app.cell
def __(np):
    def em_V1_PP13(T, T0=10000.0):
        return (T / T0) ** (-0.755)

    def em_4959_PP13(T, T0=10000.0):
        result = T ** (-0.34) * np.exp(-29160 / T)
        result = result / (T0 ** (-0.34) * np.exp(-29160 / T0))
        return result

    def em_4363_PP13(T, T0=10000.0):
        result = T ** (-0.34) * np.exp(-62120 / T)
        result = result / (T0 ** (-0.34) * np.exp(-62120 / T0))
        return result
    return em_4363_PP13, em_4959_PP13, em_V1_PP13


@app.cell
def __(mo):
    mo.md(r"""Repeat the previous graph but adding the PP13 curves""")
    return


@app.cell
def __(
    V15_mult,
    V3d_4f,
    em_4363_PP13,
    em_4959_PP13,
    em_V1_PP13,
    normalize,
    oii_multiplet_sum_emissivity,
    oiiic,
    plt,
    sns,
    temperatures,
):
    fig_1, ax_1 = plt.subplots(figsize=(7, 7))
    density_1 = 100.0
    T0_1 = 10000.0
    em_1 = oii_multiplet_sum_emissivity(temperatures, density_1)
    em_1 = normalize(temperatures, em_1)
    line, = ax_1.plot(temperatures, em_1, label='O II V1', ls='-', lw=4)
    ax_1.plot(temperatures, em_V1_PP13(temperatures), label=None, color=line.get_color(), ls=line.get_ls(), lw=line.get_lw() / 4, alpha=1)
    em_1 = oii_multiplet_sum_emissivity(temperatures, density_1, multiplet=V15_mult)
    em_1 = normalize(temperatures, em_1)
    ax_1.plot(temperatures, em_1, label='O II V15', ls='--', lw=4)
    em_1 = oii_multiplet_sum_emissivity(temperatures, density_1, multiplet=V3d_4f)
    em_1 = normalize(temperatures, em_1)
    ax_1.plot(temperatures, em_1, label='O II 3d-4f', ls=':', lw=4)
    em_1 = oiiic.getEmissivity(tem=temperatures, den=density_1, wave=5007)
    em_1 = normalize(temperatures, em_1)
    line, = ax_1.plot(temperatures, em_1, label='[O III] 5007', ls='-', lw=2.5)
    ax_1.plot(temperatures, em_4959_PP13(temperatures), label=None, color=line.get_color(), ls=line.get_ls(), lw=line.get_lw() / 4, alpha=1)
    em_1 = oiiic.getEmissivity(tem=temperatures, den=density_1, wave=4363)
    em_1 = normalize(temperatures, em_1)
    line, = ax_1.plot(temperatures, em_1, label='[O III] 4363', ls='-.', lw=2.5)
    ax_1.plot(temperatures, em_4363_PP13(temperatures), label=None, color=line.get_color(), ls=line.get_ls(), lw=line.get_lw() / 4, alpha=1)
    for slope_1 in [-1, 0, 1, 2, 3, 4, 5, 6, 7]:
        ax_1.plot(temperatures, (temperatures / T0_1) ** slope_1, label=None, lw=1, alpha=0.2, color='k')
    annotate_kws_1 = dict(fontsize='small', horizontalalignment='center', verticalalignment='center_baseline')
    ax_1.annotate('$T^{-1}$', (40000.0, (40000.0 / T0_1) ** (-1)), **annotate_kws_1)
    ax_1.annotate('$T^{2}$', (40000.0, (40000.0 / T0_1) ** 2), **annotate_kws_1)
    ax_1.annotate('$T^{7}$', (20000.0, (20000.0 / T0_1) ** 7), **annotate_kws_1)
    ax_1.legend(fontsize='small')
    ax_1.set(xscale='log', yscale='log', ylim=[0.01, 1000.0], xlim=[None, None], xlabel='Temperature, K', ylabel='Relative emissivity')
    sns.despine()
    fig_1.tight_layout()
    fig_1.savefig('oplusplus-emissivity-vs-t-loglog-with-PP13.pdf')
    fig_1
    return T0_1, annotate_kws_1, ax_1, density_1, em_1, fig_1, line, slope_1


@app.cell
def __(mo):
    mo.md(
        r"""
        The agreement in the V1 emissivity is good for $T$ higher than 10,000 K so we can use the power law to extend the range beyond 30,000 K

        The agreement in collisional emissivities is good up to 30,000 K, which is more than the stated range of validity in PP13 (5000 to 15,000 K). 

        So, we can use PyNeb everywhere, except for V1 above 20,000 K, where we can use the power law. 

        Note that this is for density 100 pcc. The V1 emissivities from PyNeb do vary with density, and at higher densities they deviate from the power law at the high T end of the range.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"""## Calculating the logarithmic derivatives of the emissivities""")
    return


@app.cell
def __(em_V1_PP13, oii_multiplet_sum_emissivity, oiiic, temperatures):
    density_2 = 100.0
    em4363 = oiiic.getEmissivity(tem=temperatures, den=density_2, wave=4363)
    em5007 = oiiic.getEmissivity(tem=temperatures, den=density_2, wave=5007)
    emV1 = oii_multiplet_sum_emissivity(temperatures, density_2)
    emV1p = em_V1_PP13(temperatures)
    return density_2, em4363, em5007, emV1, emV1p


@app.cell
def __(em4363, em5007, emV1, emV1p, np, temperatures):
    q4363 = np.gradient(np.log(em4363), np.log(temperatures))
    q5007 = np.gradient(np.log(em5007), np.log(temperatures))
    qV1 = np.gradient(np.log(emV1), np.log(temperatures))
    qV1p = np.gradient(np.log(emV1p), np.log(temperatures))
    return q4363, q5007, qV1, qV1p


@app.cell
def __(mo):
    mo.md(r"""Make a polars dataframe just for fun""")
    return


@app.cell
def __(pl, q4363, q5007, qV1, qV1p, temperatures):
    df = pl.DataFrame(
        {
            "T": temperatures,
            "qA": q4363,
            "qB": q5007,
            # "qC": np.where(np.isfinite(qV1), qV1, None),
            "qC": qV1,
            "qC PP13": qV1p,
        }
    )
    return (df,)


@app.cell
def __(mo):
    mo.md(r"""Look at every 20th row to get an overview""")
    return


@app.cell
def __(df):
    df[::20]
    return


@app.cell
def __(mo):
    mo.md(r"""Correlations between columns""")
    return


@app.cell
def __(df):
    df.corr()
    return


@app.cell
def __(mo):
    mo.md(r"""Note that polars makes a distinction between missing values (None) and float NaNs. However, when I tried that, it did not work with .corr()""")
    return


@app.cell
def __(df, plt):
    fig_2, ax_2 = plt.subplots()
    ax_2.plot('T', 'qA', label='[O III] 4363', data=df)
    ax_2.plot('T', 'qB', label='[O III] 5007', data=df)
    ax_2.plot('T', 'qC', label='O II V1', data=df)
    ax_2.plot('T', 'qC PP13', label='O II V1 PP', data=df)
    ax_2.axhline(color='k', lw=0.5)
    ax_2.legend()
    ax_2.set(xscale='log', xlabel='Temperature, K', ylabel='Emissivity slope index, $q$')
    ax_2
    return ax_2, fig_2


@app.cell
def __(mo):
    mo.md(r"""## Calculating the bias factors, Q""")
    return


@app.cell
def __():
    def bias(qj, qk):
        Q = qj * (qj - 1) - qk * (qk - 1)
        Q = Q / (2 * (qj - qk))
        return Q
    return (bias,)


@app.cell
def __(mo):
    mo.md(r"""This seems to be the recommended way of making a new dataframe based on columns from the old one. First I use select() to take the T column from the original and add 3 bias columns. Then I use with_columns() to add two more columns for the differences. Maybe there is a way of doing it all at once, but I do not know how to allow the reference to new columns I have just created.""")
    return


@app.cell
def __(bias, df, pl):
    bdf = df.select(
        pl.col("T"),
        bias(pl.col("qA"), pl.col("qB")).alias("Q_AB"),
        bias(pl.col("qB"), pl.col("qC")).alias("Q_BC"),
        bias(pl.col("qB"), pl.col("qC PP13")).alias("Q_BC PP13"),
    ).with_columns(
        dQ = (pl.col("Q_AB") - pl.col("Q_BC")),
        dQp = (pl.col("Q_AB") - pl.col("Q_BC PP13")),
    )
    bdf[::20]
    return (bdf,)


@app.cell
def __(bdf, plt):
    fig_3, ax_3 = plt.subplots()
    ax_3.plot('T', 'Q_AB', label='$Q_\\mathrm{AB}$: 4363 / 5007', data=bdf)
    line_1, = ax_3.plot('T', 'Q_BC', label='$Q_\\mathrm{BC}$: 5007 / V1', data=bdf)
    ax_3.plot('T', 'Q_BC PP13', label='', data=bdf, color=line_1.get_color(), lw=line_1.get_lw() / 4)
    line_1, = ax_3.plot('T', 'dQ', label='Difference', data=bdf)
    ax_3.plot('T', 'dQp', label='', data=bdf, color=line_1.get_color(), lw=line_1.get_lw() / 4)
    ax_3.axhline(color='k', lw=0.5)
    ax_3.legend()
    ax_3.set(xscale='log', xlabel='Temperature, K', ylabel='Bias factor, $Q$')
    fig_3
    return ax_3, fig_3, line_1


@app.cell
def __(mo):
    mo.md(r"""## Fit a function to the Qs""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Polynomial fit in log10 T

        This is the simplest option since it can be done in numpy
        """
    )
    return


@app.cell
def __(bdf, np):
    pfitAB = np.polynomial.Polynomial.fit(
        np.log10(bdf["T"]),
        bdf["Q_AB"],
        deg=4,
    )
    pfitAB
    return (pfitAB,)


@app.cell
def __(pfitAB):
    print(repr(pfitAB))
    return


@app.cell
def __(pfitAB):
    pfitAB.convert()
    return


@app.cell
def __(pfitAB):
    pfitAB([3.5, 4.0, 4.5, 5.0])
    return


@app.cell
def __(bdf, np, pfitAB, pl):
    bdf_1 = bdf.with_columns(Q_AB_fit=pfitAB(np.log10(pl.col('T')))).with_columns(Q_AB_residual=10 * (pl.col('Q_AB') - pl.col('Q_AB_fit')))
    return (bdf_1,)


@app.cell
def __(bdf_1, plt):
    fig_4, ax_4 = plt.subplots()
    line_2, = ax_4.plot('T', 'Q_AB', label='$Q_\\mathrm{AB}$: 4363 / 5007', data=bdf_1)
    ax_4.plot('T', 'Q_AB_fit', label='fit', data=bdf_1, color='r', lw=line_2.get_lw() / 4)
    ax_4.plot('T', 'Q_AB_residual', label='10 x residual', data=bdf_1, color='g', lw=line_2.get_lw() / 4)
    ax_4.axhline(color='k', lw=0.5)
    ax_4.legend()
    ax_4.set(xscale='log', xlabel='Temperature, K', ylabel='Bias factor, $Q$')
    fig_4
    return ax_4, fig_4, line_2


@app.cell
def __(mo):
    mo.md(r"""So the 4th order polynomial gives a reasonable fit, except it will be very badly behaved outside the fitted range.""")
    return


@app.cell
def __(mo):
    mo.md(r"""### Fit a constant plus 1/T^n""")
    return


@app.cell
def __(mo):
    mo.md(r"""This may be better behaved. We will use astropy's modeling functionality""")
    return


@app.cell
def __():
    from astropy.modeling import models, fitting
    return fitting, models


@app.cell
def __(mo):
    mo.md(r"""We fix the x_0 normalization to be 1e4 K since there is no need to vary both that and the amplitude. We also try out fixing the power law index to be -1, just for simplicity.""")
    return


@app.cell
def __(bdf_1, fitting, models):
    model = models.PowerLaw1D(x_0=10000.0, alpha=0.95, fixed={'x_0': True, 'alpha': True}) + models.Const1D(amplitude=-1.1, fixed={'amplitude': True})
    fitter = fitting.TRFLSQFitter(calc_uncertainties=True)
    x, y = (bdf_1['T'].to_numpy(), bdf_1['Q_AB'].to_numpy())
    fitted_model = fitter(model, x, y)
    return fitted_model, fitter, model, x, y


@app.cell
def __(mo):
    mo.md(r"""Note that the LMLSQFitter did not work, strangely, but this Trust Region Reflective algorithm works fine""")
    return


@app.cell
def __(fitted_model):
    fitted_model
    return


@app.cell
def __(fitter):
    fitter.fit_info
    return


@app.cell
def __(mo):
    mo.md(r"""Amazingly, it converged with only 4 function evaluations!""")
    return


@app.cell
def __(fitter, np):
    np.sqrt(np.diagonal(fitter.fit_info.param_cov))
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        The param_cov can be used to estimate the uncertainties in the parameters, which are very low. 

        More important to look at the residuals:
        """
    )
    return


@app.cell
def __(fitted_model, pl, x, y):
    residuals = y - fitted_model(x)
    pl.Series(residuals).describe()
    return (residuals,)


@app.cell
def __(mo):
    mo.md(
        r"""
        So the rms residual is 0.07, which is not bad. If I allow the power law index to vary, then this is reduced to about 0.02. Taking the compromise power law index of -0.95, we still keep the rms at 0.03.

        Now, we add the model and residual to the dataframe and look at the graph:
        """
    )
    return


@app.cell
def __(bdf_1, fitted_model, residuals, x):
    bdf_2 = bdf_1.with_columns(Q_AB_fit=fitted_model(x), Q_AB_residual=10 * residuals)
    return (bdf_2,)


@app.cell
def __(bdf_2, plt):
    fig_5, ax_5 = plt.subplots()
    line_3, = ax_5.plot('T', 'Q_AB', label='$Q_\\mathrm{AB}$: 4363 / 5007', data=bdf_2)
    ax_5.plot('T', 'Q_AB_fit', label='fit', data=bdf_2, color='r', lw=line_3.get_lw() / 4)
    ax_5.plot('T', 'Q_AB_residual', label='10 x residual', data=bdf_2, color='g', lw=line_3.get_lw() / 4)
    ax_5.axhline(color='k', lw=0.5)
    ax_5.legend()
    ax_5.set(xscale='log', xlabel='Temperature, K', ylabel='Bias factor, $Q$')
    fig_5
    return ax_5, fig_5, line_3


@app.cell
def __(mo):
    mo.md(
        r"""
        So that looks really good. The residuals are about as good as for the 4th order polynomial fit, but with 2 parameters instead of 5!

        The main problems are:
        (1) the discontinuity at about 25000 K, which is a problem with PyNeb. 
        (2) Inaccuracies at the lowest T, which is at least partially due to the edge effects with the numerical derivative calculation, but also suggests that power law index of -1 is not quite right.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"""### Repeat for $Q_\mathrm{BC}$""")
    return


@app.cell
def __(bdf_2, fitting, models):
    model_1 = models.PowerLaw1D(x_0=10000.0, alpha=0.95, fixed={'x_0': True, 'alpha': True}) + models.Const1D(amplitude=-1.1, fixed={'amplitude': True})
    fitter_1 = fitting.TRFLSQFitter(calc_uncertainties=True)
    x_1, y_1 = (bdf_2['T'].to_numpy(), bdf_2['Q_BC PP13'].to_numpy())
    fitted_model_1 = fitter_1(model_1, x_1, y_1)
    return fitted_model_1, fitter_1, model_1, x_1, y_1


@app.cell
def __(fitted_model_1):
    fitted_model_1
    return


@app.cell
def __(fitter_1):
    fitter_1.fit_info
    return


@app.cell
def __(fitter_1, np):
    np.sqrt(np.diagonal(fitter_1.fit_info.param_cov))
    return


@app.cell
def __(fitted_model_1, pl, x_1, y_1):
    residuals_1 = y_1 - fitted_model_1(x_1)
    pl.Series(residuals_1).describe()
    return (residuals_1,)


@app.cell
def __(mo):
    mo.md(r"""So the rms residuals are 0.03 with fixed index, or 0.01 with varying index. Or 0.02 with index and offset fixed at the values from the Q_AB fit.""")
    return


@app.cell
def __(bdf_2, fitted_model_1, residuals_1, x_1):
    bdf_3 = bdf_2.with_columns(Q_BC_fit=fitted_model_1(x_1), Q_BC_residual=10 * residuals_1)
    return (bdf_3,)


@app.cell
def __(bdf_3, plt):
    fig_6, ax_6 = plt.subplots()
    line_4, = ax_6.plot('T', 'Q_BC', label='$Q_\\mathrm{BC}$: 5007 / V1', data=bdf_3)
    ax_6.plot('T', 'Q_BC PP13', label='', data=bdf_3, color=line_4.get_color(), lw=line_4.get_lw() / 4)
    ax_6.plot('T', 'Q_BC_fit', label='fit', data=bdf_3, color='r', lw=line_4.get_lw() / 4)
    ax_6.plot('T', 'Q_BC_residual', label='10 x residual', data=bdf_3, color='g', lw=line_4.get_lw() / 4)
    ax_6.axhline(color='k', lw=0.5)
    ax_6.legend()
    ax_6.set(xscale='log', xlabel='Temperature, K', ylabel='Bias factor, $Q$')
    fig_6
    return ax_6, fig_6, line_4


@app.cell
def __(mo):
    mo.md(r"""## Summary of functional fits to the Q bias factors""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        The 3-parameter fits are as follows:

        \[
        Q_\mathrm{AB} = 4.80\, T_4^{-0.96} - 1.09
        \]

        and

        \[
        Q_\mathrm{BC} = 1.57\, T_4^{-0.94} - 1.16
        \]

        Strangely, we need blank line before and after each displayed math equation in marimo
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        The compromise fits are as follows:

        $$
        Q_\mathrm{AB} = 4.83\, T_4^{-0.95} - 1.10
        $$

        and

        $$
        Q_\mathrm{BC} = 1.52\, T_4^{-0.95} - 1.10
        $$
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        The second pair are clearly better because they greatly simpify the bias difference:

        $$
        Q_\mathrm{AB} - Q_\mathrm{BC} = 3.23\, T_4^{-0.95}
        $$
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"""The residuals of these fits are of order 0.03 or less, which is better than the accuracy of the Taylor expansion in the t2 analysis, which has relative truncation error of order $Q t^2 \approx 0.1$.""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Comparison with Peimbert & Peimbert's bias factors

        Equations (10, 11) of PP2013 give the Q values as the term in parentheses divided by 2.
        """
    )
    return


@app.cell
def __():
    def Q_AB(T):
        return (4.83 * (T / 1e4) ** -0.95) - 1.10

    def Q_BC(T):
        return (1.52 * (T / 1e4) ** -0.95) - 1.10

    def Q_AB_PP(T):
        return 0.5 * ((91300 / T) - 2.68)

    def Q_BC_PP(T):
        fac = 29160 / T
        return 0.5 * (fac - 3.095 + 0.415 / (fac + 0.415))
    return Q_AB, Q_AB_PP, Q_BC, Q_BC_PP


@app.cell
def __(Q_AB, Q_AB_PP, Q_BC, Q_BC_PP, plt, temperatures):
    fig_7, ax_7 = plt.subplots()
    line_5, = ax_7.plot(temperatures, Q_AB(temperatures), label='$Q_\\mathrm{AB}$: 4363 / 5007')
    ax_7.plot(temperatures, Q_AB_PP(temperatures), label='', color=line_5.get_color(), lw=line_5.get_lw(), ls='dashed')
    line_5, = ax_7.plot(temperatures, Q_BC(temperatures), label='$Q_\\mathrm{BC}$: 5007 / V1')
    ax_7.plot(temperatures, Q_BC_PP(temperatures), label='', color=line_5.get_color(), lw=line_5.get_lw(), ls='dashed')
    ax_7.axhline(color='k', lw=0.5)
    ax_7.legend()
    ax_7.set(xscale='log', xlabel='Temperature, K', ylabel='Bias factor, $Q$')
    fig_7
    return ax_7, fig_7, line_5


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Repeat everything for [N II]

        Here we only have the collisional lines to deal with, since there are no  recombination N I lines.
        """
    )
    return


@app.cell
def __(pn):
    niic = pn.Atom("N", 2)
    niic.getTransition(5755)
    return (niic,)


@app.cell
def __(niic, temperatures):
    density_3 = 100.0
    em6583 = niic.getEmissivity(tem=temperatures, den=density_3, wave=6583)
    em5755 = niic.getEmissivity(tem=temperatures, den=density_3, wave=5755)
    return density_3, em5755, em6583


@app.cell
def __(em5755, em6583, normalize, plt, sns, temperatures):
    fig_8, ax_8 = plt.subplots(figsize=(7, 7))
    density_4 = 100.0
    T0_2 = 10000.0
    em_2 = em6583
    em_2 = normalize(temperatures, em_2)
    ax_8.plot(temperatures, em_2, label='[N II] 6583', ls='-', lw=2.5)
    em_2 = em5755
    em_2 = normalize(temperatures, em_2)
    ax_8.plot(temperatures, em_2, label='[N II] 5755', ls='-.', lw=2.5)
    for slope_2 in [-1, 0, 1, 2, 3, 4, 5, 6, 7]:
        ax_8.plot(temperatures, (temperatures / T0_2) ** slope_2, label=None, lw=1, alpha=0.2, color='k')
    annotate_kws_2 = dict(fontsize='small', horizontalalignment='center', verticalalignment='center_baseline')
    ax_8.annotate('$T^{-1}$', (40000.0, (40000.0 / T0_2) ** (-1)), **annotate_kws_2)
    ax_8.annotate('$T^{2}$', (40000.0, (40000.0 / T0_2) ** 2), **annotate_kws_2)
    ax_8.annotate('$T^{7}$', (20000.0, (20000.0 / T0_2) ** 7), **annotate_kws_2)
    ax_8.legend(fontsize='small')
    ax_8.set(xscale='log', yscale='log', ylim=[0.01, 1000.0], xlim=[None, None], xlabel='Temperature, K', ylabel='Relative emissivity')
    sns.despine()
    fig_8.tight_layout()
    fig_8.savefig('nplus-emissivity-vs-t-loglog.pdf')
    fig_8
    return T0_2, annotate_kws_2, ax_8, density_4, em_2, fig_8, slope_2


@app.cell
def __(em5755, em6583, np, temperatures):
    q5755 = np.gradient(np.log(em5755), np.log(temperatures))
    q6583 = np.gradient(np.log(em6583), np.log(temperatures))
    return q5755, q6583


@app.cell
def __(pl, q5755, q6583, temperatures):
    ndf = pl.DataFrame(
        {
            "T": temperatures,
            "qA": q5755,
            "qB": q6583,
        }
    )
    ndf[::20]
    return (ndf,)


@app.cell
def __(ndf, plt):
    fig_9, ax_9 = plt.subplots()
    ax_9.plot('T', 'qA', label='[N II] 5755', data=ndf)
    ax_9.plot('T', 'qB', label='[N II] 6583', data=ndf)
    ax_9.axhline(color='k', lw=0.5)
    ax_9.legend()
    ax_9.set(xscale='log', xlabel='Temperature, K', ylabel='Emissivity slope index, $q$')
    fig_9
    return ax_9, fig_9


@app.cell
def __(bias, ndf, pl):
    nbdf = ndf.select(
        pl.col("T"),
        bias(pl.col("qA"), pl.col("qB")).alias("Q_AB"),
    )
    nbdf[::20]
    return (nbdf,)


@app.cell
def __(fitter_1, models, nbdf):
    model_2 = models.PowerLaw1D(x_0=10000.0, alpha=0.95, fixed={'x_0': True, 'alpha': False}) + models.Const1D(amplitude=-1.1, fixed={'amplitude': False})
    x_2, y_2 = (nbdf['T'].to_numpy(), nbdf['Q_AB'].to_numpy())
    fitted_model_2 = fitter_1(model_2, x_2, y_2)
    fitted_model_2
    return fitted_model_2, model_2, x_2, y_2


@app.cell
def __(fitted_model_2, pl, x_2, y_2):
    residuals_2 = y_2 - fitted_model_2(x_2)
    pl.Series(residuals_2).describe()
    return (residuals_2,)


@app.cell
def __(fitted_model_2, nbdf, residuals_2, x_2):
    nbdf_1 = nbdf.with_columns(Q_AB_fit=fitted_model_2(x_2), Q_AB_residual=10 * residuals_2)
    return (nbdf_1,)


@app.cell
def __(nbdf_1, plt):
    fig_10, ax_10 = plt.subplots()
    line_6, = ax_10.plot('T', 'Q_AB', label='$Q_\\mathrm{AB}$: 5755 / 6583', data=nbdf_1)
    ax_10.plot('T', 'Q_AB_fit', label='fit', data=nbdf_1, color='r', lw=line_6.get_lw() / 4)
    ax_10.plot('T', 'Q_AB_residual', label='10 x residual', data=nbdf_1, color='g', lw=line_6.get_lw() / 4)
    ax_10.axhline(color='k', lw=0.5)
    ax_10.legend()
    ax_10.set(xscale='log', xlabel='Temperature, K', ylabel='Bias factor, $Q$')
    ...
    return ax_10, fig_10, line_6


@app.cell
def __(mo):
    mo.md(r"""So rms residuals of 0.02 or so.""")
    return


@app.cell
def __():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

"""
Tools to fit a zp from a color transformation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from saltworks.plottools import binplot
from saltworks.linearmodels import RobustLinearSolver, linear_func, indic
from saltworks.indextools import make_index

from .match import match

# pylint: disable=invalid-name,too-many-locals,too-many-arguments


def get_matched_cats(survey, star_lc_cat, logger, by=None, **kwargs):
    """Align secondary star catalog with star lc catalog

    :param survey: secondary star catalog provider
    :param recarray star_lc_cat: lc averaged catalog
    :param logger: logger
    :param dict by: loop over values given by dict unique key
    :return recarray star_selec: aligned secondary star catalog
    :return recarray lc_selec: aligned lc star catalog
    :return list index: selected index of secondary catalog
    """
    if by is None:
        star_selec, lc_selec, index = _get_matched_cats(survey, star_lc_cat, **kwargs)
        logger.info(f"number of stars in lc catalog: {len(star_lc_cat)}")
        logger.info(f"number of stars considered in ref catalog: {len(index)}")
        logger.info(f"number of match with ref catalog: {len(star_selec)}")
        return star_selec, lc_selec

    key = list(by.keys())[0]
    stack_star = []
    stack_lc = []

    for k in by[key]:
        _star_lc_cat = star_lc_cat[star_lc_cat[key] == k]
        kwargs[key] = k
        star_selec, lc_selec, index = _get_matched_cats(survey, _star_lc_cat, **kwargs)
        logger.info(k)
        logger.info(f"number of stars in lc catalog: {len(_star_lc_cat)}")
        logger.info(f"number of stars considered in ref catalog: {len(index)}")
        logger.info(f"number of match with ref catalog: {len(star_selec)}")
        stack_star.append(star_selec)
        stack_lc.append(lc_selec)

    star_selec = np.hstack(stack_star)
    lc_selec = np.hstack(stack_lc)
    return star_selec, lc_selec


def _get_matched_cats(survey, star_lc_cat, arcsecrad=1, **kwargs):

    star_cat = survey.get_secondary_star_catalog(**kwargs)
    if isinstance(star_cat, pd.DataFrame):
        star_cat = star_cat.to_records()

    selec = np.isfinite(star_lc_cat["ra"]) & np.isfinite(star_lc_cat["dec"])
    if isinstance(star_lc_cat, pd.DataFrame):
        star_lc_cat = star_lc_cat.to_records()
    star_lc_cat = star_lc_cat[selec]
    ra_bounds = star_lc_cat["ra"].min(), star_lc_cat["ra"].max()
    dec_bounds = star_lc_cat["dec"].min(), star_lc_cat["dec"].max()

    selec = (star_cat["ra"] > ra_bounds[0] - 0.2) & (
        star_cat["ra"] < ra_bounds[1] + 0.2
    )
    selec &= (star_cat["dec"] > dec_bounds[0] - 0.2) & (
        star_cat["dec"] < dec_bounds[1] + 0.2
    )
    star_cat = star_cat[selec]

    index = match(star_lc_cat, star_cat, arcsecrad=arcsecrad)
    star_selec = star_cat[index != -1]
    lc_selec = star_lc_cat[index[index != -1]]

    return star_selec, lc_selec, index

# pylint: disable=dangerous-default-value
def plot_diff_mag(
    survey,
    star_selec,
    lc_selec,
    xlabel="mag",
    lims=[-0.2, 0.2],
    fig=None,
    axs=None,
    **kwargs,
):
    """Plot mag difference between lc and secondary star catalogs.

    :param survey: secondary star catalog provider
    :param recarray star_selec: aligned secondary star catalog
    :param recarray lc_selec: aligned light curve star catalog
    :param str xlabel: can be mag or color
    :return: fig, ax
    """
    nband = len(survey.bands)
    nx, ny = (nband, 1) if nband < 4 else (nband // 2 + 1, 2)

    if axs is None:
        fig, axs = plt.subplots(nx, ny, sharex=True, sharey=True)
    axs = axs.flatten()
    for ax, band in zip(axs, survey.bands):
        labels = survey.get_secondary_labels(band, **kwargs)
        mag = -2.5 * np.log10(lc_selec[f"flux_{band}"])
        if labels["mag"] not in star_selec.dtype.names:
            continue
        mag0 = star_selec[labels["mag"]]
        diff = mag - mag0
        x = (
            mag0
            if xlabel == "mag"
            else star_selec[labels[xlabel][0]] - star_selec[labels[xlabel][1]]
        )
        goods = np.isfinite(x)
        binplot(x[goods], diff[goods] - np.nanmean(diff), ax=ax)
        ax.grid("on")
        ax.set_ylim(*lims)
        ax.set_ylabel(f"{band}: aper-psf")
    axs[-1].set_xlabel(xlabel)
    if nband > 3:
        axs[-2].set_xlabel(xlabel)
    return fig, axs


def compute_zp(
    survey,
    band,
    lc_selec,
    star_selec,
    color_range,
    zpkey="ccd",
    error_floor=0,
    **kwargs,
):
    """Fit a zp per zpkey (like ccd, name) and a joined linear color term

    :param survey: secondary star catalog provider
    :param band: band name
    :param recarray star_selec: aligned secondary star catalog
    :param recarray lc_selec: aligned light curve star catalog
    :param list color_range: color range on which the fit is done
    :param str zpkey: column name of lc_selec on which zp apply
    :return dict dfit: dict with all fitted quantities
    """

    labels = survey.get_secondary_labels(band, **kwargs)
    mag_psf = -2.5 * np.log10(lc_selec[f"flux_{band}"])
    emag_psf = 1.08 * (lc_selec[f"eflux_{band}"] / lc_selec[f"flux_{band}"])

    mag_ap = star_selec[labels["mag"]]
    emag_ap = star_selec[labels["emag"]]

    color = star_selec[labels["color"][0]] - star_selec[labels["color"][1]]
    wcolor = np.sqrt(1 / (emag_psf**2 + emag_ap**2 + error_floor**2))

    goods = (np.isfinite(mag_psf)) & (np.isfinite(mag_ap))
    goods &= (np.isfinite(color)) & (np.isfinite(wcolor))
    goods &= (color > color_range[0]) & (color < color_range[1])
    for k, v in labels["goods"].items():
        goods &= star_selec[k] > v
    goods &= (mag_ap < labels["mag_cut"][1]) & (mag_ap > labels["mag_cut"][0])

    y = np.array((mag_psf - mag_ap))
    w = np.array(wcolor)  # w = np.ones((goods.sum()))

    model = linear_func(color[goods], name="alpha") + indic(
        np.array(lc_selec[zpkey])[goods], name="beta"
    )
    solver = RobustLinearSolver(model, y[goods], weights=w[goods])
    x = solver.robust_solution(nsig=3)
    model.params.free = x
    res = solver.get_res(y[goods], x)
    err = np.sqrt(solver.get_cov().diagonal())

    return dict(
        {
            "y": y,
            "x": x,
            "color": color,
            "res": res,
            "err": err,
            "mag": mag_ap,
            "goods": goods,
            "bads": solver.bads,
            "w": w,
            "model": model(),
            "wres": solver.get_wres(x=x),
        }
    )

# pylint: disable=dangerous-default-value
def plot_zpfit_res(
    zpfits,
    xlabel="mag",
    lims=[-0.03, 0.03],
    fig=None,
    axs=None,
):
    """Plot zp fit residuals.


    :param str xlabel: can be mag or color
    :return: fig, ax
    """
    bands = list(zpfits.keys())

    nband = len(bands)
    nx, ny = (nband, 1) if nband < 4 else (nband // 2 + nband % 2, 2)

    if axs is None:
        fig, axs = plt.subplots(nx, ny, sharex=True, sharey=True)
    axs = axs.flatten()
    for ax, band in zip(axs, bands):
        _dfit = zpfits[band]
        binplot(
            np.array(_dfit[xlabel][_dfit["goods"]]),
            np.array(_dfit["res"]),
            ax=ax,
            data=True,
            label=band,
        )
        ax.grid("on")
        ax.set_ylim(*lims)
        ax.legend()
    axs[-1].set_xlabel(xlabel)
    if nband > 3:
        axs[-2].set_xlabel(xlabel)
    plt.tight_layout()
    return fig, axs


def zpfit_diagnostic(dfit, nbins=15):
    """Plot zpfit diagnostic including rms of the residual compared to
    measurement error and chi2.
    """
    # rms vs predicted error, chi2
    bads = dfit["bads"]
    y = dfit["res"]
    wres = dfit["wres"]

    fig, ax = plt.subplots(2, 2, figsize=(15, 5), sharex="col")
    ax = list(ax.flatten())
    for x, (ax0, ax1), xlabel in zip(
        [dfit["mag"][dfit["goods"]], dfit["color"][dfit["goods"]]],
        [[ax[0], ax[2]], [ax[1], ax[3]]],
        ["mag", "color"],
    ):
        _, xbinned, xerr, index = make_bins(x, nbins)
        ngood = np.array([(~bads[e]).sum() for e in index])

        mean_y2 = np.array([(y[e][~bads[e]] ** 2).sum() for e in index]) / ngood
        mean_2y = (np.array([y[e][~bads[e]].sum() for e in index]) / ngood) ** 2
        chi2 = np.array([(wres[e][~bads[e]] ** 2).sum() for e in index]) / (ngood - 1)
        rms = np.sqrt(mean_y2 - mean_2y)
        # nmeas = np.array([len(y[e]) for e in index])

        yerr = np.sqrt(1 / dfit["w"][dfit["goods"]] ** 2)
        yerr = [yerr[e].mean() for e in index]

        ax0.errorbar(xbinned, rms, xerr=xerr, ls="None", marker="+", label="res rms")
        ax0.errorbar(
            xbinned, yerr, xerr=xerr, ls="None", marker="+", label="predicted errors"
        )
        ax1.errorbar(
            xbinned, chi2, xerr=xerr, ls="None", marker="+", label="chi2 / dof"
        )
        ax1.set_ylim(0, 0.1)
        ax1.set_ylim(0.5, 10)
        ax1.set_yscale("log")
        ax0.legend()
        ax1.legend()
        ax1.axhline(y=1, color="k", ls="--")
        ax1.set_xlabel(xlabel)
    return fig, ax


def make_bins(x, nbins):
    """Define nbins bin in x.
    :param array x: x
    :param int nbins: number of bins
    :return array bins: bins limit
    :return array xbinned: binned version of x
    :return array xerr: bins size
    :return array index: index of x corresponding to each bin
    """
    bins = np.linspace(x.min(), x.max() + abs(x.max() * 1e-7), nbins + 1)
    yd = np.digitize(x, bins)
    index = make_index(yd)
    xbinned = 0.5 * (bins[:-1] + bins[1:])
    usedbins = np.array(np.sort(list(set(yd)))) - 1
    xbinned = xbinned[usedbins]
    bins = bins[usedbins + 1]
    xerr = np.array([bins, bins]) - np.array([xbinned, xbinned])
    return bins, xbinned, xerr, index

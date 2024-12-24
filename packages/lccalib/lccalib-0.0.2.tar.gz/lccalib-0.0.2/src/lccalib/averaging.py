"""
Tools to make a single light curve catalog with averaged flux
"""
import os
import itertools
import ssl
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

from astroquery.gaia import GaiaClass
from astropy.table import vstack

from saltworks.linearmodels import LinearModel, RobustLinearSolver
from saltworks.plottools import binplot
from saltworks.dataproxy import DataProxy

from .match import match

#pylint: disable=invalid-name,too-many-locals, too-many-arguments,dangerous-default-value

def get_gaia_match(stars, offset=0.02, maxq=5000):
    """Return aligned Gaia and input star subset catalog.

    TODO: apply pm.
    """
    # pylint: disable=protected-access
    _create_unverified_https_context = ssl._create_unverified_context
    ssl._create_default_https_context = _create_unverified_https_context

    gaia = GaiaClass(
        gaia_tap_server="https://gea.esac.esa.int/",
        gaia_data_server="https://gea.esac.esa.int/",
        )
    ra_min, dec_min = stars["ra"].min() - offset, stars["dec"].min() - offset
    ra_max, dec_max = stars["ra"].max() + offset, stars["dec"].max() + offset

    # pylint: disable=line-too-long
    #query = f"select TOP {maxq} source_id, ra, dec from gaiadr3.gaia_source where has_xp_continuous = 'True' and  ra <= {ra_max} and ra >= {ra_min} and dec <= {dec_max} and dec >= {dec_min}"
    query = f"select TOP {maxq} source_id, ra, dec from gaiadr3.gaia_source where ra <= {ra_max} and ra >= {ra_min} and dec <= {dec_max} and dec >= {dec_min}"
    # job = gaia.launch_job_async(query, dump_to_file=False)
    job = gaia.launch_job(query, dump_to_file=False)
    gaia_ids = job.get_results()
    if len(gaia_ids) > maxq-100: # split in 4 if close to 5000, but no more
        gaia_ids = []
        ra2 = (ra_max+ra_min)/2
        dec2 = (dec_max+dec_min)/2
        for _ra_min, _ra_max, _dec_min, _dec_max in [(ra_min, ra2, dec_min, dec2),
                                                     (ra_min, ra2, dec2, dec_max),
                                                     (ra2, ra_max, dec_min, dec2),
                                                     (ra2, ra_max, dec2, dec_max)]:
            query = f"select TOP {maxq} source_id, ra, dec from gaiadr3.gaia_source where ra <= {_ra_max} and ra >= {_ra_min} and dec <= {_dec_max} and dec >= {_dec_min}"
            job = gaia.launch_job(query, dump_to_file=False)
            gaia_ids.append(job.get_results())
        gaia_ids = vstack(gaia_ids)
    index = match(gaia_ids, stars, arcsecrad=20)
    selected_stars = stars[index != -1]
    selected_ids = gaia_ids[index[index != -1]]
    return selected_ids.to_pandas(), selected_stars, index


def cut_from_epoch_number(T, min_d=3):
    """cut stars with less than 3 epochs"""
    if min_d < 1:
        return T
    nstar = int(T["index"].max() + 1)
    dates = set(T["mjd"].astype(int))
    ndate = len(dates)
    D = np.zeros((nstar, ndate))
    vdate = T["mjd"].astype(int)
    for i, d in enumerate(dates):
        dt = T[vdate == d]
        D[dt["index"].astype(int), i] += 1
    ikeep = np.sum(D, axis=1) > min_d
    #print(("cut %d/%d" % (len(ikeep) - ikeep.sum(), len(ikeep))))
    T = T[ikeep[T["index"].astype(int)]]
    return T

def star_lc_averager(
    T, star_key="star", flux_key="flux", eflux_key="error", error_floor=0, show=False
):
    """Compute average flux and associated errors."""
    # pylint: disable=E1101
    # pylint: disable=E1130
    dp = DataProxy(T, flux=flux_key, eflux=eflux_key)
    dp.add_field("star", T[star_key].astype(int))
    dp.make_index("star", intmap=True)

    weights = 1.0 / np.sqrt(dp.eflux**2 + error_floor)

    model = LinearModel(list(range(len(dp.nt))), dp.star_index, np.ones_like(dp.flux))
    solver = RobustLinearSolver(model, np.array(dp.flux), weights=np.array(weights))
    avg_flux = solver.robust_solution(nsig=3)
    solver.model.params.free = avg_flux
    res = solver.get_res(dp.flux)
    wres = solver.get_wres(avg_flux)
    ngood = np.bincount(dp.star_index, ~solver.bads)
    nz = 0
    while ngood[-1]==0:
        ngood = ngood[:-1]
        nz += 1
    index = dp.star_index[~solver.bads]
    mean_y2 = np.bincount(index, weights=dp.flux[~solver.bads] ** 2) / ngood
    mean_2y = (np.bincount(index, weights=dp.flux[~solver.bads]) / ngood) ** 2
    chi2 = np.bincount(index, weights=wres[~solver.bads] ** 2) / (ngood - 1)
    err = np.sqrt(solver.get_cov().diagonal())
    with np.errstate(divide="ignore", invalid="ignore"):
        avg_cat = pd.DataFrame(
            data={
                "star": dp.star_set if not nz else dp.star_set[:-nz],
                "flux": avg_flux if not nz else avg_flux[:-nz],
                "eflux": err if not nz else err[:-nz],
                "rms": np.sqrt(mean_y2 - mean_2y),
                "nmeas": np.bincount(index),
                "chi2": chi2,
            }
        )

    if show:
        plot_star_averager(avg_cat, res=res, dp=dp, goods=~solver.bads)
    return avg_cat, index, ~solver.bads


def add_columns(avg_cat, T, names, index, goods):
    """Complete average catalog with columns"""
    N = np.bincount(index)
    d = {}
    with np.errstate(divide="ignore", invalid="ignore"):
        for n in names:
            avg = np.bincount(index, T[n][goods]) / N
            d[n] = avg
    avg_cat = avg_cat.assign(**d)
    return avg_cat


def plot_night_averager(avg_cat, single=True, **kwargs):
    """Show a comparison of residual dispersion and expected errors for
    the night average fit, stacked over several nights.
    """
    if single:
        return plot_single_night_averager(avg_cat, **kwargs)
    fig, ax = plt.subplots(2, 2)  # , sharex=True, sharey=True)
    ax = list(ax.flatten())
    mag = -2.5 * np.log10(avg_cat["flux"])
    for x, ax0, ax1, xlabel in zip(
        [avg_cat["mjd"].to_numpy(), mag.to_numpy()],
        [ax[0], ax[1]],
        [ax[2], ax[3]],
        ["mjd", "mag"],
    ):
        binplot(
            x,
            (avg_cat["eflux"] / avg_cat["flux"]).to_numpy(),
            label="predicted errors",
            ax=ax0,
            data=False,
        )

        binplot(
            x,
            (avg_cat["rms"] / avg_cat["flux"]).to_numpy(),
            color="r",
            label="res rms",
            ax=ax0,
        )
        ax0.grid()
        ax0.set_ylabel(r"$\sigma_f / f$")
        ax0.legend()
        binplot(x, avg_cat["chi2"].to_numpy(), ax=ax1)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel("chi2")
        ax1.grid()
    fig.tight_layout()
    return fig, ax


def plot_single_night_averager(avg_cat, res=None, dp=None):
    """Averager control plots."""
    N = 2 if res is None else 3
    fig, ax = plt.subplots(N, 1, sharex=True)
    ax[0].plot(avg_cat["mjd"], avg_cat["rms"] / avg_cat["flux"], "r.", label="res rms")
    ax[0].plot(
        avg_cat["mjd"],
        avg_cat["eflux"] * np.sqrt(avg_cat["nmeas"]) / avg_cat["flux"],
        "k.",
        label=r"$\sigma_f \sqrt{N} / f$",
    )
    ax[0].grid()
    ax[0].set_ylabel(r"$\sigma_f / f$")
    ax[0].legend()
    ax[1].plot(avg_cat["mjd"], avg_cat["chi2"], "k.")
    ax[1].set_xlabel("mjd")
    ax[1].set_ylabel("chi2")
    ax[1].grid()
    if res is not None:
        binplot(dp.mjd, res, robust=True, ax=ax[2])
        ax[2].plot(dp.mjd, res / dp.flux, "k.")
        ax[2].set_ylabel("res / f")
        ax[2].grid()
    return fig, ax


def plot_star_averager(avg_cat, res=None, dp=None, goods=None):
    """Averager control plots."""
    N = 2 if res is None else 3
    fig, ax = plt.subplots(N, 1, sharex=True, layout="constrained")

    m = -2.5 * np.log10(np.array(avg_cat["flux"]))
    binplot(m, avg_cat["rms"] / avg_cat["flux"], color="r", label="res rms", ax=ax[0])
    binplot(
        m,
        avg_cat["eflux"] * np.sqrt(avg_cat["nmeas"]) / avg_cat["flux"],
        color="k",
        label=r"$\sigma_f \sqrt{N}$",
        ax=ax[0],
    )
    ax[0].grid()
    ax[0].set_ylabel(r"$\sigma_f / f$")
    ax[0].legend()

    ax_histy = ax[1].inset_axes([1.05, 0, 0.25, 1], sharey=ax[1])
    ok = np.isfinite(avg_cat["chi2"])
    ax_histy.hist(
        avg_cat["chi2"][ok],
        bins=10,
        density=True,
        histtype="step",
        color="black",
        orientation="horizontal",
    )
    binplot(m[ok], np.array(avg_cat["chi2"])[ok], ax=ax[1])
    ax[1].set_xlabel("mag")
    ax[1].set_ylabel("chi2")
    ax[1].grid()

    if res is not None:
        ax_histy = ax[2].inset_axes([1.05, 0, 0.25, 1], sharey=ax[2])
        #x = -2.5 * np.log10(dp.flux)[goods]
        y = res[goods]
        res_min, res_max = -10000.0, 10000.0
        xx = np.linspace(res_min, res_max, 1000)
        me, sc = norm.fit(y)
        ax_histy.tick_params(axis="y", labelleft=False)
        ax_histy.hist(
            y,
            bins=50,
            density=True,
            histtype="step",
            color="black",
            orientation="horizontal",
        )
        ax_histy.plot(
            norm.pdf(xx, loc=me, scale=sc), xx, color="black", label=f"{int(sc)}"
        )
        ax_histy.legend(fontsize=8)

        binplot(-2.5 * np.log10(dp.flux), res, robust=True, ax=ax[2])
        ax[2].set_ylabel("res")
        ax[2].set_ylim(res_min, res_max)
        ax[2].grid()
    fig.tight_layout(h_pad=0.1)
    return fig, ax


def night_averager(
    T, mjd_key="mjd", flux_key="flux", eflux_key="error", error_floor=0, show=False
):
    """Compute mean flux per night.

    :param recarray T: input catalog
    :return array avg_cat: mjd, flux, flux_err
    :return array indices: mjd indices
    """
    # pylint: disable=E1101
    # pylint: disable=E1130

    dp = DataProxy(T, flux=flux_key, eflux=eflux_key)
    dp.add_field("mjd", T[mjd_key].astype(int))
    dp.make_index("mjd", intmap=True)

    weights = 1.0 / np.sqrt(dp.eflux**2 + error_floor)
    weights[~np.isfinite(weights)] = 0

    model = LinearModel(list(range(len(dp.nt))), dp.mjd_index, np.ones_like(dp.flux))
    solver = RobustLinearSolver(model, np.array(dp.flux), weights=np.array(weights))
    avg_flux = solver.robust_solution(nsig=3)

    solver.model.params.free = avg_flux
    res = solver.get_res(dp.flux)
    wres = solver.get_wres(avg_flux)
    index = dp.mjd_index[~solver.bads]
    ngood = np.bincount(dp.mjd_index, ~solver.bads)
    with np.errstate(divide="ignore", invalid="ignore"):
        mean_y2 = np.bincount(index, weights=dp.flux[~solver.bads] ** 2) / ngood
        mean_2y = (np.bincount(index, weights=dp.flux[~solver.bads]) / ngood) ** 2
        avg_cat = pd.DataFrame(
            data={
                "mjd": [
                    float(np.mean(T[mjd_key][dp.mjd_index == i]))
                    for i in range(len(dp.mjd_set))
                ],
                "flux": avg_flux,
                "eflux": np.sqrt(solver.get_cov().diagonal()),
                "rms": np.sqrt(mean_y2 - mean_2y),
                "nmeas": np.bincount(index),
                "chi2": np.bincount(index, weights=wres[~solver.bads] ** 2)
                / (ngood - 1),
            }
        )

    if show:
        plot_single_night_averager(avg_cat, res=res, dp=dp)#, goods=~solver.bads)

    return avg_cat, index, ~solver.bads


def chain_averaging(lccat, logger, gaia_match=False, extra_cols=[]):
    """Chain night and star averaging.

    :param recarray lccat: star light curve catalog
    :return recarray cat: night averaged catalog
    :return recaraay star_lc_cat: star averaged catalog
    """
    if not isinstance(lccat, np.recarray):
        lccat = lccat.to_records()
    star_set = list(set(lccat["star"]))
    cat = []
    for s in star_set:
        T = lccat[lccat["star"] == s]
        T = T[T["ra"]!=0] #todo remove this as soon as mklc is fixed
        try:
            cat_, idx, goods = night_averager(
                T,
                mjd_key="mjd",
                flux_key="flux",
                eflux_key="error",
                show=False,
            )
            cat_ = cat_.assign(star=int(s) * np.ones((len(cat_))).astype(int))
            cat_ = add_columns(cat_, T, ["ra", "dec"]+extra_cols, idx, goods)
            cat.append(cat_)
        except: #pylint: disable=bare-except
            logger.warning(
                f"Night averager failed for star {s}"
                f", number of epochs is {len(set(T['mjd'].astype(int)))}"
            )
            cat_ = pd.DataFrame(
                data={
                    "mjd": T["mjd"],
                    "flux": T["flux"],
                    "eflux": T["error"],
                    "star": int(s) * np.ones((len(T))).astype(int),
                    "rms":np.ones((len(T)))*np.nan,
                    "nmeas":np.ones((len(T))),
                    "chi2":np.ones((len(T)))*np.nan,
                })
            d = {}
            for k in ["ra", "dec"]+extra_cols:
                d[k] = T[k]
            cat_ = cat_.assign(**d)
            cat.append(cat_)

    cat = pd.concat(cat)
    cat = cat[np.isfinite(cat["eflux"])]
    cat = cat[np.isfinite(cat["ra"])]

    # cat = cut_from_epoch_number(cat.to_records(), min_d=min_d)
    star_lc_cat, idx, goods = star_lc_averager(
        cat.to_records(),
        star_key="star",
        flux_key="flux",
        eflux_key="eflux",
        show=False,
    )

    star_lc_cat = add_columns(star_lc_cat, cat, ["ra", "dec"]+extra_cols, idx, goods)

    if gaia_match:
        selected_ids, star_lc_cat, _ = get_gaia_match(
            star_lc_cat, offset=0.02, maxq=5000
        )
        star_lc_cat = star_lc_cat.astype({"star": "int64"})
        star_lc_cat["star"] = selected_ids["SOURCE_ID"].astype("int64").values
    return cat, star_lc_cat


def lc_stack(
    d_iterator, fn_provider, bands, cols=["flux", "eflux", "rms", "nmeas", "chi2"]
):
    """Stack all catalogs in a single one

    :param dict d_iterator: keys and values indexing catalogs
    :param func fn_provider: function which return a catalog filename for a given set of key/value
    :param str list bands: list of band names
    :param str list cols: list of columns to stack, named col_band in stacked catalog
    :return recaraay stacked: stacked catalog
    """

    # pylint: disable=no-member

    stacked = []

    for k_i in itertools.product(*d_iterator.values()):
        kwargs = dict(zip(d_iterator.keys(), k_i))

        lc_catalog = []
        for band in bands:
            kwargs["band"] = band
            cat_ = fn_provider(**kwargs)
            if isinstance(cat_, str):
                if os.path.exists(cat_):
                    cat_ = pd.read_parquet(cat_)
                else:
                    continue
            cat_ = cat_.assign(band=np.full(len(cat_), band))
            lc_catalog.append(cat_)
        if len(lc_catalog)==0:
            continue
        lc_catalog = pd.concat(lc_catalog)

        # flux per band as columns
        dp = DataProxy(lc_catalog)
        dp.add_field("star", lc_catalog["star"].astype(int))
        dp.make_index("star")  # , intmap=True)
        reshaped = pd.DataFrame.from_dict({"star": dp.star_set})

        dkey = {}
        for _k, _v in kwargs.items():
            if _k != "band":
                dkey[_k] = [_v] * len(reshaped)
        reshaped = reshaped.assign(**dkey)

        reshaped = add_columns(
            reshaped,
            lc_catalog,
            ["ra", "dec"],
            dp.star_index,
            np.ones((len(dp.star_index))).astype("bool"),
        )
        N = len(reshaped)

        for band in bands:
            selec = lc_catalog["band"] == band
            nancols = dict(
                zip(
                    [c + f"_{band}" for c in cols],
                    [np.ones((N)) * np.nan for i in cols],
                )
            )
            reshaped = reshaped.assign(**nancols)
            for l in cols:
                k = l + f"_{band}"
                i = reshaped.columns.get_loc(k)
                reshaped.iloc[dp.star_index[selec], i] = lc_catalog[l][selec]
        stacked.append(reshaped)
    stacked = pd.concat(stacked)
    return stacked

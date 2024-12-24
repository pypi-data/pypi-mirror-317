"""
Compress a LC catalog by doing a night averaging the flux. 

"""

import numpy as np
import pandas as pd
from lccalib.averaging import night_averager, add_columns
from lccalib.averaging import plot_night_averager

def check_epochs(t, selec, key):
    """ One needs at least 2 measurements to make the average. 
    """
    if selec.sum()<1:
        return False
    return len(set(t[selec][key].astype(int)))>1

    
def compress(sn1ae, snid="snid", mjd="time", extra_cols=["ra", "dec"]):
    """ Perform night averaging for all sn and all band. 

    :return dataframe _all: compressed dataframe. 
    """

    band_set = list(set(sn1ae["band"]))
    sn_set = list(set(sn1ae[snid]))
    print(len(band_set), " bands ", len(sn_set), " sn")
    _all = [] #loop over sn and band
    for band in band_set:
        print(band)
        bselec = sn1ae["band"]==band
        for isn, sn in enumerate(sn_set):
            selec = bselec & (sn1ae[snid]==sn)
            if selec.sum()>0 and check_epochs(sn1ae, selec, mjd):
                # flux averaging
                cat, idx, goods = night_averager(sn1ae[selec],
                                                 mjd_key=mjd,
                                                 flux_key="flux",
                                                 eflux_key="fluxerr")
                cat = cat.assign(name=np.full(len(cat), sn))
                cat = cat.assign(band=np.full(len(cat), band))

                # averaging other quantities
                if extra_cols:
                    cat = add_columns(cat, sn1ae[selec], extra_cols, idx, goods)
                _all.append(cat)
            else:
                #if selec.sum()>0:
                #    print("Not enough measurements", sn1ae[selec][mjd])
                continue

    _all = pd.concat(_all)
    print(f"raw dataframe {len(sn1ae)} rows, after compression {len(_all)}")
    return _all

def check_compression(avg_sn1ae, snid="snid", mjd="time"):
    band_set = list(set(avg_sn1ae["band"]))
    sn_set = list(set(avg_sn1ae[snid]))
    for band in band_set:
        bselec = avg_sn1ae["band"]==band
        for isn, sn in enumerate(sn_set):
            selec = bselec & (avg_sn1ae[snid]==sn)
            _byint = avg_sn1ae[selec][mjd].astype(int)
            assert len(np.unique(_byint.astype(int))) == len(_byint)

if __name__ == '__main__':

    sn1ae = pd.read_csv("DC1_lcs.csv")

    # we use a subset for the demo
    band_subset = ['ztf'+b for b in ['g', 'r', 'i']]
    mask = sn1ae['band'].isin(band_subset) 
    sn1ae = sn1ae[mask]

    # do night averaging
    sn1ae = sn1ae.to_records()
    avg_sn1ae = compress(sn1ae, snid="sn_id", mjd="mjd", extra_cols=[])

    # check it
    check_compression(avg_sn1ae, snid="name", mjd="mjd")

    # look at control plot
    selec = avg_sn1ae["nmeas"]>1 # goods
    selec &= avg_sn1ae["flux"]>0
    fig, ax = plot_night_averager(avg_sn1ae[selec], single=False)
    ax[0].set_ylim(0,10)
    ax[1].set_ylim(0,10)
    ax[2].set_ylim(0,250)
    ax[3].set_ylim(0,250)

    # look at the control plots for a given SN
    band = 'ztfr'
    selec = sn1ae["band"]==band
    selec &= sn1ae["sn_id"]==1911
    cat, idx, goods = night_averager(sn1ae[selec],
                                     mjd_key="mjd",
                                     flux_key="flux",
                                     eflux_key="fluxerr",
                                     show=True)
    fig, ax = plt.subplots(1,1)
    ax.plot(sn1ae[selec]["mjd"], sn1ae[selec]["flux"], "k+")
    ax.plot(cat["mjd"], cat["flux"], "b+")

    
    

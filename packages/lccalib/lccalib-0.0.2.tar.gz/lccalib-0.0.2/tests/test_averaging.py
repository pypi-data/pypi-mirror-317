import pandas as pd
import numpy as np

from lccalib.averaging import night_averager, add_columns

def make_raw_cat():
    raw_cat = pd.DataFrame(
        data={
            "mjd": [
                float(54000 + i/20 + j)
                for j in range(10)
                for i in range(10)
            ],
            "flux": 10000. + np.random.randn(100),
            "eflux": np.ones((100)),
        }
    )
    return raw_cat

def test_night_avering():
    raw_cat = make_raw_cat()
    
    avg_cat, _idx, _goods = night_averager(raw_cat,
                                           mjd_key='mjd',
                                           flux_key="flux",
                                           eflux_key="eflux")
    
    assert len(avg_cat)==10

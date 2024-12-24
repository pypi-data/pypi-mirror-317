"""
Interface to various survey inputs.
"""

from abc import ABC, abstractmethod

# pylint:disable=W0221

class Survey(ABC):
    """Abstract class defining the minimum required inputs for any survey."""

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_secondary_star_catalog(self, **kwargs):
        """Return the calibrated secondary stars catalog."""

    @abstractmethod
    def get_secondary_star_lc(self, **kwargs):
        """Return the secondary stars light curves."""

    @abstractmethod
    def get_sne_lc(self, **kwargs):
        """Return the supernovae light curves."""

    @abstractmethod
    def get_secondary_labels(self, band, **kwargs):
        """Return a dictionary giving the column names in secondary catalog.

        The dictionary should looks like:
        >>> dict( {
        >>>       "mag": str,
        >>>        "emag": str,
        >>>        "color": (str, str) ,
        >>>        "goods": dict({str: float}), #name and threshold
        >>>        "mag_cut": (float, float) })
        """

    @abstractmethod
    @property
    def bands(self):
        """Return list of bands"""

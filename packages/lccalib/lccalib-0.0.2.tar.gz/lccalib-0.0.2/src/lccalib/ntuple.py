"""
Tools to read SNLS catalogs, extracted from croaks.NTuple
"""

import numpy as np


def read_header(fh):
    """ Return keys, values from file header. 
    """
    keys = {}
    names = []
    for line in fh:
        if line.startswith("#"):
            if line[1:].strip() == "end":
                break
            names.append(line[1:].split(":")[0].strip())
        elif line.startswith("@"):
            l = line[1:].split()
            keys[l[0]] = convert(" ".join(l[1:]))
    return keys, names


def convert(value):
    """ Convert into python type. 
    """
    value = value.strip()
    if not value:
        value = "nan"
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            pass
    return value


def fromtxt(filename):
    """Return catalog as recarray."""
    #pylint: disable=unspecified-encoding
    comments = set(["#", "\n"])
    with open(filename, "r") as fid:
        keys, names = read_header(fid)
        records = []
        for line in fid:
            if line[0] in comments:
                continue
            vals = line.split()
            records.append([convert(v) for v in vals])
    nt = np.rec.fromrecords(records, names=names)  # .view(NTuple)
    nt.keys = keys
    return nt

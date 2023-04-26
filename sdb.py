import glob
import subprocess
import utils

import astropy.units as au

from tempfile import mkdtemp
from astropy.io import fits

from config import config


class _SimpleSpec():
    def __init__(self):
        self.data = {}
        self.units = {}


def qubrics_spec_by_qid(qid, db):
    spec_list = []
    try:
        for group in db[qid]:
            # from _ you can get wave, flux, err
            _ = _SimpleSpec()
            _.data['wave'] = db[qid][group][:]['wave']
            _.data['flux'] = db[qid][group][:]['flux']
            _.data['sig'] = db[qid][group][:]['error']
            _.units['wave'] = au.AA
            _.units['flux'] = au.dimensionless_unscaled
            _.units['sig'] = au.dimensionless_unscaled
            spec_list.append(_)

        return [spec_list], len(spec_list)
    except KeyError:
        return [None], 0


def get_spectra(RA, DEC, sep, db):
    if utils._is_number(RA):
        return db.spectra_from_coord((RA, DEC), tol=sep*au.arcsec)
    else:
        if "-" not in DEC and "+" not in DEC:
            DEC = "+" + DEC
        return db.spectra_from_coord(RA + DEC, tol=sep*au.arcsec)


def query_db(query, db):
    qmeta = db.query_meta(query)
    return db.spectra_from_meta(qmeta, subset=True)


def write_spec(spec, full_path):
    wave = fits.Column(name='wave', format='D',
                       array=spec.data['wave'].reshape(-1, 1) * spec.units['wave'])
    flux = fits.Column(name='flux', format='D',
                       array=spec.data['flux'].reshape(-1, 1) * spec.units['flux'])
    err = fits.Column(name='err', format='D',
                      array=spec.data['sig'].reshape(-1, 1) * spec.units['flux'])
    hdu = fits.BinTableHDU.from_columns([wave, flux, err])
    hdu.writeto(full_path, overwrite=True)


def open_ac(path):
    ac_params = "  ".join(glob.glob(path + "/*.fits"))
    subprocess.run("python " + config["ac_path"] + "  " + ac_params, shell=True,
                   capture_output=True, text=True)


def write_and_open(spec, path=None, filename="spec"):
    if path is None:
        path = mkdtemp() + "/"
    for (n, _) in enumerate(spec[0]):
        write_spec(_, full_path=path + filename + "_" + str(n) + ".fits")

    open_ac(path)
    return 0

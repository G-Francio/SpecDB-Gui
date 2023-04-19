import glob
import subprocess

import astropy.units as au

from specdb.specdb import SpecDB
from tempfile import mkdtemp
from astropy.io import fits

ACGUI_PATH = "/home/francio/repo/astrocook/ac_gui.py"
sdb = SpecDB(db_file='/media/data/Data/Catalogues/SpecDB/IGMspec_DB_v03.1.hdf5')


def get_spectra(RA, DEC, sep, sdb=sdb):
    if "-" not in DEC and "+" not in DEC:
        DEC = "+" + DEC
    return sdb.spectra_from_coord(RA + DEC, tol=sep*au.arcsec)


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
    subprocess.run("python " + ACGUI_PATH + "  " + ac_params, shell=True,
                   capture_output=True, text=True)


def write_and_open(spec, path=mkdtemp() + "/", filename="spec"):
    for (n, _) in enumerate(spec[0]):
        write_spec(_, full_path=path + filename + "_" + str(n) + ".fits")

    open_ac(path)
    return 0

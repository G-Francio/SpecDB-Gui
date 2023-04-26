import glob
import subprocess
from tempfile import mkdtemp
from astropy.io import fits

from config import config


class InvalidInput(Exception):
    pass


def parse_input(RAs, DECs, RAd, DECd, tol):
    if _all_empty(RAs, DECs, RAd, DECd, tol):
        raise InvalidInput(
            "Please provide coordinates and a matching radius.")

    if not _valid_RAs_DECs(RAs, DECs) and RAd == "" and DECd == "":
        raise InvalidInput(
            "Please provide RAs and DECs coordinates as (01 15 22.14, 03 14 03.13) or (01:15:22.14, 03:14:03.13).")

    if not _is_number(tol):
        raise InvalidInput(
            "The matching radius should be a number (unit: arcsec)")
    _tol = float(tol)

    if not _valid_pairs((RAs, DECs), (RAd, DECd)):
        raise InvalidInput("Please provide both RA and DEC")

    if _is_number(RAd):
        _RA, _DEC = float(RAd), float(DECd)
    else:
        _RA, _DEC = _sub_space_for_color(RAs, DECs)
    return _RA, _DEC, _tol


def parse_qid(qid):
    if not _is_number(qid):
        raise InvalidInput(
            "Please provide a numeric qid.")
    return int(qid)


def _valid_pairs(pair_1, pair_2):
    if (pair_1[0] != "" and pair_1[1] != "") or (pair_2[0] != "" and pair_2[1] != ""):
        return True
    else:
        return False


def _is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def _all_empty(RAs, DECs, RAd, DECd, tol):
    if RAs == "" and DECs == "" and RAd == "" and DECd == "" and tol == "":
        return True
    else:
        return False


def _is_RA_valid(RA):
    if not (":" in RA or " " in RA):
        return False
    return True


def _is_DEC_valid(RA):
    if not (":" in RA or " " in RA):
        return False
    return True


def _valid_RAs_DECs(RA, DEC):
    return _is_RA_valid(RA) and _is_DEC_valid(DEC)


def _sub_space_for_color(RA, DEC):
    return RA.replace(" ", ":"), DEC.replace(" ", ":")


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


def write_spec(spec, full_path):
    wave = fits.Column(name='wave', format='D',
                       array=spec.data['wave'].reshape(-1, 1) * spec.units['wave'])
    flux = fits.Column(name='flux', format='D',
                       array=spec.data['flux'].reshape(-1, 1) * spec.units['flux'])
    err = fits.Column(name='err', format='D',
                      array=spec.data['sig'].reshape(-1, 1) * spec.units['flux'])
    hdu = fits.BinTableHDU.from_columns([wave, flux, err])
    hdu.writeto(full_path, overwrite=True)

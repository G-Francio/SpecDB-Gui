import glob
import subprocess
from tempfile import mkdtemp
from astropy.io import fits

from config import config


class InvalidInput(Exception):
    pass


def parse_input(RAs, DECs, RAd, DECd, tol):
    """Parse and validate user input for RA, DEC, and radius.

    Args:
        RAs (str): Right ascension (RA) in format "HH:MM:SS" or "HH MM SS".
        DECs (str): Declination (DEC) in format "DD:MM:SS" or "DD MM SS".
        RAd (str): Right ascension (RA) as a decimal number.
        DECd (str): Declination (DEC) as a decimal number.
        tol (str): Matching radius in arcseconds as a string.

    Raises:
        InvalidInput: If user input is invalid.

    Returns:
        tuple: A tuple of right ascension, declination, and matching radius.
    """
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
        _RA, _DEC = _sub_space_for_colon(RAs, DECs)
    return _RA, _DEC, _tol


def parse_qid(qid):
    """Parse and validate user input for qid.

    Args:
        qid (str): QID as a string.

    Raises:
        InvalidInput: If query ID is not a valid integer.

    Returns:
        int: The query ID as an integer.
    """
    if not _is_number(qid):
        raise InvalidInput(
            "Please provide a numeric qid.")
    return int(qid)


def _valid_pairs(pair_1, pair_2):
    """Check if both RA and DEC pairs are provided.

    Args:
        pair_1 (tuple): A tuple of two strings representing RA and DEC.
        pair_2 (tuple): A tuple of two strings representing RA and DEC.

    Returns:
        bool: True if both pairs are not empty, False otherwise.
    """
    if (pair_1[0] != "" and pair_1[1] != "") or (pair_2[0] != "" and pair_2[1] != ""):
        return True
    else:
        return False


def _is_number(n):
    """
    Checks if a given input is a number.

    Args:
        n (any): Input to be checked.

    Returns:
        bool: True if the input is a number, False otherwise.
    """
    try:
        float(n)
        return True
    except ValueError:
        return False


def _all_empty(RAs, DECs, RAd, DECd, tol):
    """
    Checks if all the given inputs are empty.

    Args:
        RAs (str): Right Ascension of source in sexagesimal format.
        DECs (str): Declination of source in sexagesimal format.
        RAd (str): Right Ascension of source in decimal format.
        DECd (str): Declination of source in decimal format.
        tol (str): Tolerance in degrees.

    Returns:
        bool: True if all the inputs are empty, False otherwise.
    """
    if RAs == "" and DECs == "" and RAd == "" and DECd == "" and tol == "":
        return True
    else:
        return False


def _is_RA_valid(RA):
    """
    Checks if the given input in RA format is valid.

    Args:
        RA (str): Right Ascension of source.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if not (":" in RA or " " in RA):
        return False
    return True


def _is_DEC_valid(DEC):
    """
    Checks if the given input in DEC format is valid.

    Args:
        DEC (str): Declination of source.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if not (":" in DEC or " " in DEC):
        return False
    return True


def _valid_RAs_DECs(RA, DEC):
    """
    Checks if the given inputs in RA and DEC formats are valid.

    Args:
        RA (str): Right Ascension of source.
        DEC (str): Declination of source.

    Returns:
        bool: True if both inputs are valid, False otherwise.
    """
    return _is_RA_valid(RA) and _is_DEC_valid(DEC)


def _sub_space_for_colon(RA, DEC):
    """
    Substitutes spaces with colons in RA and DEC formats.

    Args:
        RA (str): Right Ascension of source in sexagesimal format.
        DEC (str): Declination of source in sexagesimal format.

    Returns:
        tuple: Tuple of strings with spaces substituted by colons in RA and DEC formats.
    """
    return RA.replace(" ", ":"), DEC.replace(" ", ":")


def open_ac(path):
    """
    Opens Astrocook on FITS files present in the given path.

    Args:
        path (str): Path containing the FITS files.

    Returns:
        None.
    """
    ac_params = "  ".join(glob.glob(path + "/*.fits"))
    subprocess.run("python " + config["ac_path"] + "  " + ac_params, shell=True,
                   capture_output=True, text=True)


def write_and_open(spec, path=None, filename="spec"):
    """
    Converts a given spectrum into FITS files, opens Astrocook on them and returns 0.

    Args:
        spec (obj): A spectrum object.
        path (str, optional): Path where the FITS files will be stored. If None, a temporary directory is created. Defaults to None.
        filename (str, optional): Name of the FITS files. Defaults to "spec".

    Returns:
        int: 0 on successful completion.

    """
    if path is None:
        path = mkdtemp() + "/"
    for (n, _) in enumerate(spec[0]):
        write_spec(_, full_path=path + filename + "_" + str(n) + ".fits")

    open_ac(path)
    return 0


def write_spec(spec, full_path):
    """
    Writes a given spectrum to a FITS file.

    Args:
        spec (obj): A spectrum object.
        full_path (str): Full path of the FITS file.

    Returns:
        None.
    """
    wave = fits.Column(name='wave', format='D',
                       array=spec.data['wave'].reshape(-1, 1) * spec.units['wave'])
    flux = fits.Column(name='flux', format='D',
                       array=spec.data['flux'].reshape(-1, 1) * spec.units['flux'])
    err = fits.Column(name='err', format='D',
                      array=spec.data['sig'].reshape(-1, 1) * spec.units['flux'])
    hdu = fits.BinTableHDU.from_columns([wave, flux, err])
    hdu.writeto(full_path, overwrite=True)

import utils
import astropy.units as au


class _SimpleSpec():
    """
    A class to store spectral data.

    Attributes:
        data (dict): a dictionary to store wave, flux, and sig arrays.
        units (dict): a dictionary to store units for wave, flux, and sig.
    """

    def __init__(self):
        self.data = {}
        self.units = {}


def qubrics_spec_by_qid(qid, db):
    """
    Retrieve a list of SimpleSpec objects from the given database and qid.

    Args:
        qid (int): the QID for the data.
        db (database): a database instance.

    Returns:
        A tuple containing a list of SimpleSpec objects and the number of retrieved spectra.
    """
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
    """
    Retrieve spectral data from the given database using coordinates and separation.

    Args:
        RA (str or float): right ascension coordinate in either string or float format.
        DEC (str or float): declination coordinate in either string or float format..
        sep (float): separation in arcseconds to use for the search.
        db (database): a database instance.

    Returns:
        A list of SimpleSpec objects.
    """
    if utils._is_number(RA):
        return db.spectra_from_coord((RA, DEC), tol=sep*au.arcsec)
    else:
        if "-" not in DEC and "+" not in DEC:
            DEC = "+" + DEC
        return db.spectra_from_coord(RA + DEC, tol=sep*au.arcsec)


def query_db(query, db):
    """
    Retrieve spectral data from the given database using a query.

    Args:
        query (str): a string representing a query to be executed on the Qubrics database.
        db (database): a database instance.

    Returns:
        A list of SimpleSpec objects.
    """
    qmeta = db.query_meta(query)
    return db.spectra_from_meta(qmeta, subset=True)


# Search functions
def _search_qubrics_by_coord(values, db):
    return None, 0


def _search_specdb_by_coord(values, db):
    """
    Searches for spectra in the SpecDB database based on the provided 
    coordinates.

    Parameters:
    -----------
    values : dict
        A dictionary of values containing the input coordinates.
    db : SpecDB
        The SpecDB database object.

    Returns:
    --------
    tuple
        A tuple containing a list of spectra and the number of spectra 
        found.
    """
    RA, DEC, tol = utils.parse_input(
        values['-RA_HMS-'], values['-DEC_DMS-'],
        values['-RA_DEC-'], values['-DEC_DEG-'],
        values['-MATCH_R-'])
    spectra = get_spectra(RA, DEC, tol, db)
    if spectra[0] is None:
        n_spec = 0
    else:
        n_spec = spectra[0].nspec
    return spectra, n_spec


def _search_qubrics_by_qid(values, db):
    """
    Searches for spectra in the QUBRICS database based on the provided qid.

    Parameters:
    -----------
    values : dict
        A dictionary of values containing the input qid.
    db : QubricsDB
        The QUBRICS database object.

    Returns:
    --------
    tuple
        A tuple containing a list of spectra and the number of spectra
        found.
    """
    return qubrics_spec_by_qid(values["-QID-"], db)


def _search_by_query(query, db):
    # try is needed, in case you search by qid in defautls SpecDB databases
    #  otherwise it seems like you crash
    """
    Searches for spectra in the SpecDB database based on the provided query.

    Parameters:
    -----------
    query : dict
        A dictionary containing the query parameters.
    db : SpecDB
        The SpecDB database object.

    Returns:
    --------
    tuple
        A tuple containing a list of spectra and the number of spectra 
        found.
    """
    try:
        spectra = query_db(query, db)
        if spectra[0] is None:
            n_spec = 0
        else:
            n_spec = spectra[0].nspec
        return spectra, n_spec
    except AttributeError:
        return None, 0


def _search_by_qid(values, db):
    """
    Searches for spectra in the SpecDB database based on the provided qid.

    Parameters:
    -----------
    values : dict
        A dictionary of values containing the input qid.
    db : SpecDB
        The SpecDB database object.

    Returns:
    --------
    tuple
        A tuple containing a list of spectra and the number of spectra 
        found.
    """
    qid = utils.parse_qid(values["-QID-"])
    query = {'qid': qid}
    return _search_by_query(query, db)


def search_spectra(values, db, is_qubrics=False):
    """
    Searches for spectra in the SpecDB or QUBRICS database based on the 
    provided values.

    Parameters:
    -----------
    values : dict
        A dictionary of values containing the input coordinates or qid.
    db : SpecDB or QubricsDB
        The database object.
    is_qubrics : bool, optional
        A flag indicating whether to search the QUBRICS database or not.

    Returns:
    --------
    tuple
        A tuple containing a list of spectra and the number of spectra 
        found.
    """
    if values["-QID-"] != "" and is_qubrics:
        return _search_qubrics_by_qid(values, db)
    elif values["-QID-"] != "" and not is_qubrics:
        return _search_by_qid(values, db)
    elif values["-QID-"] == "" and is_qubrics:
        return _search_qubrics_by_coord(values, db)
    elif values["-QID-"] == "" and not is_qubrics:
        return _search_specdb_by_coord(values, db)

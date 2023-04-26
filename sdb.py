import utils
import astropy.units as au


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


# Search functions
def _search_qubrics_by_coord(values, db):
    return None, 0


def _search_specdb_by_coord(values, db):
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
    return qubrics_spec_by_qid(values["-QID-"], db)


def _search_by_query(query, db):
    # try is needed, in case you search by qid in defautls SpecDB databases
    #  otherwise it seems like you crash
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
    qid = utils.parse_qid(values["-QID-"])
    query = {'qid': qid}
    return _search_by_query(query, db)


def search_spectra(values, db, is_qubrics=False):
    if values["-QID-"] != "" and is_qubrics:
        return _search_qubrics_by_qid(values, db)
    elif values["-QID-"] != "" and not is_qubrics:
        return _search_by_qid(values, db)
    elif values["-QID-"] == "" and is_qubrics:
        return _search_qubrics_by_coord(values, db)
    elif values["-QID-"] == "" and not is_qubrics:
        return _search_specdb_by_coord(values, db)

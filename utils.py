class InvalidInput(Exception):
    pass


def parse_input(RAs, DECs, RAd, DECd, tol):
    if _all_empty(RAs, DECs, RAd, DECd, tol):
        raise InvalidInput(
            "Please provide coordinates and a matching radius.")

    if not _valid_RAs_DECs(RAs, DECs) and RAd == "" and DECd == "":
        raise InvalidInput(
            "Please provide RAs and DECs coordinates either as (01 15 22.14, 03 14 03.13) or (01:15:22.14, 03:14:03.13).")

    if not _is_number(tol):
        raise InvalidInput(
            "The matching radius should be a number (unit: arcsec)")
    _tol = float(tol)

    if not _valid_pairs((RAs, DECs), (RAd, DECd)):
        raise InvalidInput("Please provide both RA and DEC")

    if _is_number(RAd):
        _RA, _DEC = RAd, DECd
    else:
        _RA, _DEC = _sub_space_for_color(RAs, DECs)
    return _RA, _DEC, _tol


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

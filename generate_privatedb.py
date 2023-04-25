# imports
from specdb.build import utils as spbu
from specdb.build import privatedb as pbuild
from linetools import utils as ltu
from astropy.table import Table
import glob
import h5py
import warnings
warnings.filterwarnings('ignore')

tree = "/home/francio/private_db/spectra/"
branches = glob.glob(tree + '*')

id_key = 'QUBRICS_ID'
maindb, tkeys = spbu.start_maindb(id_key)

mflux_files, meta_file = pbuild.grab_files(branches[0])
meta_dict = ltu.loadjson(meta_file[0])

# Read redshift, and deal with all shenaningans
ztbl = Table.read("/media/data/Data/Catalogues/QSO_SDSS_Spectra/DR18_DB.fits")
# now some magic to make sure the format is consistent with SpecDB


def get_spec_file(plate, mjd, fiber):
    """
    Generates filenames
    """
    return f"spec-{plate:04}-{mjd}-{fiber:04}.fits"


# Rename cols
ztbl.rename_columns(["RAd", "DECd", "z_spec"], ["RA", "DEC", "ZEM"])

# Add extra, required
ztbl["ZEM_SOURCE"] = "SDSS"
ztbl["SPEC_FILE"] = [get_spec_file(
    ztbl['PLATE'][i][0], ztbl['MJD'][i][0], ztbl['FIBERID'][i][0]) for i in range(len(ztbl['MJD']))]

# Select columns you need
ztbl = ztbl['RA', 'DEC', 'ZEM', 'ZEM_SOURCE', 'SPEC_FILE', 'qid']

# and flatten the one you need to flatten
for colname in ['RA', 'DEC', 'ZEM', 'qid']:
    ztbl[colname] = ztbl[colname].flatten()

# create meta
meta = pbuild.mk_meta(mflux_files, ztbl, fname=False,
                      mdict=meta_dict['meta_dict'], parse_head=meta_dict['parse_head'],
                      mtbl_file="/home/francio/private_db/SDSS_meta.fits")

# add groups and IDS
gdict = {}
flag_g = spbu.add_to_group_dict('QUBRICS', gdict)
maindb = pbuild.add_ids(maindb, meta, flag_g, tkeys,
                        id_key, first=(flag_g == 1))


# create file
hdf = h5py.File('QUBRICS.hdf5', 'w')
pbuild.ingest_spectra(hdf, 'QUBRICS', meta,
                      max_npix=meta_dict['maxpix'])


pbuild.write_hdf(hdf, 'QUBRICS', maindb, [str('SDSS')], gdict, 'v01')

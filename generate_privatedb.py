# imports
from specdb.specdb import IgmSpec
from specdb.build import utils as spbu
from specdb.build import privatedb as pbuild
from linetools import utils as ltu
from astropy.table import Table
import glob
import specdb
import h5py
import warnings
warnings.filterwarnings('ignore')


id_key = 'QUBRICS_Test'
maindb, tkeys = spbu.start_maindb(id_key)

branch = '/home/francio/private_db/SDSS/'
flux_files, meta_file = pbuild.grab_files(branch)

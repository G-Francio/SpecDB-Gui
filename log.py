import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Output logs to console
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)

# Output logs to file
fh = logging.FileHandler('mylog.log')
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)
logger.addHandler(fh)


wrong_db_format = """
The database you choose is formatted according to the SpecDB
standard, but it appears the package is not available.
Either load a QUBRICS' formatted database (and check the
corrisponding box), or install SpecDB and try again.
"""

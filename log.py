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

import logging

logger = logging.getLogger('tbank_kassa')
logger.addHandler(logging.NullHandler())


def setup_logging(level=logging.INFO, fmt=None):
    if fmt is None:
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    logger.setLevel(level)

import logging

from ocpp.v16.call_result import SendLocalList


def get_logger(name: str, debug_level) -> logging.Logger:
    """Function to get a logger

    :param name: Name of the logger"""

    root_logger = logging.getLogger()

    logger = root_logger.getChild(name)

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if debug_level == "DEBUG":
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    elif debug_level == "INFO":
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)

    rotating_file_handler = logging.handlers.RotatingFileHandler(
        filename='ocpp_controler.log',
        maxBytes=1000000,
        backupCount=5
    )
    rotating_file_handler.setFormatter(formatter)
    logger.addHandler(rotating_file_handler)

    return logger
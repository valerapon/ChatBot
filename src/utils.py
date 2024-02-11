import logging


def create_logger(name: str):
    handler = logging.FileHandler(f'logs/{name}')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger

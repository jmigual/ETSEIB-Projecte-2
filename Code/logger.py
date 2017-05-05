import logging


def set_default_logger(file_name="info.log"):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s")
    handler_s = logging.StreamHandler()
    handler_f = logging.FileHandler(file_name)
    handler_s.setFormatter(formatter)
    handler_f.setFormatter(formatter)
    log.addHandler(handler_s)
    log.addHandler(handler_f)


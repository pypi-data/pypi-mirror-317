import logging

sh = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s  - %(levelname)s[line:%(lineno)d] - %(module)s.%(funcName)s: %(message)s")
formatter.datefmt = "%Y-%m-%d %H:%M:%S"
sh.setFormatter(formatter)

logger = logging.getLogger("scan_utils")
logging.getLogger("werkzeug").disabled = True
logging.getLogger("paramiko").disabled = True
logging.getLogger("paramiko.transport").disabled = True
logging.getLogger("paramiko.sftp").disabled = True

logger.setLevel(logging.DEBUG)
logger.addHandler(sh)

def record_log(type, params):
    def wrapper(func):
        def  new_func(*args, **kwargs):
            func(*args, **kwargs)

        return new_func()

    return wrapper()

def new_logger(name, date_format="%Y-%m-%d %H:%M:%S", log_format="%(asctime)s - %(name)s  - %(levelname)s[line:%(lineno)d] - %(module)s.%(funcName)s: %(message)s"):
    sh = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    formatter.datefmt = date_format
    sh.setFormatter(formatter)

    logger = logging.getLogger(name)
    logging.getLogger("werkzeug").disabled = True
    logging.getLogger("paramiko").disabled = True
    logging.getLogger("paramiko.transport").disabled = True
    logging.getLogger("paramiko.sftp").disabled = True

    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    return logger
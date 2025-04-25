import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')
console_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(console_handler)

logger.propagate = False
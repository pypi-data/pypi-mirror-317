import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)


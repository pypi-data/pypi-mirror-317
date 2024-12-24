import logging

from sale_price_house_prediction_model.config.core import PACKAGE_ROOT, config

logging.getLogger(config.app_cnf.package_name).addHandler(logging.NullHandler())
with open(PACKAGE_ROOT / 'VERSION') as version_file:
    __version__ = version_file.read().strip()

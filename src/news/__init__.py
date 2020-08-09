# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from pkg_resources import DistributionNotFound, get_distribution

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "news"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound


logging.basicConfig(filename=f'/home/jay/feelgood_logs/{datetime.date(datetime.now())}.txt', 
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

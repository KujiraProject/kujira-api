#  -*- coding: utf-8 -*-
"""Tasks' scheduler for Kujira"""

import logging
import os
from kujira.scheduler.scheduler import Scheduler
from kujira.scheduler import plugins

LOG_FILE_PATH = '/var/log/kujira/scheduler.log'

# Create directory for logs if not exists
if not os.path.exists(os.path.dirname(LOG_FILE_PATH)):
    os.makedirs(os.path.dirname(LOG_FILE_PATH))

LOG = logging.getLogger(__name__)

LOG_FILE = logging.FileHandler(LOG_FILE_PATH, 'w+')

FORMATTER = logging.Formatter(
    '%(asctime)s %(threadName)s %(name)s: %(message)s')
LOG_FILE.setFormatter(FORMATTER)

LOG.addHandler(LOG_FILE)

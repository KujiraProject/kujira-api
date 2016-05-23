"""
Websocket package

Handles server-client communications: event and graph data
"""
import logging
import os
import errno

LOGGER_FILE_PATH = '/var/log/kujira/websocket.log'

# Create directory if needed
if not os.path.exists(os.path.dirname(LOGGER_FILE_PATH)):
    os.makedirs(os.path.dirname(LOGGER_FILE_PATH))

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

HANDLER = logging.FileHandler(LOGGER_FILE_PATH, 'w')

FORMATTER = logging.Formatter(
    '%(asctime)s %(threadName)-11s %(name)-9s %(message)s')
HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(HANDLER)

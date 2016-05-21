"""
Websocket package

Handles server-client communications
"""
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter(
    '%(asctime)s %(threadName)-11s %(name)-9s %(message)s')
HANDLER = logging.FileHandler('/var/log/websocket.log', 'w')
HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(HANDLER)

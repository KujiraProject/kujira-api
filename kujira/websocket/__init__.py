"""
Websocket package v0.1

notification_thread.py - defines parent class for websocket notifications
event_notification.py - defines class for event oriented notifications
diagram_notification.py - defines class for diagram oriented notifications
room_management.py - creates rooms and manages users in each room
websocket_api.py - defines supported api for WEB client
"""
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter(
    '%(asctime)s %(threadName)-11s %(name)-9s %(message)s')
HANDLER = logging.FileHandler('/var/log/websocket.log', 'w')
HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(HANDLER)

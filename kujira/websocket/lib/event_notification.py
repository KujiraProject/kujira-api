"""
Event notification

Defines class used to periodically send event notifications via websocket.
"""
from kujira.websocket.lib.notification_thread import NotificationThread
from kujira.store.events_queue import RedisQueue
import json


class EventNotificationThread(NotificationThread):
    """Stoppable thread for event notification via websocket"""

    def __init__(self, socket, room_information):
        """
        Initialize object

        :param socket: instance of SocketIO class
        :param room_information: dictionary with room and event names
        """
        NotificationThread.__init__(self, socket, room_information)
        self.redis_handler = RedisQueue()
        self.redis_handler.connect()

    def get_data(self):
        """
        Collect data from Redis, and return message dictionary

        :returns: message dictionary
        """
        data = self.redis_handler.pop()
        return json.loads(data)

    def check_connection(self):
        """
        Check connection to Redis

        :returns: connection status
        """
        return self.redis_handler.is_connected()
        
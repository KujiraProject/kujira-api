"""
Diagram notification

Defines class used to periodically send graph data via websocket.
Temporary implementation.
"""
import time
from kujira.websocket.lib.notification_thread import NotificationThread


class GraphNotificationThread(NotificationThread):
    """Stoppable thread for diagram notification via websocket"""

    def __init__(self, socket, room_information):
        """
        Initialize object

        :param socket: instance of SocketIO class
        :param room_information: dictionary with room and event names
        """
        NotificationThread.__init__(self, socket, room_information)
        # Temporary implementation
        self.count = 0

    def get_data(self):
        """
        Collect data from Redis, and return message dictionary

        :returns: message dictionary
        """
        # Temporary implementation
        time.sleep(2)
        self.count += 1
        data = {"x": self.count, "y": self.count}
        message = {"type": "DATA",
                   "name": self.room_name,
                   "message": "Data chunk",
                   "data": data}
        return message

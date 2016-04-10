"""
Event notification

Defines class used to periodically send event notifications via websocket.
"""

from kujira.websocket.notification_thread import NotificationThread


class EventNotificationThread(NotificationThread):
    """Stoppable thread for event notification via websocket"""

    def __init__(self, socket, room_information):
        """
        Initialize object

        Keyword arguments:
        socket -- instance of SocketIO class
        room_information -- dictionary with room and event names
        """
        NotificationThread.__init__(self, socket, room_information)

    def get_data(self):
        """Collect data from Redis"""
        return {"eventType": "Warning",
                "id": 420,
                "message": "High memory usage."}

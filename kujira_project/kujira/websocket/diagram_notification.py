"""
Diagram notification

Defines class used to periodically send diagram notifications via websocket.
Temporary implementation.
"""

from kujira.websocket.notification_thread import NotificationThread


class DiagramNotificationThread(NotificationThread):
    """Stoppable thread for diagram notification via websocket"""

    def __init__(self, socket, room_information):
        """
        Initialize object

        Keyword arguments:
        socket -- instance of SocketIO class
        room_information -- dictionary with room and event names
        """
        NotificationThread.__init__(self, socket, room_information)
        # Temporary implementation
        self.count = 0

    def get_data(self):
        """Collect data from Graphite"""
        # Temporary implementation
        self.count += 1
        return {"x": self.count, "y": self.count}

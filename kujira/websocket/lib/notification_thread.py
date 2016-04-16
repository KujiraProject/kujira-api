"""
Notification thread

Defines abstract class used to periodically send notifications via websocket.
"""

import time
import threading
from kujira.websocket import LOGGER


class NotificationThread(threading.Thread):
    """Stoppable thread for notification via websocket"""

    def __init__(self, socket, room_information):
        """
        Initialize object

        Keyword arguments:
        socket -- instance of SocketIO class
        room_information -- dictionary with room and event names
        """
        threading.Thread.__init__(self)
        # Stop thread when main kujira stops
        self.daemon = True
        # Start thread paused
        self.paused = True
        self.state = threading.Condition()
        self.socket = socket
        self.room_name = room_information["name"]
        self.event_name = room_information["eventName"]

    def get_data(self):
        """Collect data"""
        pass

    def run(self):
        """Send notifications when data provided"""
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified
            # do stuff
            data = self.get_data()
            if data is not None:
                self.socket.emit(self.event_name, data, room=self.room_name,
                                 namespace='/kujira')
                LOGGER.debug("[" + self.room_name + "] Notification sent.")
            time.sleep(2)

    def resume(self):
        """Reasume thread"""
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        """Pause thread"""
        with self.state:
            self.paused = True  # make self block and wait

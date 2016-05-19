"""
Notification thread

Defines abstract class used to periodically send notifications via websocket.
"""

import time
import threading
from kujira.websocket import LOGGER
from kujira.store.exceptions import ConnectionError


class NotificationThread(threading.Thread):
    """Stoppable thread for notification via websocket"""

    def __init__(self, socket, room_information):
        """
        Initialize object

        :param socket: instance of SocketIO class
        :param room_information: dictionary with room and event names
        """
        threading.Thread.__init__(self)
        # Stop thread when main kujira stops
        self.daemon = True
        # Start thread paused
        self.paused = True
        self.state = threading.Condition()
        self.socket = socket
        self.room_name = room_information["name"]
        self.notification_name = room_information["notificationName"]
        self.event_type = room_information["type"]

    def get_data(self):
        """
        Collect data, and return message dict

        :returns: message dict
        """
        pass

    def check_connection(self):
        """
        Check connection to data source

        :returns: connection status
        """
        pass

    def handle_data_source_exception(self, exception_message):
        """
        Handle data source exception

        :param exception_message: exception message
        """
        LOGGER.debug("[" + self.room_name + "] Exception occurred: " +
                     exception_message)

        while not self.check_connection():
            self.send_message("ERROR", self.room_name,
                              "Data source unreachable")
            LOGGER.debug("[" + self.room_name + "] Data source unreachable.")
            time.sleep(10)

        self.send_message("NOTIFICATION", self.room_name,
                          "Connection restored.")
        LOGGER.debug("[" + self.room_name + "] Connection restored.")

    def send_data(self, data):
        """
        Send data via websocket

        :param data: data retrived from data source
        """
        self.socket.emit(self.notification_name, data, room=self.room_name,
                         namespace='/kujira')

    def run(self):
        """Send notifications when data provided"""
        while True:
            with self.state:
                if self.paused:
                    # block until notified
                    self.state.wait()
            try:
                data = self.get_data()
            except ConnectionError as exception:
                self.handle_data_source_exception(exception.message)

            self.send_data(data)

    def send_message(self, message_type, name, message):
        """
        Send standard message dict without data

        :param message: message_type
        :param message: name
        :param message: message
        """
        message = {"type": message_type,
                   "name": name,
                   "message": message,
                   "data": {}}
        self.socket.emit("MESSAGE", message,
                         room=self.room_name, namespace='/kujira')

    def resume(self):
        """Resume thread"""
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        """Pause thread"""
        with self.state:
            self.paused = True  # make self block and wait

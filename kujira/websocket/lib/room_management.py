"""
Room management

Creates descriptions of available rooms. Manage thread handlers for each room.
Manages users in each room and keeps track of their number.
"""

# Instance of SocketIO class
from kujira import SOCKETIO
from kujira.websocket.lib.event_notification import EventNotificationThread
from kujira.websocket.lib.graph_notification import GraphNotificationThread
from kujira.websocket.exceptions import InvalidRoomNameError
from kujira.websocket import LOGGER

# Description of each room
ROOM_DESCRIPTION = [{"name": "LoggedIn",
                     "notificationName": "event notification",
                     "type": "event"},
                    {"name": "Graph1",
                     "notificationName": "graph notification",
                     "type": "graph"},
                    {"name": "Graph2",
                     "notificationName": "graph notification",
                     "type": "graph"},
                    {"name": "Graph3",
                     "notificationName": "graph notification",
                     "type": "graph"}]

ROOM_HANDLER = {"event": EventNotificationThread,
                "graph": GraphNotificationThread}
# Dictionary for each room thread
ROOM_THREAD = {}
# Dictionary for lists of users in each room
USERS_IN_ROOM = {}

# Initialize dictionaries
for room in ROOM_DESCRIPTION:
    USERS_IN_ROOM[room["name"]] = []
    # Depending on room type start different thread
    ROOM_THREAD[room["name"]] = ROOM_HANDLER[room["type"]](SOCKETIO, room)

# Starts thread for each room.
for room_key in ROOM_THREAD.keys():
    ROOM_THREAD[room_key].start()
    LOGGER.debug("[" + room_key + "] Thread started.")


def add_user_to_room(room_name, user_sid):
    """
    Add user to room and resume thread if requirement meet

    :param room_name: room name
    :param user_sid: user SID
    """
    if room_name not in USERS_IN_ROOM:
        raise InvalidRoomNameError()
    # Check if user is already in room
    if user_sid not in USERS_IN_ROOM[room_name]:
        USERS_IN_ROOM[room_name].append(user_sid)
        LOGGER.debug(
            "[" + room_name + "] User joined the room. User SID: " + user_sid)
        send_broadcast_message("NOTIFICATION", "User status",
                               "User joined room", {"SID":user_sid})
        # First user that joins room resumes thread
        if len(USERS_IN_ROOM[room_name]) == 1:
            ROOM_THREAD[room_name].resume()
            LOGGER.debug("[" + room_name + "] Thread resumed.")

def remove_user_from_room(room_name, user_sid):
    """
    Remove user from room and pause thread if requirement meet

    :param room_name: room name
    :param user_sid: user SID
    """
    if room_name not in USERS_IN_ROOM:
        raise InvalidRoomNameError()
    # Check if user is in room
    if user_sid in USERS_IN_ROOM[room_name]:
        USERS_IN_ROOM[room_name].remove(user_sid)
        LOGGER.debug(
            "[" + room_name + "] User left the room. User SID: " + user_sid)
        send_broadcast_message("NOTIFICATION", "User status", "User left room",
                               {"SID":user_sid})
        # Last user that leaves room pauses thread
        if len(USERS_IN_ROOM[room_name]) == 0:
            ROOM_THREAD[room_name].pause()
            LOGGER.debug("[" + room_name + "] Thread paused.")


def remove_user(user_sid):
    """
    Remove user from each room

    :param user_sid: user SID
    """
    # Iterate through each room
    for room_name in USERS_IN_ROOM.keys():
        remove_user_from_room(room_name, user_sid)

def send_broadcast_message(message_type, name, message, data):
    """
    Send broadcast message to connected users.
    SocketIO event: "MESSAGE"
    namespace: /kujira
    broadcast: True

    :param message_type: message_type
    :param name: name
    :param message: message
    :param data: data
    """
    message = {"type": message_type,
               "name": name,
               "message": message,
               "data": data}
    SOCKETIO.emit("MESSAGE", message,
                  broadcast=True, namespace='/kujira')
                         
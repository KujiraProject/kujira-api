"""
Room management

Creates descriptions of available rooms. Manage thread handlers for each room.
Manages users in each room and keeps track of their number.
"""

# Instance of SocketIO class
from kujira import SOCKETIO
from kujira.websocket.lib.event_notification import EventNotificationThread
from kujira.websocket.lib.diagram_notification import DiagramNotificationThread
from kujira.websocket import LOGGER

# Description of each room
ROOM_DESCRIPTION = [{"name": "LoggedIn",
                     "eventName": "event notification",
                     "type": "event"},
                    {"name": "Diagram1",
                     "eventName": "diagram 1 notification",
                     "type": "diagram"}]

# Dictionary for each room thread
ROOM_THREAD = {}
# Dictionary for lists of users in each room
USERS_IN_ROOM = {}

# Initialize dictionaries
for room in ROOM_DESCRIPTION:
    USERS_IN_ROOM[room["name"]] = []
    # Depending on room type start different thread
    if room["type"] is "event":
        ROOM_THREAD[room["name"]] = EventNotificationThread(SOCKETIO, room)
    elif room["type"] is "diagram":
        ROOM_THREAD[room["name"]] = DiagramNotificationThread(SOCKETIO, room)

# Starts thread for each room.
for room_key in ROOM_THREAD.keys():
    ROOM_THREAD[room_key].start()
    LOGGER.debug("[" + room_key + "] Thread started.")


def add_user_to_room(room_name, user_sid):
    """Add user to room and resume thread if requirement meet"""
    # Check if room_name is correct and if user isn't already inside
    if room_name in USERS_IN_ROOM and user_sid not in USERS_IN_ROOM[room_name]:
        USERS_IN_ROOM[room_name].append(user_sid)
        LOGGER.debug(
            "[" + room_name + "] User joined the room. User SID: " + user_sid)
        # First user that joins room resumes thread
        if len(USERS_IN_ROOM[room_name]) == 1:
            ROOM_THREAD[room_name].resume()
            LOGGER.debug("[" + room_name + "] Thread resumed.")


def remove_user_from_room(room_name, user_sid):
    """Remove user from room and pause thread if requirement meet"""
    # Check if room_name is correct and if user is inside
    if room_name in USERS_IN_ROOM and user_sid in USERS_IN_ROOM[room_name]:
        USERS_IN_ROOM[room_name].remove(user_sid)
        LOGGER.debug(
            "[" + room_name + "] User left the room. User SID: " + user_sid)
        # Last user that leaves room pauses thread
        if len(USERS_IN_ROOM[room_name]) == 0:
            ROOM_THREAD[room_name].pause()
            LOGGER.debug("[" + room_name + "] Thread paused.")


def remove_user(user_sid):
    """Remove user from each room and pause thread if requirement meet"""
    # Iterate through each room
    for room_name in USERS_IN_ROOM.keys():
        # Check if user inside room
        if user_sid in USERS_IN_ROOM[room_name]:
            USERS_IN_ROOM[room_name].remove(user_sid)
            LOGGER.debug(
                "[" + room_name + "] User left the room. User SID: " + user_sid)
            # Last user that leaves room pauses thread
            if len(USERS_IN_ROOM[room_name]) == 0:
                ROOM_THREAD[room_name].pause()
                LOGGER.debug("[" + room_name + "] Thread paused.")

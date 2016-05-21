"""
Websocket API

Defines interface for WEB clients to communicate via websocket

This module MUST be imported where SocketIO.run(app) (or SocketIO()) is used or
server won't receive any WEB client messages.
"""
from flask import request
from flask_socketio import join_room, leave_room, disconnect
from kujira.websocket.lib.room_management import add_user_to_room, \
    remove_user_from_room, remove_user
from kujira.websocket.exceptions import InvalidRoomNameError
from kujira import SOCKETIO


@SOCKETIO.on('join', namespace='/kujira')
def join(message):
    """
    Join desired room for further communication

    :param message: Contains room name
    """
    try:
        add_user_to_room(message['room'], request.sid)
        join_room(message['room'])
        send_message("NOTIFICATION", "Room status", "Room joined.",
                     {"room":message['room']})
    except InvalidRoomNameError:
        send_message("ERROR", "Room status", "Invalid room name.",
                     {"room":message['room']})


@SOCKETIO.on('leave', namespace='/kujira')
def leave(message):
    """
    Leave desired room to stop further communication

    :param message: Contains room name
    """
    try:
        remove_user_from_room(message['room'], request.sid)
        leave_room(message['room'])
        send_message("NOTIFICATION", "Room status", "Room joined.",
                     {"room":message['room']})
    except InvalidRoomNameError:
        send_message("ERROR", "Room status", "Invalid room name.",
                     {"room":message['room']})


@SOCKETIO.on('disconnect request', namespace='/kujira')
def disconnect_request():
    """Disconnect websocket"""
    disconnect()


@SOCKETIO.on('disconnect', namespace='/kujira')
def on_disconnect():
    """Leave all rooms"""
    remove_user(request.sid)

def send_message(message_type, name, message, data):
    """
    Send message to connected user.
    SocketIO event: "MESSAGE"
    namespace: /kujira

    :param message_type: Type of the message
    :param name: Name of the message
    :param message: Content of the message
    :param data: Additional data
    """
    message = {"type": message_type,
               "name": name,
               "message": message,
               "data": data}
    SOCKETIO.emit("MESSAGE", message, namespace='/kujira')

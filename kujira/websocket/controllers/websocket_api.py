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
# Instance of SocketIO class
from kujira import SOCKETIO


@SOCKETIO.on('join', namespace='/kujira')
def join(message):
    """Join desired room for further communication"""
    join_room(message['room'])
    add_user_to_room(message['room'], request.sid)


@SOCKETIO.on('leave', namespace='/kujira')
def leave(message):
    """Leave desired room to stop further communication"""
    leave_room(message['room'])
    remove_user_from_room(message['room'], request.sid)


@SOCKETIO.on('disconnect request', namespace='/kujira')
def disconnect_request():
    """Disconnect websocket"""
    disconnect()


@SOCKETIO.on('connect', namespace='/kujira')
def on_connect():
    """No implementation"""
    pass


@SOCKETIO.on('disconnect', namespace='/kujira')
def on_disconnect():
    """Leave all rooms"""
    remove_user(request.sid)


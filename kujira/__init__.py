""" Kujira API is flask/websocket app for serving Ceph cluster data """

from flask import Flask
from flask_socketio import SocketIO

import eventlet
eventlet.monkey_patch()

SOCKETIO = SocketIO()


def create_app():
    """Create an application."""
    app = Flask(__name__)
    app.config.from_object('config')

    SOCKETIO.init_app(app, engineio_logger=True, async_mode='eventlet')

    return app

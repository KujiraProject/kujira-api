'''from flask import Flask
from flask_socketio import SocketIO

import eventlet
eventlet.monkey_patch()

SOCKETIO = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config.from_object('config')

    SOCKETIO.init_app(app, engineio_logger=True, async_mode='eventlet')

    return app'''

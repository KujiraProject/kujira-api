""" Kujira API is flask/websocket app for serving Ceph cluster data """

import eventlet
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from kujira.blueprints import AUTH_BP, SERVER_BP, OSD_BP, POOL_BP, MON_BP, CLUSTER_BP
from kujira.rest.controllers import osds, pools, servers, clusters, mons
import kujira.auth

eventlet.monkey_patch()

SOCKETIO = SocketIO()

def create_app():
    """Create an application."""
    app = Flask(__name__)

    app.register_blueprint(AUTH_BP)
    app.register_blueprint(OSD_BP)
    app.register_blueprint(SERVER_BP)
    app.register_blueprint(POOL_BP)
    app.register_blueprint(MON_BP)
    app.register_blueprint(CLUSTER_BP)

    app.config.from_object('config')

    SOCKETIO.init_app(app, engineio_logger=True, async_mode='eventlet')
    CORS(app)

    return app

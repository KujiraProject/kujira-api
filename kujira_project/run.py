from kujira import create_app, SOCKETIO
# Must import websocket_api or won't receive websocket messages
import kujira.websocket.websocket_api

APP = create_app(debug=True)

if __name__ == '__main__':
    SOCKETIO.run(APP)

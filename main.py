from app import app, socketio
from listeners.server import *

if __name__ == '__main__':
    # app.debug = True
    socketio.run(app, host="0.0.0.0")

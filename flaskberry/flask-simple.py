import os
from flask import Flask
from flask_socketio import SocketIO

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev'
)

websocketio = SocketIO(app, async_mode=async_mode ,cors_allowed_origins="*")

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

import sysinfo
app.register_blueprint(sysinfo.bp)

import api
app.register_blueprint(api.bp)

import charts
app.register_blueprint(charts.bp)

import Eweb_sockets
app.register_blueprint(Eweb_sockets.bp)


if __name__ == "__main__":    
    websocketio.run(app, host='0.0.0.0', port=5000, debug=True)

import psutil
from . import socket_client

from flask import (
    Blueprint, jsonify
)

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/cpu_usage')
def cpu_usage():
    return jsonify({'cpu':cpu_usage_info()})

@bp.route('/imu_data')
def imu_data():
    return jsonify({'data':socket_client.getData()}) #get json data
    
def cpu_usage_info():
    return str(psutil.cpu_percent())
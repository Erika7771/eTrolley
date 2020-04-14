import psutil
import numpy as np
import socket_client

from flask import (
    Blueprint, jsonify
)

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/cpu_usage')
def cpu_usage():
    return jsonify({'cpu':cpu_usage_info()})

@bp.route('/imu_data')
def imu_data():
    data = socket_client.getData()
    return jsonify({'acc_data':data['buff_acc'],'ang_data':data['buff_vel']}) #get json data
    
def cpu_usage_info():
    return str(psutil.cpu_percent())
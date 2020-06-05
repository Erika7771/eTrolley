#---------------------------------------------------------------------
#Blueprint example. Show the cpu usage info on the url /api/cpu_usage
#---------------------------------------------------------------------
import psutil
import numpy as np

from flask import (
    Blueprint, jsonify
)

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/cpu_usage')
def cpu_usage():
    return jsonify({'cpu':cpu_usage_info()})
    
def cpu_usage_info():
    return str(psutil.cpu_percent())
#---------------------------------------------------------------------
# Blueprint to render the charts page
#---------------------------------------------------------------------

from flask import (
    Blueprint, jsonify, Flask, render_template
)

bp = Blueprint('charts', __name__, url_prefix='/charts')

@bp.route('/')
def sensors_charts():
    return render_template("charts.html")
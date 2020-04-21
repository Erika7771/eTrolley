import os
import glob
from zipfile import ZipFile
from flask import Flask
from flask_socketio import SocketIO
from flask import request, send_file, abort
import pathlib


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

import web_sockets
app.register_blueprint(web_sockets.bp)

def get_latestRecord(sensor):
    folder = f'./raspweb/flaskberry/static/recordings/{sensor}/'
    list_of_files = glob.glob(f'{folder}*.csv')
    if len(list_of_files)<1:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def get_recordsZip(sensors):
    
    filesToZip = []
    
    for sensor in sensors:
        latestFile = get_latestRecord(sensor)
        if latestFile:
            filesToZip.append(latestFile)
            
    if len(filesToZip) == 1:
        fileName   = os.path.basename(filesToZip[0])
        folderName = os.path.basename(os.path.dirname(filesToZip[0]))
        return "static/recordings/"+folderName+"/"+fileName
    
    # Create a ZipFile Object
    zipFile = 'static/recordings/last.zip'
    zipObj = ZipFile('./raspweb/flaskberry/'+zipFile, 'w')
    
    for file in filesToZip:
       zipObj.write(file,os.path.basename(file))
       
    zipObj.close()
    
    return zipFile 
    

@app.route('/recordings/last_recording')
def serve_records():
   
    if request.args.get('data'):
       sensors = request.args.get('data').split(";")
    else:
        return abort(404)
    
    filename = get_recordsZip(sensors)
    
    return send_file(filename,
                     cache_timeout = 1,
                     as_attachment=True,
                     attachment_filename=os.path.basename(filename))



if __name__ == "__main__":    
    websocketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)

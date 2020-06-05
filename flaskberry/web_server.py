#---------------------------------------------------------------------
# Create the Flask server  
#---------------------------------------------------------------------
import os
import glob
from zipfile import ZipFile
from flask import Flask
from flask_socketio import SocketIO
from flask import request, send_file, abort
from pathlib import Path
import eventlet

#Async mode must be 'eventlet' to make mqtt work
eventlet.monkey_patch()
async_mode = 'eventlet'

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev'
)

# Add socketio to the existing Flask application to enable WebSockets
websocketio = SocketIO(app, async_mode=async_mode ,cors_allowed_origins="*")

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Register the blueprints
import sysinfo
app.register_blueprint(sysinfo.bp)

import api
app.register_blueprint(api.bp)

import charts
app.register_blueprint(charts.bp)

import web_sockets
app.register_blueprint(web_sockets.bp)


my_path = Path(__file__).resolve().parents[0] #/home/pi/raspweb/flaskberry

# Return the latest (and only) record the sensor
def get_latestRecord(sensor):
    folder = f"{my_path}/static/recordings/{sensor}/"
    list_of_files = glob.glob(f"{folder}*.csv")
    if len(list_of_files)<1:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

#Create a zip file with the last records of the sensors
def get_recordsZip(sensors):
    
    filesToZip = []
    
    for sensor in sensors:
        latestFile = get_latestRecord(sensor)
        if latestFile:
            filesToZip.append(latestFile)
    
    # If only one sensor has been recorded, return it without create the zip
    if len(filesToZip) == 1:
        fileName   = os.path.basename(filesToZip[0])
        folderName = os.path.basename(os.path.dirname(filesToZip[0]))
        return "static/recordings/"+folderName+"/"+fileName
    
    # Create a ZipFile Object
    zipFile = "static/recordings/last.zip"
    zipObj = ZipFile(f"{my_path}/"+zipFile, 'w')
    
    for file in filesToZip:
       zipObj.write(file,os.path.basename(file))
       
    zipObj.close()
    return zipFile 
    
#Handle download zip request. This function fires when the user tries to
#download the zip file. 
@app.route('/recordings/last_recording')
def serve_records():
    
    if request.args.get('data'):
       sensors = request.args.get('data').split(";")
    else:
        return abort(404)
    
    #zip selected sensors and return them to the page
    filename = get_recordsZip(sensors)
    return send_file(filename,
                     cache_timeout = 1,
                     as_attachment=True,
                     attachment_filename=os.path.basename(filename))

#Handle download unifile request. This function fires when the user tries to
#download the single csv file. 
@app.route('/recordings/unifile')
def serve_unifile():    
    
    #Find the file and return it to the page.
    list_of_files = glob.glob(f"{my_path}/static/recordings/*.csv")
    
    if len(list_of_files) < 1:
        return abort(404)
        
    if len(list_of_files) > 1:
        return abort(404)

    unifile = list_of_files[0]
     
    return send_file(unifile,
                     cache_timeout = 1,
                     as_attachment=True,
                     attachment_filename=os.path.basename(unifile))

# Start Flask application on port 5000. 
if __name__ == "__main__":    
    websocketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# eTrolley
Semester Project @react lab, EPFL


To start everything create a file .sh with the following commands:

pkill python  
i2cdetect -y 1  
source /home/pi/raspweb/.venv/bin/activate    
python3 /home/pi/raspweb/local/local_server.py &    
python3 /home/pi/raspweb/flaskberry/web_server.py    

#### Main files:
raspweb/local/  
&emsp; local_server.py: &emsp;&emsp;  Start the local server and stream the sensors data over local sockets.
  
raspweb/flaskberry/  
&emsp; web_server.py : &emsp;&emsp; Start the Flask server.  
&emsp; web_sockets.py: &emsp;&emsp;Connect as client to the local server and manage websockets.  
&emsp; templates/  
&emsp;&emsp;&emsp; charts.html:&emsp;&emsp; Chart page html static structure.  
&emsp; static/  
&emsp;&emsp; dist/js/pages/  
&emsp;&emsp;&emsp; chartsConfig.js:&ensp;Listen over webosckets and update ghraps content when new data are available.  
&emsp;&emsp; recordings/: &emsp;&emsp;&ensp; Store all recordings.

raspweb/extra/  
&emsp; getData.py:  &emsp;&emsp; &emsp;&ensp;Connect directly to local server without passing through the Flask server.


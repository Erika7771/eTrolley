# eTrolley
Semester Project at REACT lab, EPFL

## Project structure:
Note: Only the main files are represented.
```
	/home/pi/raspweb/
	├── flaskberry/
	│     ├── web_server.py               
	│     ├── blueprints
	│     ├── static/
	│     │     ├── dist/
	│     │     │     ├── css/
	│     │     │     └── js/
	│     │     │          └──pages/
	│     │     │               └── chartsConfig.js
	│     │     └── recordings/
	│     │           ├── sensor_folder/
	│     │           │    └── sensor_record.csv
	│     │           ├── single_file.csv
	│     │           └── last.zip	
	│     └── templates/
	│           ├── EtestSocket.html
	│           └── charts.html
	├── local/
	│     ├── sensors scripts
	│     └── mqtt_SensorsClient.py       
	├── extra/
	│     └──getData.py
	├── .venv/
	├── MANIFEST.in
	├── requirements.txt
	├── requirementsLocal.txt
	└── setup.py	

```

|Module| Function |
|--|--|
| mqtt_sensorsClient.py  |  Start the MQTT client and publish the sensors data on different topics.  |
|web_server.py| Start the Flask server.|
|web_sockets.py|Connect as a client to the Mosquitto broker and manage WebSockets.|
|charts.html|Chart page HTML static structure.|
|chartsConfig.js| Listen over WebSockets and update graphs content when new data is available.|
|recordings/|Store all the recordings.|
|getData&#46;py |Connect directly to the Mosquitto Broker without going through the Flask server.|


## Installation:
 The first installation requires an internet connection, possibly via ethernet cable since 
 the WiFi module will be used to create another network. 
### 1. Operating system
Install the last operating system (Raspberry Pi OS with Desktop image)  on a Micro SD.

### 2. Interfaces 
 ####  I2C 
 
 Install the following packages:  
 <pre><code> sudo apt-get install -y python-smbus
 sudo apt-get install -y i2c-tools</code></pre>
 
Open:
<pre><code>sudo raspi-config </code></pre>
and go to : interface options -> enable I2C

Reboot, then test the connection:
<pre><code>sudo i2cdetect -y 1</code></pre>
This should show the I2C address in use (0x68)

#### SPI/CAN
Open:
<pre><code>sudo nano /boot/config.txt</code></pre>

and uncomment the line:
<pre><code>dtparam=spi=on</code></pre>

Add the following line after the previous one:
<pre><code>dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=24</code></pre>

Reboot and check that  SPI and CAN modules were started: 
<pre><code>dmesg | grep -i spi
dmesg | grep -i can</code></pre>

Install the utils to receive and send data:
<pre><code>sudo apt-get install can-utils</code></pre>

Add to `/etc/network/interface` the following lines to automatically start the CAN interface at boot. The bitrate must match the Arduino/motors speed:
<pre><code>auto can0
iface can0 inet manual
        pre-up /sbin/ip link set $IFACE type can bitrate 250000
        up /sbin/ifconfig $IFACE up
        down /sbin/ifconfig $IFACE down
</code></pre>

Listen to all the incoming messages to check if everything works:
<pre><code>candump any</code></pre>

### 3. Wireless access point
Follow the official guide to set up the Network: [https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md](https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md).

### 4. Mosquitto Broker
Follow this guide to install the Mosquitto Broker: https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/

### 5. Brick Daemon
The Brick Daemon is necessary to connect the TinkerForge IMU. It can be downloaded from here: [https://www.tinkerforge.com/en/doc/Software/Brickd.html](https://www.tinkerforge.com/en/doc/Software/Brickd.html)

### 5. Virtual environment
Create a virtual environment  `.venv`in `/home/pi/raspweb` and activate it:

    mkdir raspweb
    python3 -m venv /home/pi/raspweb/.venv
    source path/.venv/bin/activate
Install all the requirements:

    pip install -r requirements.txt
    pip install -r requirementsLocal.txt

Finally, install the Flask application:

   `pip install -e .`

### 6. Bash script
This step is optional, it creates a script to automatically run the commands sequence required to start the MQTT client and the Flask server.
In `/home/pi/`create a  new file `startFlaskberry.sh `with the following content:

    pkill python
    source /home/pi/raspweb/.venv/bin/activate
    python3 /home/pi/raspweb/local/mqtt_sensorsClient.py &
    python3 /home/pi/raspweb/flaskberry/web_server.py

Note:  If the Razor IMU does not start,  try to add `i2cdetect -y 1` right after `pkill python`.  



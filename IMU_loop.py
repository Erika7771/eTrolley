#!/usr/bin/env python3

""" IMU 1.2 """

HOST = "localhost"
PORT = 4223
UID = "5VHux5" # Unique ID of IMU Brick

import os
import json
import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu import BrickIMU

path = "../Flask/static/dist/js/pages"
file_j = "readings.json"

ipcon = IPConnection() # Create IP connection object
imu = BrickIMU(UID, ipcon) # Create device object
ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected 
while True:
    time.sleep(0.1)
    [x,y,z] = imu.get_acceleration()
    a = [x,y,z]
    [ax,ay,az] = imu.get_angular_velocity()
    v = [ax,ay,az]
    a.extend(v)
    data = {'Ax':x, 'Ay':y, 'Az':z, 'Vx':ax, 'Vy':ay, 'Vz':z} 
    #log data with json
    with open(os.path.join(path,file_j), 'a') as f:
        json.dump(data,f)
    print(a)
    
ipcon.disconnect()  

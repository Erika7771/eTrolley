""" SparkFun Razor 9 Dof"""

from FaBo9AXISMPU9250Python import FaBo9Axis_MPU9250 
from datetime import datetime
import threading, time
import sys
import numpy as np
import json
import writeToCSV as CSV

class Reading:    
    def __init__(self):
        self.buff_acc = []
        self.buff_vel = [] 
    
    def clear(self):
        self.buff_acc.clear()
        self.buff_vel.clear()
        
r = Reading()
Razor_IMU = None
csvfile_acc = None
csvfile_vel = None

def read():
  global csvfile_acc
  global Razor_IMU
  
  while True: # ~2ms per loop       
      
    if len(r.buff_vel) > 50 or len(r.buff_acc) > 50:
        r.clear()
    data_acc = Razor_IMU.readAccel()       
    data_vel = Razor_IMU.readGyro()
    r.buff_acc.append(list(data_acc.values()))
    r.buff_vel.append(list(data_vel.values()))
    
    if csvfile_acc:
        CSV.write_file(csvfile_acc, 'Razor_acc', data_acc.values())
    if csvfile_vel:
        CSV.write_file(csvfile_vel, 'Razor_vel', data_vel.values())  
    
    time.sleep(0.01)     

def init():
    global Razor_IMU
    Razor_IMU = FaBo9Axis_MPU9250.MPU9250()
    print("Hey, Razor connected!")
    # Start background process 
    t_read = threading.Thread(target=read)
    # t_read.daemon = True
    t_read.start()



      
def get_buffers():
    return r



def record(sensor):
    global csvfile_acc
    global csvfile_vel
    
    if sensor == 'Razor_acc':
        csvfile_acc = CSV.create_file(sensor)
    elif  sensor == 'Razor_vel':
        csvfile_vel = CSV.create_file(sensor)
        
def record_stop(sensors):
    global csvfile_acc
    global csvfile_vel
    
    if sensors == 'Razor_acc':
        csvfile_acc = None
    elif  sensors == 'Razor_vel':
        csvfile_vel = None

if __name__ == "__main__":
    while True:
        time.sleep(1)        
        val = get_buffers()
        print(json.dumps(val.__dict__))
        

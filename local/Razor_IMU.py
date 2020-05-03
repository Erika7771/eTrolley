""" SparkFun Razor 9 Dof"""

import FaBo9Axis_MPU9250 
import threading, time
from utils import Reading_IMU

r = Reading_IMU()
Razor_IMU = None

def read():
  global Razor_IMU
  
  while True: # ~2ms per loop       
      
    if len(r.buff_vel) > 50 or len(r.buff_acc) > 50:
        r.clear()
    data_acc = Razor_IMU.readAccel()       
    data_vel = Razor_IMU.readGyro()
    r.buff_acc.append(list(data_acc.values()))
    r.buff_vel.append(list(data_vel.values()))
    if r.data_queue_acc:
        r.data_queue_acc.put(list(data_acc.values()))
    if r.data_queue_vel:
        r.data_queue_vel.put(list(data_vel.values()))
    
    time.sleep(0.003)     

def init():
    global Razor_IMU
    Razor_IMU = FaBo9Axis_MPU9250.MPU9250()
    print("Hey, Razor connected!")
    # Start background process 
    t_read = threading.Thread(target=read)
    t_read.start()

      
def get_buffers():
    return r.getBuffers()

def emptyBuffes():
    r.clear()

def record(sensor):
        dataType = 'acc' if sensor=='Razor_acc' else  'vel'
        r.record(sensorName=sensor, dataType=dataType)
    
def record_stop(sensor):
     dataType = 'acc' if sensor=='Razor_acc' else  'vel'
     r.record_stop(dataType=dataType)

if __name__ == "__main__":
    while True:
        time.sleep(1)       
        

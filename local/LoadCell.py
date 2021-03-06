from hx711 import HX711
import RPi.GPIO as GPIO
import logging
import time
import threading
import statistics
import numpy as np
from utils import Reading_LC

# NB: A wire of the load cell broke before implementing the MQTT protocol,
# so I couldn't check if this module still works properly. It should not
# pose problems though, the format of the data hasn't changed.

GPIO.setwarnings(False)
# logging.basicConfig(level=logging.DEBUG)

#Set VDD pin to 3.3V 
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, True)

lc = Reading_LC()
hx711 = None
csvfile = None


def read():
    global csvfile
    global hx711
    
    # Before starting saving the data, compute and remove the offset of the measurements. 
    offset = 0
    values = hx711.get_raw_data(times=5) 
    offset = statistics.mean(values)
    while True:
       if len(lc.data) > 50:
            lc.clear()
        measure = hx711.get_raw_data(times=2) #Take two measurement at a time 
        ms1 = (measure[0]-offset)
        ms2 = (measure[1]-offset)
        extendedArray = np.linspace(ms1, ms2, 20) # Add values between the readings for representation purposes 
        lc.extend(np.reshape(extendedArray, (20,1)).tolist())
        if lc.data_queue: #if recording, put the values in a queue 
            lc.data_queue.put(ms1)
            lc.data_queue.put(ms2)       
        time.sleep(0.08) 

# initialize the Load Cell and start the background thread that reads the sensor.
def init():
    global hx711
    hx711 = HX711(dout_pin=5, pd_sck_pin=6, channel='A', gain=128)
    hx711.reset() 
    print("Hey, Load Cell connected!")
    t_read = threading.Thread(target=read)
    t_read.start()

def get_buffer():
    return lc.getBuffer()

def emptyBuffer():
    lc.clear()

def record():
    lc.record(sensorName = 'Load_Cell')
    
def record_stop():
     lc.record_stop()
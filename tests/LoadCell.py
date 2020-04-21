#!/usr/bin/python3
from hx711 import HX711
import RPi.GPIO as GPIO
import logging
import time
import threading
import json
import statistics
import writeToCSV as CSV

GPIO.setwarnings(False)
# logging.basicConfig(level=logging.DEBUG)

#Set VDD pin to 3.3V 
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, True)

hx711 = None
data = []
offset = 0
csvfile = None

def read():
    global csvfile
    global hx711
    
    values = hx711.get_raw_data(times=5)
    offset = statistics.mean(values)
    while True:
        if len(data) > 50:
            data.clear()
        measure = hx711.get_raw_data(times=2)
        ms1 = round(measure[0]-offset,2)
        ms2 = round(measure[1]-offset,2)
        data.append([measure[0]-offset])
        data.append([measure[1]-offset])
        if csvfile:
            CSV.write_file(csvfile, 'Load_Cell', [[ms1], [ms2]])        
        time.sleep(0.08) 

def init():
    global hx711
    hx711 = HX711(dout_pin=5, pd_sck_pin=6, channel='A', gain=128)
    hx711.reset() 
    print("Hey, Load Cell connected!")
    t_read = threading.Thread(target=read)
    # t_read.daemon = True
    t_read.start()

def get_buffer():
    return  data

def record():
    global csvfile    
    csvfile = CSV.create_file('Load_Cell')
        
def record_stop():
    global csvfile
    csvfile = None

if __name__ == "__main__":
    while True:
        time.sleep(1)        
        raw_data = json.dumps(get_buffer().__dict__)
        print(type(raw_data))

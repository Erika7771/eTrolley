import logging
import time
import threading
import json
import statistics
import writeToCSV as CSV
import numpy as np
import random
from utils import Reading_LC

lc = Reading_LC()

def read():
    while True:
        if len(lc.data) > 50:
            lc.clear()
        measure = [[random.randint(-10000, 10000)] for i in range(2)]
        ms1 = (measure[0])
        ms2 = (measure[1])
        lista = np.linspace(ms1, ms2, 20)
        lc.data.extend(np.reshape(lista, (20,1)).tolist())        
        if lc.data_queue:
            lc.data_queue.put(ms1)
            lc.data_queue.put(ms2)
        time.sleep(0.08) 

def init():
    print("Hey, simulated Load Cell connected!")
    t_read = threading.Thread(target=read)
    t_read.start()

def get_buffer():
    return lc.getBuffer()

def emptyBuffer():
    lc.clear()

def record():
    lc.record(sensorName = "Load_Cell")
    
def record_stop():
     lc.record_stop()

if __name__ == "__main__":
    init()
    while True:
        time.sleep(1)        
        raw_data = get_buffer()
        print(raw_data)


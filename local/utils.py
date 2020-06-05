#----------------------------------------------------------------------------------
# Contain the classes of the sensors
#----------------------------------------------------------------------------------

import multiprocessing
import writeToCSV as CSV

class Reading_IMU:
    
    STOP_TOKEN = "Stop"
    
    def __init__(self):
        self.buff_acc = []
        self.buff_vel = []
        self.csvfile_acc = None
        self.csvfile_vel = None
        self.data_queue_acc = None
        self.data_queue_vel = None
        self.writer_process_acc = None
        self.writer_process_vel = None
    
    def clear(self):
        self.buff_acc.clear()
        self.buff_vel.clear()
        
    def getBuffers(self):
        return {"buff_acc":self.buff_acc, "buff_vel": self.buff_vel}
  
    def record(self,dataType,sensorName):    
        if dataType == 'acc':
            self.data_queue_acc = multiprocessing.Queue() #Initialize the queue used by the writing process 
            self.csvfile_acc = CSV.create_file(sensorName) # Create a new CSV file
            # Configure and start the writing process
            self.writer_process_acc = multiprocessing.Process(target = CSV.write_file, args=(self.csvfile_acc, sensorName, self.data_queue_acc, Reading_IMU.STOP_TOKEN))
            self.writer_process_acc.start()    
        elif  dataType == 'vel':
            self.data_queue_vel = multiprocessing.Queue()
            self.csvfile_vel = CSV.create_file(sensorName)
            self.writer_process_vel = multiprocessing.Process(target = CSV.write_file, args=(self.csvfile_vel, sensorName, self.data_queue_vel, Reading_IMU.STOP_TOKEN))
            self.writer_process_vel.start()
            
    #Stop the writing process by putting a token in the queue and reinitialize the csv and queue objects.
    def record_stop(self, dataType):    
        if dataType == 'acc':
            self.csvfile_acc = None
            self.data_queue_acc.put(Reading_IMU.STOP_TOKEN) 
            self.writer_process_acc.join()
            self.data_queue_acc = None
        elif dataType == 'vel':
            self.csvfile_vel = None            
            self.data_queue_vel.put(Reading_IMU.STOP_TOKEN)
            self.writer_process_vel.join()
            self.data_queue_vel = None

class Reading_LC:
    
    STOP_TOKEN = "Stop"
    
    def __init__(self):
        self.data = []
        self.csvfile = None
        self.data_queue = None
        self.writer_process = None
        
    def clear(self):
        self.data.clear()
        
    def getBuffer(self):        
        return {"data":self.data}
  
    def record(self,sensorName):    
            self.data_queue = multiprocessing.Queue()
            self.csvfile = CSV.create_file(sensorName)
            self.writer_process = multiprocessing.Process(target = CSV.write_file, args=(self.csvfile, sensorName, self.data_queue, Reading_LC.STOP_TOKEN))
            self.writer_process.start()   

    def record_stop(self):  
            self.csvfile = None
            self.data_queue.put(Reading_LC.STOP_TOKEN)
            self.writer_process.join()
            self.data_queue = None

class Reading_CAN(Reading_LC):

    def __init__(self):
        super().__init__()
        self.bus = None
    
    
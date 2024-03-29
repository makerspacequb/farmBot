#NAME: farmbot.py
#DATE: 12/06/2019
#AUTH: Ryan McCartney
#DESC: A python class for moving the farmbot with intuative methods
#COPY: Copyright 2019, All Rights Reserved, Ryan McCartney

import threading
import time
import requests
from requests import Session

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper
    
class Farmbot:

    debug = False
    logFilePath = "control/log.txt"

    def __init__(self,ipAddress):

        self.logging = True
        self.baseURL = "http://"+ipAddress+":8080/"
        self.connected = True
        self.error = False

        #Start capturing status packets
        self.getStatus()

    #Logging Function
    def log(self, entry):
        
        currentDateTime = time.strftime("%d/%m/%Y %H:%M:%S")
        logEntry = currentDateTime + ": " + entry

        if self.logging == True:
            #open a txt file to use for logging
            logFile = open(self.logFilePath,"a+")
            logFile.write(logEntry+"\n")
            logFile.close()

        print(logEntry)
    
    #Send and Receive Messages with implemented logging
    def sendCommand(self, command):

        #Start Timing
        start = time.time()

        #combine with host address
        message = self.baseURL + "send?command=" + command
    
        try:
            response = requests.post(message,timeout=1)
            status = response.content.decode("utf-8").split("\n")

            if self.debug == True:
                self.log("INFO = Transmission response code is "+str(response.status_code))
                end = time.time()
                print("STATUS: Sending '",command,"' took %.2f seconds." % round((end-start),2))
                self.log(status)
            self.connected = True

        except:
            self.log("ERROR = Could not access API")
            self.connected = False

    @threaded
    def getStatus(self):
        
        delay = 0.25 #Seconds
        while self.connected:

            try:
                message = self.baseURL + "getLine"
                response = requests.post(message,timeout=1)
            
                status = response.content.decode("utf-8").split("\n")
                self.log("INFO: " + status)
            except:
                self.log("ERROR: No status response. No Connection.")
                self.connected = False
        
            time.sleep(delay)

    def lightOn(self):
        self.sendCommand("l1")
        self.log("INFO: Lights turned on")

    def lightOff(self):
        self.sendCommand("l0")
        self.log("INFO: Lights turned off")

    def waterOn(self):
        self.sendCommand("w1")
        self.log("INFO: Water turned on")
    
    def waterOff(self):
        self.sendCommand("w0")
        self.log("INFO: Water turned off")

    def vacuumOn(self):
        self.sendCommand("v1")
        self.log("INFO: Water turned on")
    
    def vacuumOff(self):
        self.sendCommand("v0")
        self.log("INFO: Water turned off")
    

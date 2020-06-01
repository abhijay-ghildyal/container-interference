import logging
import redis
import json
#import sys
from pygtail import Pygtail
import time
from datetime import datetime
import re

# logFilePath="/home/abhijay/CS_533_Project/logs/experiment_w_5_processes.log"
logFilePath="/home/abhijay/CS_533_Project/logs/main.log"
lowCPUusageDocker = ""

while 1:
    for line in Pygtail(logFilePath):
        # print(line)
        
        logLine = line.split('==')

        
        timeNow = datetime.now()
#        print(timeNow)
        logTime = datetime.strptime(logLine[0].strip(), "%m/%d/%Y %I:%M:%S %p")

        log = json.loads(logLine[1].strip())

        # try:
        # print(logTime,timeNow)
        if (logTime-timeNow).total_seconds()/60 < 10:
            log = json.loads(logLine[1].strip())
            # print(log['LogType'], log['LogType'] == '1', log['LogType'] == 1)
            # if lowCPUusageDocker != "":
            #     print("\ncheck lowCPUusageDocker: not ", lowCPUusageDocker != "", " : ",log['LogType'],log['LogType'] == '1')    
            #     print(log,"\n")
            if log['LogType'] == '4':
#                    break
               # print(log)
                if log["cpu_usage"]!="['']":
                    # print("turn into json",log["cpu_usage"].replace("'",'"').replace(":",':"').replace(",",'",').replace("}",'"}'))
                    logCPUusage = json.loads(log["cpu_usage"].replace("'",'"').replace(":",':"').replace(",",'",').replace("}",'"}'))
                    # print(logCPUusage)
                    for key in logCPUusage.keys():
                        logCPUusage[key] = float(logCPUusage[key].strip())
                    
                    minValKey = min(logCPUusage, key=logCPUusage.get)
                    
                    if logCPUusage[minValKey] < 250:
                        lowCPUusageDocker = minValKey
                        print("lowCPUusageDocker: ",lowCPUusageDocker)
                        # input()
                    else:
                        lowCPUusageDocker = ""
            elif lowCPUusageDocker != "" and log['LogType'] == '1':
                batchTime = float(log["BatchTime"])
                # print("and batchTime: ", batchTime)
                if batchTime > 1:
                    print("Contention! Docker ", lowCPUusageDocker, " has current CPU usage ", logCPUusage[lowCPUusageDocker], " and the batch time of the application is ", batchTime)
                    # input()
                    # r = redis.Redis(host='localhost', port=6379, db=0)
                    # r.set('migrate', lowCPUusage)
            print("\n ===== \n")
                            
        # except Exception:
        #     continue
            
    time.sleep(2)
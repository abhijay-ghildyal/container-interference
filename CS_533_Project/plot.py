import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import re
from datetime import datetime
import numpy as np
import seaborn as sns
sns.set()
import matplotlib
cmap = matplotlib.cm.get_cmap("tab10")
import json

plt.rcParams["figure.figsize"] = (30,5)

with open('/home/abhijay/CS_533_Project/logs/experiment_w_7_processes.log','r') as f:
    lines = f.readlines()

x={}
y={}

xEpochTime={}
yEpochTime={}

xCPUtime={}
yCPUtime={}

for i, line in enumerate(lines):
    line = line.split('==')
    line[1] = line[1].strip()
    
    
    lineJson = json.loads(line[1])
    
    logTime = datetime.strptime(line[0].strip(), "%m/%d/%Y %I:%M:%S %p")
    
    # For CPU usage
    if lineJson['LogType']=='4':
        logCPUusage = json.loads(lineJson["cpu_usage"].replace("'",'"').replace(":",':"').replace(",",'",').replace("}",'"}'))
        
        if logCPUusage==['']:
            continue
        
        for key in logCPUusage.keys():
            logCPUusage[key] = float(logCPUusage[key].strip())
        
#        print(line_dict.keys())
        for key in logCPUusage.keys():
            if key in yCPUtime.keys():
                xCPUtime[key].append(logTime)
                yCPUtime[key].append(float(logCPUusage[key]))
            else:
                xCPUtime[key]=[logTime]
                yCPUtime[key] = [float(logCPUusage[key])]
                
        continue
    
#    datetime.strptime('05/26/2020 04:20:49 PM', "%m/%d/%Y %I:%M:%S %p")
    
    if int(lineJson["LogType"])==1:
        if lineJson['Docker'] in y.keys():
            x[lineJson['Docker']].append(logTime)
            y[lineJson['Docker']].append(float(lineJson['BatchTime']))
        else:
            x[lineJson['Docker']]=[logTime]
            y[lineJson['Docker']] = [float(lineJson['BatchTime'])]
    
    # epoch time
    if int(lineJson["LogType"])==2:
        if lineJson['Docker'] in yEpochTime.keys():
            xEpochTime[lineJson['Docker']].append(logTime)
            yEpochTime[lineJson['Docker']].append(float(lineJson['EpochTime']))
        else:
            xEpochTime[lineJson['Docker']]=[logTime]
            yEpochTime[lineJson['Docker']] = [float(lineJson['EpochTime'])]
    
    print( i, int(lineJson["LogType"]))   


#def movingaverage (values, window):
#    weights = np.repeat(1.0, window)/window
#    sma = np.convolve(values, weights, 'valid')
#    return sma


#for i, key in enumerate(x.keys()):
#    plt.plot(x[key][14:], movingaverage(y[key], 15), c=colors[i])

#plt.plot()

ax=plt.gca()
plt.xticks(rotation=45, ha='right')
plt.title("Batch Time (solid line plot) and Epoch Time (dotten lines are epochs 1,2..n) as the no. of dockers increase (every 30 secs)")
fmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(fmt)
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=30))

# Vertical lines for epochs
for i, keyEpochTime in enumerate(xEpochTime.keys()):
    plt.vlines(xEpochTime[keyEpochTime], ymin=0, ymax=max(list(y.values())[0])+0.1, color=cmap.colors[i], linestyle='dashed')

#Line plot for batch time
for i, key in enumerate(x.keys()):
    plt.plot(x[key], y[key], c=cmap.colors[i], label=key)

plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("BatchTime_and_EpochTime.png", dpi=400)

plt.plot()


ax=plt.gca()
fmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(fmt)
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=30))

for i, key in enumerate(xCPUtime.keys()):
    plt.plot(xCPUtime[key], yCPUtime[key], label=key)

plt.xticks(rotation=45, ha='right')
plt.title("Docker stats - CPU usage as no. of dockers increase (every 30 secs)")

plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig("CPUusage.png", dpi=400)

#plt.plot()


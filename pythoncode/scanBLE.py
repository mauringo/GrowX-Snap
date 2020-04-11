from bluepy.btle import Scanner, DefaultDelegate, UUID, Peripheral
import time
import json

from miflora.miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from mitemp_bt.mitemp_bt_poller import MiTempBtPoller, \
    MI_TEMPERATURE, MI_HUMIDITY, MI_BATTERY
import time
from btlewrap.bluepy import BluepyBackend

import os

#path = "/home/mauro/pythonMauro"

# Check current working directory.
retval = os.getcwd()
print ("Current working directory %s" % retval)

# Now change the directory
#os.chdir( path )
 



class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

    
class sensorsScan():
    newList = []
    PollingList = []
    def scanForNew(checkList):
        global newList
        a=checkList
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(8.0)
        for dev in devices:
            for (adtype, desc, value)in dev.getScanData():
                
                if adtype==2 and value=="0000fe95-0000-1000-8000-00805f9b34fb" and not dev.addr in a and not dev.addr in newList:
                    newList.append(dev.addr)

                    print("ok_ALREADY")

    def scanForNewThermo():
        a=0
        Data={}
        thermolist=[]
        with open('PollingList.json', 'r') as fh:
            Data = json.load(fh)
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(8.0)
        for dev in devices:
            for (adtype, desc, value)in dev.getScanData():
                
                if adtype==22 and (value.find("95fe5020aa01")==0 or 
value=="ffffe0e83e94490e"):
                    thermolist.append(dev.addr)                         
                    print("ok thermo")
                    a=a+1
        Data['thermos']=thermolist
        with open("PollingList.json", 'w', encoding='utf-8') as f:
                json.dump(Data, f, ensure_ascii=False, indent=4)
        return(a)
             
    def startScan():
        global newList
        newList = []
        with open('PollingList.json', 'r') as fh:
            Data = json.load(fh)
        checkList=Data['sensors']
        print(checkList)
        for i in range(1):

            sensorsScan.scanForNew(checkList)
            
            time.sleep(2)
        NewSensors={}
        NewSensors["sensors"]=newList
        with open("NewSensors.json", 'w', encoding='utf-8') as f:
            json.dump(NewSensors, f, ensure_ascii=False, indent=4)
        return len(newList)
    
    def saveNewDevice():
        Data={}
        with open('pant.json', 'r') as fh:
            Data = json.load(fh)
        wichPlant=Data['plants']
        PollingList = []
        with open('PollingList.json', 'r') as fh:
            Data = json.load(fh)
        PollingList=Data['sensors']
        PlantList=Data['plants']
        ThermoList=Data['thermos']
        with open('NewSensors.json', 'r') as fh:
            Data = json.load(fh)
        newList=Data['sensors']
        for i in newList:
            poller = MiFloraPoller(i, BluepyBackend, retries=1, cache_timeout=60)
            print(poller.parameter_value(MI_CONDUCTIVITY))
            if poller.parameter_value(MI_CONDUCTIVITY)>100:
                print("Connected "+wichPlant)
                PollingList.append(i)
                PlantList.append(wichPlant)
                print("i am recording"+ wichPlant)
                newList.remove(i)
                break
        Data['sensors']=newList
        with open("NewSensors.json", 'w', encoding='utf-8') as f:
                json.dump(Data, f, ensure_ascii=False, indent=4) 
        
        Data['sensors']=PollingList
        Data['plants']=PlantList
        Data['thermos']=ThermoList
        with open("PollingList.json", 'w', encoding='utf-8') as f:
                json.dump(Data, f, ensure_ascii=False, indent=4)  
        
        return len(newList)  
              

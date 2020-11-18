import os
import time
import json

from bluepy.btle import Scanner, DefaultDelegate, UUID, Peripheral, BTLEManagementError
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from mitemp_bt.mitemp_bt_poller import MiTempBtPoller, MI_TEMPERATURE, MI_HUMIDITY, MI_BATTERY
from btlewrap.bluepy import BluepyBackend
from file_mngr import pl_find


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

    

def scanForNew(checkList):

    newList = []
    
    for i in range(getDongleNumber()):
        print ("using dongle: "+str(i))
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(8.0)
        
        for dev in devices:
            for (adtype, _, value)in dev.getScanData():                 
                if adtype==2 and value=="0000fe95-0000-1000-8000-00805f9b34fb" and not dev.addr in checkList and not dev.addr in newList:
                    newList.append(dev.addr)

                    print("ok_ALREADY")
    
    return newList

def scanForNewThermo():

    thermoCount = 0
    Data={}
    thermolist=[]
    with open('Payloads/PollingList.json', 'r') as fh:
        Data = json.load(fh)
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(8.0)
    for dev in devices:
        for (adtype, _ , value)in dev.getScanData():
            
            if adtype==22 and (value.find("95fe5020aa01")==0 or value=="ffffe0e83e94490e" or value=="ffffef636b21d2a4"):  # or value=="ffffe0e83e94490e" or value=="ffffef636b21d2a4"
                thermolist.append(dev.addr)                         
                print("ok thermo")
                thermoCount += 1

    Data['thermos']=thermolist
    with open("Payloads/PollingList.json", 'w', encoding='utf-8') as f:
            json.dump(Data, f, ensure_ascii=False, indent=4)
            
    return thermoCount

def startScan():
    
    with open('Payloads/PollingList.json', 'r') as fh:
        Data = json.load(fh)
    checkList=Data['sensors']
    print(checkList)
    
    # for i in range(1):

    newList = scanForNew(checkList)
    #time.sleep(2)

    NewSensors={}
    NewSensors["sensors"]=newList

    with open("Payloads/NewSensors.json", 'w', encoding='utf-8') as f:
        json.dump(NewSensors, f, ensure_ascii=False, indent=4)

    return len(newList)


def saveNewDevice():

    Data={}
    with open('Payloads/Plants.json', 'r') as fh:
        Data = json.load(fh)

    whichplant=Data['plants']
    PollingList = []
    with open('Payloads/PollingList.json', 'r') as fh:
        Data = json.load(fh)
    PollingList=Data['sensors']
    PlantList=Data['plants']
    ThermoList=Data['thermos']

    with open('Payloads/NewSensors.json', 'r') as fh:
        Data = json.load(fh)
    newList=Data['sensors']
    for i in newList:
        poller = MiFloraPoller(i, BluepyBackend, retries=1, cache_timeout=60)
        print(poller.parameter_value(MI_CONDUCTIVITY))
        if (poller.parameter_value(MI_CONDUCTIVITY)>100 or poller.parameter_value(MI_MOISTURE)>40):
            print("Connected "+whichplant)
            PollingList.append(i)
            PlantList.append(whichplant)
            print("i am recording"+ whichplant)
            newList.remove(i)
            break
    Data['sensors']=newList
    with open("Payloads/NewSensors.json", 'w', encoding='utf-8') as f:
            json.dump(Data, f, ensure_ascii=False, indent=4) 
    
    Data['sensors']=PollingList
    Data['plants']=PlantList
    Data['thermos']=ThermoList
    with open("Payloads/PollingList.json", 'w', encoding='utf-8') as f:
            json.dump(Data, f, ensure_ascii=False, indent=4)  
    
    return len(newList)  

def getDongleNumber():
    i=0
    while(1):
    
        try:
            scanner = Scanner(i).withDelegate(ScanDelegate())
            devices = scanner.scan(0.1)
            i=i+1
        except  BTLEManagementError as e:
            print("endscan")
            break
        
    print("I have found "+str(i)+ " BLE dongles")     
    return i


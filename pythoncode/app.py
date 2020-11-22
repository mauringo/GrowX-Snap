from flask import Flask, redirect, render_template, request, session, url_for, Response
import os
import time
import json
import scan_BLE as Scanner
import influx_measure
from influx_measure import SystemPoller
from threading import Thread
from file_mngr import pl_find


dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path+"/uploads")
app = Flask(__name__, static_url_path='')





_SCANNINGALREADY = False
_PAIRINGALREADY = False
_PLANTSSCANNED = 0
_THERMOCOUNT = 0
def scanning():

    global _SCANNINGALREADY

    newListLen= Scanner.startScan()

    _SCANNINGALREADY = False

    return newListLen

def pairing(whichPlant):

    print("Pairing "+ whichPlant)

    newListLen =Scanner.saveNewDevice()
    

    return newListLen


def pairThermoThread():   
    global _THERMOCOUNT, _PAIRINGALREADY,_SCANNINGALREADY
    Poller.stop()
    _PAIRINGALREADY = True
    _THERMOCOUNT = Scanner.scanForNewThermo()
    _PAIRINGALREADY = False
    _SCANNINGALREADY = False

    Poller.start()


def restartThread():   
    global  _PAIRINGALREADY,_SCANNINGALREADY
    _PAIRINGALREADY = True
    Poller.stop()
   
  
    _PAIRINGALREADY = False
    _SCANNINGALREADY = False

    Poller.start()

def removeone():   
    global _THERMOCOUNT, _PAIRINGALREADY,_SCANNINGALREADY
    Poller.stop()
    _PAIRINGALREADY = True
    _THERMOCOUNT = Scanner.scanForNewThermo()
    _PAIRINGALREADY = False
    _SCANNINGALREADY = False

    Poller.start()

def pairFloraThread(whichPlant): 
    global _PLANTSSCANNED, _PAIRINGALREADY    
    Data={}   
    Poller.stop()
    _PAIRINGALREADY = True
    print("scanning")
    _PLANTSSCANNED = scanning()
    print("pairing")
    Data.clear()
    Data['plants']=whichPlant
    with open("Payloads/Plants.json", 'w', encoding='utf-8') as f:
            json.dump(Data, f, ensure_ascii = False, indent = 4)
    _PLANTSSCANNED=pairing(whichPlant)
    Poller.start()
    _PAIRINGALREADY = False
    _SCANNINGALREADY = False


#rest API functions

@app.route('/remone',methods=['GET', 'POST'])
def removeoneg():
    global _SCANNINGALREADY
    global _PAIRINGALREADY
    
    
    if  not _PAIRINGALREADY and not _SCANNINGALREADY:
        print("I have removeone")
        with open('Payloads/PollingList.json', 'r') as fh:
            Data = json.load(fh)
        PollingList=Data['sensors']
        PlantList=Data['plants']
        ThermoList=Data['thermos']

        datar = str(request.data.decode('UTF-8'))
        print (datar)
        obj = json.loads(datar)
        print (obj['sensor'])

        #sensore thermo
        if(obj['sensor']=='Thermo'):
            ThermoList=[]
        elif obj['sensor'] in PlantList :
            PollingList.pop(PlantList.index(obj['sensor'] ))
            PlantList.pop(PlantList.index(obj['sensor'] ))
            
        Data['sensors']=PollingList
        Data['plants']=PlantList
        Data['thermos']=ThermoList
        with open('Payloads/PollingList.json', 'w', encoding='utf-8') as f:
            json.dump(Data, f, ensure_ascii=False, indent=4) 
        
        restarter = Thread(target=restartThread)
        restarter.start()
        info={}
        s="Sensor Removed"
        info['status']=s
        print(s)
        resp = json.dumps(info)
        return resp

    info={}
    s="i am already pairing"
    info['status']=s
    print(s)
    resp = json.dumps(info)
    return resp

@app.route('/addone',methods=['GET', 'POST'])
def addoneg():
    global _SCANNINGALREADY
    global _PAIRINGALREADY
    
    
    if  not _PAIRINGALREADY and not _SCANNINGALREADY:
        print("I have addone")
        with open('Payloads/PollingList.json', 'r') as fh:
            Data = json.load(fh)
        PollingList=Data['sensors']
        PlantList=Data['plants']
        ThermoList=Data['thermos']

        datar = str(request.data.decode('UTF-8'))
        print (datar)
        obj = json.loads(datar)
        print (obj['sensor'])
        print ()
        
        if(obj['sensor']=='Thermo'):
            ThermoList.append(obj['MAC'])
        elif not obj['sensor'] in PlantList :
            PollingList.append(obj['MAC'])
            PlantList.append(obj['sensor'])
        elif obj['sensor'] in PlantList :
            info={}
            s =  obj['sensor'] + " has already a sensor"
            print(s)
            info['status']=s
            resp = json.dumps(info)
            return resp

        Data['sensors']=PollingList
        Data['plants']=PlantList
        Data['thermos']=ThermoList
        with open('Payloads/PollingList.json', 'w', encoding='utf-8') as f:
            json.dump(Data, f, ensure_ascii=False, indent=4) 
        
        restarter = Thread(target=restartThread)
        restarter.start()
        info={}
        s="Sensor Added"
        info['status']=s
        print(s)
        resp = json.dumps(info)
        return resp

    info={}
    s="i am already pairing"
    info['status']=s
    print(s)
    resp = json.dumps(info)
    return resp

@app.route('/remall',methods=['GET', 'POST'])
def remall():              
    global _SCANNINGALREADY
    global _PAIRINGALREADY
    global Poller 

    print("I have received: Remove All Sensors")
    Poller.stop()
    Data={}
    Data['sensors']=[]
    Data['plants']=[]
    Data['thermos']=[]
    with open('Payloads/PollingList.json', 'w', encoding='utf-8') as f:
        json.dump(Data, f, ensure_ascii=False, indent=4) 
  
    return ("All sensors removed")


@app.route('/pairthermo',methods=['GET', 'POST'])
def pairThermo():
    global _SCANNINGALREADY
    global _PAIRINGALREADY
    global Poller 
    info={}
    if  not _PAIRINGALREADY and not _SCANNINGALREADY:
        print("I have received Thermo")
        Data={}
        with open('Payloads/PollingList.json', 'r') as fh:
            Data = json.load(fh)
        PlantList=Data['plants']
        ThermoList=Data['thermos']
        if(len(ThermoList)==0): 
                  
            myScanner = Thread(target=pairThermoThread)
            myScanner.start()
            s="Scan started"
            info['status']=s
            print(s)
            resp = json.dumps(info)
            return resp
        else:
            s="Thermo already paired"
            info['status']=s
            print(s)
            resp = json.dumps(info)
            return resp
    s="i am already pairing"
    info['status']=s
    print(s)
    resp = json.dumps(info)
    return resp
            



@app.route('/pairflora',methods=['GET', 'POST'])
def PairFlora():

    global _SCANNINGALREADY
    global _PAIRINGALREADY
    global Poller 

    info={}
    print("I have received PairFlora")
    if not _PAIRINGALREADY and not _SCANNINGALREADY:
    
   
        Data={}
        with open('Payloads/PollingList.json', 'r') as fh:
            Data = json.load(fh)
        # PollingList=Data['sensors']
        PlantList=Data['plants']
        ThermoList=Data['thermos']
        
        whichPlant = str(request.data.decode('UTF-8'))
        print (whichPlant)
        str(request.data.decode('UTF-8'))
        if whichPlant in PlantList:
            s = whichPlant + " has already a sensor"
            print(s)
            info['status']=s
            resp = json.dumps(info)
            return resp
        else:
            myScanner = Thread(target=pairFloraThread,args=(whichPlant,)) 
            myScanner.start()
            s="Plant to be recorded: " + whichPlant
            info['status']=s
            print(s)
            resp = json.dumps(info)
            return resp

    elif _PAIRINGALREADY:
        s="Already in Pairing mode"
        info['status']=s
        print(s)
        resp = json.dumps(info)
        return resp
    elif _SCANNINGALREADY:
        s="Already in Scanning mode"
        print(s)
        info['status']=s
        resp = json.dumps(info)
        return resp

@app.route('/info',methods=['GET', 'POST'])
def info():
    global _SCANNINGALREADY
    global _PAIRINGALREADY
    status='Polling'
    bpairing=False
    info={}
    with open('Payloads/PollingList.json', 'r') as fh:
            Data = json.load(fh)
        # PollingList=Data['sensors']
    PlantList=Data['plants']
    ThermoList=Data['thermos']

    if (_PAIRINGALREADY or _SCANNINGALREADY):
        status='Pairing'
        bpairing=True

    
    info['status']=status
    info['pairing']=bpairing
    info['plants']=PlantList
    info['thermos']=ThermoList
    info['ndongle']=str(Poller.NofDongles)
    resp = json.dumps(info)
    return resp
    




Poller = SystemPoller()

def main():
    Poller.checkDatabase()
    Poller.start()
    app.run(host='0.0.0.0',debug = True, port=23231)

if __name__=="__main__":
    main()



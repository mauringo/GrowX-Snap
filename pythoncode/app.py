'''from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print( "Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    if(dev.addr=="58:2d:34:35:24:7b"):
   	 print ("Device %s (%s), RSSI=%d dB, " % (dev.addr, dev.addrType,dev.rssi))
   	 for (adtype, desc, value) in dev.getScanData():
       	      print ( desc+" "+ value+" "+str(adtype)+" "+str("ffffe0e83e94490e"==value)  )







'''
import scanBLE
import InfluxMeasurement2
import time
import paho.mqtt.client as mqtt
import json

import os

#path = "/home/mauro/pythonMauro"

# Check current working directory.
#retval = os.getcwd()
#print ("Current working directory %s" % retval)

# Now change the directory
#os.chdir( path )


client = mqtt.Client("python2")
broker = "127.0.0.1"

 
ScanninAlready=False
PairingAlready=False
whichPlant = 1

checkList= []

def scanning():
    global ScanninAlready
    a=scanBLE.sensorsScan.startScan()
    client.publish("scannumber", payload=a, qos=2)
    ScanninAlready= False
    return a

def pairing():
    global wichPlant
    print("Pairing "+wichPlant)
    a=scanBLE.sensorsScan.saveNewDevice()
    client.publish("tobepaired", payload=a, qos=2)
    return a

def onConnect(Client, userdate, flag, rc):
    client.subscribe(topic="Scan",qos=2)
    client.subscribe(topic="Pair",qos=2)
    client.subscribe(topic="wichplant",qos=2)
    client.subscribe(topic="PairThermo",qos=2)
    client.subscribe(topic="wichplant",qos=2)
    client.subscribe(topic="Polling",qos=2)
    client.subscribe(topic="remall",qos=2)


def onMessage(client, userdata, message):
    global ScanninAlready
    global PairingAlready
    global wichPlant

    if  message.topic=="remall":
        InfluxMeasurement2.SystemPoller.Stop()
        Data={}
        Data['sensors']=[]
        Data['plants']=[]
        Data['thermos']=[]
        with open("PollingList.json", 'w', encoding='utf-8') as f:
                json.dump(Data, f, ensure_ascii=False, indent=4)  

    if  message.topic=="PairThermo" and not PairingAlready and not ScanninAlready:
        Data={}
        with open('PollingList.json', 'r') as fh:
            Data = json.load(fh)
        PollingList=Data['sensors']
        PlantList=Data['plants']
        ThermoList=Data['thermos']
        if(len(ThermoList)==0):
            InfluxMeasurement2.SystemPoller.Stop()
            a=scanBLE.sensorsScan.scanForNewThermo()
            if(a>0):
                client.publish("ThermoResult", payload="Paired", qos=2)
            if(a==0):
                client.publish("ThermoResult", payload="Not Found", qos=2)
            PairingAlready = True
            print("scanning")
            InfluxMeasurement2.SystemPoller.Start()
            PairingAlready = False
        else:
            client.publish("ThermoResult", payload="There is already a thermometer paired", qos=2)

    if  message.topic=="Pair" and not PairingAlready and not ScanninAlready:
        Data2={}
        Data={}
        with open('PollingList.json', 'r') as fh:
            Data = json.load(fh)
        PollingList=Data['sensors']
        PlantList=Data['plants']
        ThermoList=Data['thermos']
        wichPlant = str(message.payload.decode('UTF-8'))
        if(wichPlant in PlantList):
            s=wichPlant+" has already a sensor"
            client.publish("FloraResult", payload=s, qos=2)
        else:
            print("Plat to be recorded"+wichPlant)
            Data2['plants']=wichPlant
            with open("pant.json", 'w', encoding='utf-8') as f:
                    json.dump(Data2, f, ensure_ascii=False, indent=4)
            InfluxMeasurement2.SystemPoller.Stop()
            PairingAlready = True
            print("scanning")
            a=scanning()
            print("pairing")
            b=pairing()
            if(a==b):
                client.publish("FloraResult", payload="Not Paired", qos=2)
            if(a>b):
                client.publish("FloraResult", payload="CONNECTED", qos=2)
            InfluxMeasurement2.SystemPoller.Start()
            PairingAlready = False

    if  message.topic=="Polling":
        print("III")
        if  InfluxMeasurement2.ImPolling == False:
            InfluxMeasurement2.SystemPoller.Start()
        else:
            InfluxMeasurement2.SystemPoller.Stop()
            InfluxMeasurement2.SystemPoller.Start()


   
client.connect_async(broker)

client.on_connect = onConnect
client.on_message = onMessage

client.loop_forever()


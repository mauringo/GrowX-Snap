import os
import time
import json

import scan_BLE as Scanner
import influx_measure
from influx_measure import SystemPoller
import paho.mqtt.client as mqtt
from file_mngr import pl_find


_BROKER = "127.0.0.1"

_SCANNINGALREADY = False
_PAIRINGALREADY = False


def scanning():

    global _SCANNINGALREADY

    newListLen= Scanner.startScan()
    client.publish("scannumber", payload= newListLen, qos=2)
    _SCANNINGALREADY = False

    return newListLen

def pairing(whichPlant):

    print("Pairing "+ whichPlant)

    newListLen =Scanner.saveNewDevice()
    client.publish("tobepaired", payload= newListLen, qos=2)
    
    return newListLen

def onConnect(client, userdata, flag, rc):
    

    client.subscribe(topic="Scan",qos=2)
    client.subscribe(topic="Pair",qos=2)
    client.subscribe(topic="whichPlant",qos=2)
    client.subscribe(topic="PairThermo",qos=2)
    client.subscribe(topic="whichPlant",qos=2)
    client.subscribe(topic="Polling",qos=2)
    client.subscribe(topic="remall",qos=2)
    

def onMessage(client, userdata, message):
    
    """TOPICS LIST
        -remall
        -PairThermo
        -Pair
        -Polling
    """    
    
    global _SCANNINGALREADY
    global _PAIRINGALREADY

    global Poller 

    """TOPIC REMALL"""

    if  message.topic=="remall":
        print("I have received"+" "+message.topic)
        Poller.stop()
        Data={}
        Data['sensors']=[]
        Data['plants']=[]
        Data['thermos']=[]
        with open('Payloads/PollingList.json', 'w', encoding='utf-8') as f:
                json.dump(Data, f, ensure_ascii=False, indent=4)  
 

    
    """TOPIC PAIRTHERMO"""

    if  message.topic=="PairThermo" and not _PAIRINGALREADY and not _SCANNINGALREADY:
        print("I have received"+" "+message.topic)
        Data={}
        with open('Payloads/PollingList.json', 'r') as fh:
            Data = json.load(fh)
        # PollingList=Data['sensors']
        PlantList=Data['plants']
        ThermoList=Data['thermos']
        if(len(ThermoList)==0):
            Poller.stop()
            thermoCount = Scanner.scanForNewThermo()

            if(thermoCount>0):
                client.publish("ThermoResult", payload="Thermometer Paired", qos=2)
            if(thermoCount==0):
                client.publish("ThermoResult", payload="Thermometer Not Found", qos=2)

            _PAIRINGALREADY = True
            print("scanning")

            Poller.start()
            _PAIRINGALREADY = False
        else:
            client.publish("ThermoResult", payload="There is already a thermometer paired", qos=2)

    """TOPIC PAIR"""


    if  message.topic=="Pair":
        print("I have received"+" "+message.topic)
        if not _PAIRINGALREADY and not _SCANNINGALREADY:

            Data={}
            with open('Payloads/PollingList.json', 'r') as fh:
                Data = json.load(fh)
            # PollingList=Data['sensors']
            PlantList=Data['plants']
            ThermoList=Data['thermos']
            
            whichPlant = str(message.payload.decode('UTF-8'))

            if whichPlant in PlantList:
                s = whichPlant + " has already a sensor"
                client.publish("FloraResult", payload = s, qos = 2)
            else:
                print("Plant to be recorded" + whichPlant)
                Data.clear()
                Data['plants']=whichPlant
                with open("Payloads/Plants.json", 'w', encoding='utf-8') as f:
                        json.dump(Data, f, ensure_ascii = False, indent = 4)

                Poller.stop()
                _PAIRINGALREADY = True
                print("scanning")
                scannedPlantListLen = scanning()
                print("pairing")
                PairedPlantListLen=pairing(whichPlant)

                if scannedPlantListLen == PairedPlantListLen:
                    client.publish("FloraResult", payload="Plant Not Paired", qos=2)
                if scannedPlantListLen>PairedPlantListLen:
                    client.publish("FloraResult", payload="Plant Paired", qos=2)

                Poller.start()
                _PAIRINGALREADY = False

        elif _PAIRINGALREADY:
            client.publish("FloraResult", payload = "Already in Pairing mode")
        elif _SCANNINGALREADY:
            client.publish("FloraResult", payload = "Already in Scanning mode")      

    """POLLING"""
    
    if  message.topic=="Polling":

        print("III")
        if  Poller.ImPolling == False():
            Poller.start()
        else:
            Poller.stop()
            Poller.start()




Poller = SystemPoller()

def main():
    Scanner.getDongleNumber()
    Poller.start()

if __name__=="__main__":
    main()

client = mqtt.Client("python2")
client.connect_async(_BROKER)
client.on_connect = onConnect
client.on_message = onMessage
client.loop_forever()

from threading import Thread
import datetime
import json
from influxdb import InfluxDBClient
from miflora.miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from mitemp_bt.mitemp_bt_poller import MiTempBtPoller, \
    MI_TEMPERATURE, MI_HUMIDITY, MI_BATTERY
import time
from btlewrap.bluepy import BluepyBackend
from bluepy.btle import BTLEException
from btlewrap import GatttoolBackend

import os

#path = "/home/mauro/pythonMauro"

# Check current working directory.
#retval = os.getcwd()
#print ("Current working directory %s" % retval)

# Now change the directory
#os.chdir( path )






host='localhost'
port=8086
user = ''
password = ''
dbname = 'room1'



client = InfluxDBClient(host, port, user, password, dbname)

ImPolling = False

class SystemPoller():
    PollingList = []
    PlantList = []
    ThermoList = []
    Data = {}
    
    x = None
    def loadPollingConf():
        
        global PollingList
        global PlantList
        global ThermoList
        with open('PollingList.json', 'r') as fh:
            Data = json.load(fh)
        PollingList=Data['sensors']
        PlantList=Data['plants']
        ThermoList=Data['thermos']
        
    
      
    def PollingThread():
        global ImPolling
        if(len(PollingList))==0:
            return
        while 1:
            print("Polling Start")
            i = 0 
            d = 0
            for d in range(len(PollingList)):    
                SystemPoller.SendInfluxMIflora(client,PollingList[d],PlantList[d])
                for j in range (60):
                    time.sleep(1)
                    if ImPolling==False:
                        return
            for d in range(len(ThermoList)):    
                SystemPoller.SendInfluxMIthermo(client,ThermoList[d])
                for j in range (60):
                    time.sleep(1)
                    if ImPolling==False:
                        return
    
        
        
        
        
    def SendInfluxMIflora(InfluxDBClient,MAC,sensor_id):
        poller = MiFloraPoller(MAC, BluepyBackend, retries=1, cache_timeout=30)
        print(sensor_id)
        measurement=("Flora"+str(sensor_id))

        try:
            Flora = [
                {
                    "measurement": measurement,
                    "fields": {
                        "Battery": poller.parameter_value(MI_BATTERY),
                        "Temperature": poller.parameter_value(MI_TEMPERATURE),
                        "Light":poller.parameter_value(MI_LIGHT),
                        "Conductivity": poller.parameter_value(MI_CONDUCTIVITY),
                        "Moisture": poller.parameter_value(MI_MOISTURE)
                    }
                }
            ]
            client.write_points(Flora)

        except BTLEException as e:
            print(datetime.datetime.now(), "Error connecting to Flora")
        except Exception as e:
            availability = 'offline'
        except BrokenPipeError as e:
            print(datetime.datetime.now(), "Error polling device. Flora"+str(MAC)+" BROKENPIPE")
        poller.clear_cache()

    def Stop():
        global ImPolling
    
        print("stopping")
        if( ImPolling==True):
            ImPolling= False
            x.join()



    def SendInfluxMIthermo(InfluxDBClient,MAC):
        print("thermo: "+MAC )
        pollerTemp = MiTempBtPoller(MAC, BluepyBackend, retries=1, cache_timeout=30)
        try:    
            Thermo = [
            {
                "measurement": "Thermo",
                "fields": {
                    "Battery": (pollerTemp.parameter_value(MI_BATTERY)),
                    "Temperature": (pollerTemp.parameter_value(MI_TEMPERATURE)),
                    "Humidity": (pollerTemp.parameter_value(MI_HUMIDITY))
                }
            }
            ]   
            client.write_points(Thermo)
        except BTLEException as e:
            print(datetime.datetime.now(), "Error connecting to device")
        except Exception as e:
            availability = 'offline'
            print(datetime.datetime.now(), "Error polling device. Device might be unreachable or offline.")
        except BrokenPipeError as e:
            print("BrokenPipeError Thermo")
        pollerTemp.clear_cache()
        
    def Start():
        global ImPolling
        global x
        
        print("startin")
        SystemPoller.loadPollingConf()
        ImPolling= True
        x=Thread(target=SystemPoller.PollingThread)
        x.start()

    
    
    
SystemPoller.Start()


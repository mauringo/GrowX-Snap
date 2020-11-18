import os
import time
import datetime
import json
from threading import Thread

from influxdb import InfluxDBClient
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from mitemp_bt.mitemp_bt_poller import MiTempBtPoller, MI_TEMPERATURE, MI_HUMIDITY, MI_BATTERY

from btlewrap.bluepy import BluepyBackend
from bluepy.btle import BTLEException
from btlewrap import GatttoolBackend


# host='localhost'
# port=8086
# user = ''
# password = ''
# dbname = 'room1'


class SystemPoller():
    
    PollingList = []
    PlantList = []
    ThermoList = []
    ImPolling = False
    client = InfluxDBClient('localhost', 8086, '', '', 'room1')
    x = None

    def __init(self):
        pass


    @staticmethod
    def _loadPollingConf():
        Data = {}
        with open('Payloads/PollingList.json', 'r') as fh:
            Data = json.load(fh)

        SystemPoller.PollingList=Data['sensors']
        SystemPoller.PlantList=Data['plants']
        SystemPoller.ThermoList=Data['thermos']
        
    
    @classmethod  
    def _pollingThread(cls):
        if(len(cls.PollingList))==0 and len(cls.ThermoList)==0:
            return
        while True:
            print("Polling Start")
            for d in range(0, len(cls.PollingList)):    
                SystemPoller.SendInfluxMIflora(cls.client,cls.PollingList[d],cls.PlantList[d])
                for _ in range (0, 60):
                    time.sleep(1)
                    if not cls.ImPolling:
                        return
                        
            for d in range(0, len(cls.ThermoList)):    
                SystemPoller.SendInfluxMIthermo(cls.client,cls.ThermoList[d])
                for _ in range (0, 60):
                    time.sleep(1)
                    if not cls.ImPolling:
                        return
    
        
        
        
    @classmethod  
    def SendInfluxMIflora(cls, InfluxDBClient, MAC, sensor_id):

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
            cls.client.write_points(Flora)

        except BTLEException as e:
            print(datetime.datetime.now(), "Error connecting to Flora: error {}".format(e))
        except BrokenPipeError as e:
            print(datetime.datetime.now(), "Error polling device. Flora"+str(MAC)+" BROKENPIPE")
        except Exception as e:
            availability = 'offline'
            print (availability)


        poller.clear_cache()

    @classmethod
    def SendInfluxMIthermo(cls, InfluxDBClient, MAC):

        print("thermo: " + MAC )
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
            cls.client.write_points(Thermo)
        except BTLEException as e:
            print(datetime.datetime.now(), "Error connecting to device: error {}".format(e))
        except BrokenPipeError as e:
            print("BrokenPipeError Thermo")
        except Exception as e:
            #availability = 'offline'
            print(datetime.datetime.now(), "Error polling device. Device might be unreachable or offline.")

        pollerTemp.clear_cache()
    
    @classmethod
    def start(cls):
        
        print("starting")
        SystemPoller._loadPollingConf()
        SystemPoller.ImPolling = True
        SystemPoller.x = Thread(target = cls._pollingThread)
        SystemPoller.x.start()
        print("polling thread lanciato")


    @staticmethod
    def stop():
            
        print("stopping")
        
        if SystemPoller.ImPolling:
            if(SystemPoller.x.isAlive()):
                SystemPoller.ImPolling = False
                SystemPoller.x.join()
            else :
                SystemPoller.ImPolling = False


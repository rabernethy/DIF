# track.py: a 4G Tote Tracking Solution in Python3
# Written by Russell Abernethy

import re
from types import LambdaType
from urllib3 import Timeout
from serial import Serial
from pynmeagps import NMEAReader
from bluepy.btle import Scanner, DefaultDelegate
import time
import requests
import os

tote_url = 'http://127.0.0.1:5000/totes'
thing_board_url = 'https://mis3502-shafer.com/azureboard' # http://20.53.192.107/home 
totes = []
ids = []

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered Device", dev.addr)
        elif isNewData:
            print("Received New Data From", dev.addr)

		
def parse_device_scan(nmr): 
# Parses responses for ones with Latitude & Longitude then adds devices found nearby
    f = []
    found = False
    while not found:
        try:
            (raw, parsed) = nmr.read()
            lat = parsed.lat
            lon = parsed.lon
            # check if the module received a usable signal
            if type(lat) == type(1.1): 
                found = True
        # Ignore entries without GPS
        except AttributeError:
            continue
        f.append([lat,lon])
    for dev in devices:
        f.append(dev.addr)
    return f

if __name__ == '__main__':

    scanner = Scanner().withDelegate(ScanDelegate())
    stream = Serial('/dev/serial0', 9600, timeout=3)
    nmr = NMEAReader(stream)

    while True:

        print("Scanning for nearby totes:")

        devices = scanner.scan(30.0)
        results = parse_device_scan(nmr)

        try:
            r = requests.get(tote_url, timeout=5)
            totes = r.json()
            for t in totes:
                ids.append(t[2])
        except (requests.ConnectionError, requests.Timeout) as e:
            print(e)
        
        print("Processing found devices:")

        lat = results[0][0]
        lon = results[0][1]
        print(lon)
        results = results[1:]
        print(results)

        for device in results:
            for id in ids:
                if id == device.replace('\n', ""):
                    for tote in totes:
                        if tote[2] == id:
                            data = {'latitude':lat,
                                    'longitude':lon,
                                    'deviceid':tote[3],
                                    'ABtelemetrytime': time.time()}
                            resp = requests.post(thing_board_url, data = data)
                            print("Tote {w}{n} Data Sent to ThingsBoard with response status {r}.\n".format(w=tote[0],n=tote[1],r=resp.status_code))
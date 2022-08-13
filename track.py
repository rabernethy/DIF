# track.py: a 4G Tote Tracking Solution in Python3
# Written by Russell Abernethy

from serial import Serial
from pynmeagps import NMEAReader
from bluepy.btle import Scanner, DefaultDelegate
import time, requests

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
    print("Parsing GPS Data")
    f = []
    found = False
    while not found:
        try:
            (raw, parsed) = nmr.read()
            lat = 39.98489822316684 # testing value
            lon = -75.1489530825776 # testing value
            #lat = parsed.lat
            #lon = parsed.lon
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
        
        print("Processing found devices:")

        lat = results[0][0]
        lon = results[0][1]
        results = results[1:]
        print(results)

        for device in results:
            data = {'latitude':lat,
                    'longitude':lon,
                    'deviceid':device.replace('\n',"").replace(":",""),
                    'ABtelemetrytime': time.time()}
            resp = requests.post(thing_board_url, data = data)
            print("Tote {w} Data Sent to ThingsBoard with response status {r}.\n".format(w=device.replace('\n',"").replace(":",""),r=resp.status_code))
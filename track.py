# track.py: a 4G Tote Tracking Solution in Python3
# Written by Russell Abernethy

from serial import Serial
from pynmeagps import NMEAReader
from bluepy.btle import Scanner, DefaultDelegate, BTLEDisconnectError
from requests.exceptions import ConnectionError
import requests
import RPi.GPIO as GPIO
import time

ser = Serial('/dev/ttyS0',115200)
ser.flushInput()

power_key = 6
time_count = 0
btle_scan_duration = 6
rec_buff = ''
rec_buff2 = ''
totes = []
ids = []
thing_board_url = 'https://mis3502-shafer.com/azureboard' # http://20.53.192.107/home


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered Device", dev.addr)
        elif isNewData:
            print("Received New Data From", dev.addr)

def send_at(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' ERROR')
            print(command + ' back:\t' + rec_buff.decode())
            return 0
        else:
            return rec_buff.decode()
    else:
        print('GPS is not ready')
        return 0


def get_gps_position():
    rec_null = True
    answer = 0
    rec_buff = ''
    
    print('Start GPS session...')
    send_at('AT+CGPS=1,1','OK',1)
    time.sleep(2)
    
    while rec_null:
        answer = send_at('AT+CGPSINFO','+CGPSINFO: ',1)
        if 1 == answer:
            answer = 0
            if ',,,,,,' in rec_buff:
                print('GPS is not ready')
                rec_null = False
                time.sleep(1)
        else:
            if answer == 0:
                print('error %d'%answer)
                rec_buff = ''
                send_at('AT+CGPS=0','OK',1)
            else:
                return answer
        time.sleep(1.5)


def power_on(power_key):
    print('SIM7600X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    print('SIM7600X is ready')
   
def parse_device_scan(nmr):
# Parses responses for ones with Latitude & Longitude then adds devices found nearby
    print("Parsing GPS Data")
    f = []
    found = False
    while not found:
        try:
            #lat,lon = 39.98489822316684,-75.1489530825776 # testing value
            while True:
                gps = get_gps_position()
                if gps is False:
                    continue
                else:
                    break
                    
            lat_lon_together = gps[gps.find("INFO:")+6:gps.find("OK")]
            
            lat = lat_lon_together[:lat_lon_together.find(",")]
            if lat.find('.') == 4:
                lat = lat.replace(".","")
                lat = lat[:2] +"." + lat[2:]
           
            else:
                lat = lat.replace(".","")
                lat = lat[:3] +"." + lat[3:]
                lat = "-" + lat[1:]
           
            lon = lat_lon_together[lat_lon_together.find("N")+2:lat_lon_together.find("W")-1]
            if lon.find('.') == 4:
                lon = lon.replace(".","")
                lon = lon[:2] +"." + lon[2:]
            else:
                lon = lon.replace(".","")
                lon = lon[:3] +"." + lon[3:]
                lon = "-" + lon[1:]

            # check if the module received a usable signal
 
            found = True
        # Ignore entries without GPS
        except AttributeError:
            continue
        f.append([float(lat),float(lon)])
    for dev in devices:
        f.append(dev.addr)
    print("Acquired GPS Data: <lat: {}|lon: {}>".format(lat,lon))
    return f

if __name__ == '__main__':
   
    # Set up GPS Device
    nmr = NMEAReader(ser)
    power_on(power_key)
    while True:
        try:
            print("Scanning for nearby totes:")
            scanner = Scanner().withDelegate(ScanDelegate())
            devices = scanner.scan(btle_scan_duration)
            results = parse_device_scan(nmr)
       
            print("Processing found devices:")

            lat = results[0][0]
            lon = results[0][1]
            results = results[1:]
           
            for device in results:
                data = {'latitude':lat,
                        'longitude':lon,
                        'deviceid':device.replace('\n',"").replace(":",""),
                        'ABtelemetrytime': time.time()}
                while True:
                    try:
                        resp = requests.post(thing_board_url, data = data)
                        break
                    except ConnectionError:
                        print("Connection Error")
                print("Tote {w} Data Sent to ThingsBoard with response status {r}.\n".format(w=device.replace('\n',"").replace(":",""),r=resp.status_code))
        except BTLEDisconnectError:
            print("Connection Error")
            continue

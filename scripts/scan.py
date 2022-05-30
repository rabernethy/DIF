# scan.py written by Russell Abernethy
from msilib import type_string
from socket import timeout
from serial import Serial
from pynmeagps import NMEAReader
from bluepy.btle import Scanner, DefaultDelegate
import datetime


class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		if isNewDev:
			print("Discovered Device", dev.addr)
		elif isNewData:
			print("Received New Data From", dev.addr)

		
def write_device_data_to_log(nmr):
	with open("logs/{}".format(datetime.datetime.now()),"w") as f:
		# get a gps reading that has latitude, longitude, and time
		found = False
		while not found:
			try:
				(raw, parsed) = nmr.read()

				print(parsed)

				lat = parsed.lat
				lon = parsed.lon

				# check if the module received a usable signal
				if type(lat) == type(1.1): 
					found = True

			except AttributeError:
				continue
		f.write("{lat}\n{lon}\n".format(lat=lat, lon=lon))


		for dev in devices:
			f.write("{addr}\n".format(addr=dev.addr))



scanner = Scanner().withDelegate(ScanDelegate())
stream = Serial('/dev/serial0', 9600, timeout=3)
nmr = NMEAReader(stream)

print("BLE Tote Scanner Started")
while True:	
	print("Scanning")
	devices = scanner.scan(10.0)
	print("Logging Scanned Devices")
	write_device_data_to_log(nmr)

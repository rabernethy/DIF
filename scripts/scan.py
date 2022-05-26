# scan.py written by Russell Abernethy
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

		
def write_device_data_to_log():
	with open("logs/{}".format(datetime.datetime.now()),"w") as f:
		for dev in devices:
			f.write("Device {addr}\n".format(addr=dev.addr))



scanner = Scanner().withDelegate(ScanDelegate())
print("BLE Tote Scanner Started")
while True:	
	print("Scanning")
	devices = scanner.scan(10.0)
	print("Logging Scanned Devices")
	write_device_data_to_log()

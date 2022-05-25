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

		
def write_data_to_log():
	with open("logs/{}".format(datetime.datetime.now()),"w") as f:
		for dev in devices:
			if dev.addr.startswith("ff:ff"):
				f.write("Device {addr} {type},RSSI = {rssi} dB\n".format(addr=dev.addr,type=dev.addrType, rssi=dev.rssi))
				for (adtype,desc,value) in dev.getScanData():
					f.write("{desc} = {val}\n".format(desc=desc,val=value))
			f.write("\n")


scanner = Scanner().withDelegate(ScanDelegate())
print("BLE Tote Scanner Started")
while True:	
	print("Scanning")
	devices = scanner.scan(10.0)
	print("Logging Scanned Devices")
	write_data_to_log()

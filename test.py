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
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

print("\n")
itr=0
with open("log{}".format(datetime.datetime.now()),"w") as f:
	for dev in devices:
		
		if dev.addr.startswith("ff:ff"):
			itr+=1
			f.write("Device {addr} {type},RSSI = {rssi} dB\n".format(addr=dev.addr,type=dev.addrType, rssi=dev.rssi))
			for (adtype,desc,value) in dev.getScanData():
				f.write("{desc} = {val}\n".format(desc=desc,val=value))
		f.write("\n")
print("Number of devices: {}".format(itr))

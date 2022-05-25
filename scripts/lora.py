from machine import Pin, UART
from time import sleep_ms

class RYLR896:
	def __init__(self, port_num, tx_pin='', rx_pin=""):
		if tx_pin== "" and rx_pin== "":
			self._uart = UART(port_num)
		else:
			self._uart = UART(port_num,tx=tx_pin, rx=rx_pin)
	def cmd(self, lora_cmd):
		self._uart.write('{}\r\n'.format(lora_cmd))
		while(self._uart.any()==0):
			pass
		reply = self._uart.readline()
		print(reply.decode().strip('\r\n'))

	def test(self):
		self._uart.write('AT\r\n')
		while(self._uart.any()==0):
			pass
		reply = self._uart.readline()
		print(reply.decode().strip('\r\n'))

	def set_addr(self, addr):
		self._uart.write('AT+ADDRESS={}\r\n'.format(addr))
		while(self._uart.any() == 0):
			pass
		reply = self._uart.readline()
		print(reply.decode().strip('\r\n'))

	def send_msg(self, addr, msg):
		self._uart.write('AT+SEND={},{},{}\r\n'.format(addr, len(msg),msg))
		while(self._uart.any() == 0):
			pass
		reply = self._uart.readline()
		print(reply.decode().strip('\r\n'))

	def read_msg(self):
		if self._uart.any() == 0:
			print('Nothing to Show')
		else:
			msg = ''
			while(self._uart.any()):
				msg = msg + self._uart.read(self._uart.any()).decode()
			print(msg.strip('\r\n'))

lora = RYLR896(1)
sleep_ms(100)
lora.set_addr(1)

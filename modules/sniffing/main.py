import pyshark
import bluetooth


def wifi():
	def processPacket(packet):
		pass

	capture = pyshark.LiveCapture(interface = 'eth0')
	capture.sniff()
	capture.apply_on_packets(processPacket)


def bluetooth_sniff():
	devices = bluetooth.discover_devices(lookup_names=True)
	for addr,name in devices:
		print(addr,name)

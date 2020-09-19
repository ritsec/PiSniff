import pyshark


def wifi():
	def processPacket(packet):
		pass

	capture = pyshark.LiveCapture(interface = 'eth0')
	capture.sniff()
	capture.apply_on_packets(processPacket)


def bluetooth():
	pass

# sudo apt install python3-pip tshark libxslt-dev python3-scapy bluez
# sudo pip3 install pyshark scapy
# https://scapy.readthedocs.io/en/latest/layers/bluetooth.html#opening-a-hci-socket

import pyshark
from scapy.layers.bluetooth import *


def wifi():
	def processPacket(packet):
		pass

	capture = pyshark.LiveCapture(interface = 'mon0')
	capture.sniff()
	capture.apply_on_packets(processPacket)


def bluetooth():
	pass

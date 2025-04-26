# Adafruit_CircuitPython_Wiznet5k example for LuckFox Pico Mini

"""
W5500  Pico
MISO   GPIO51
MOSI   GPIO50
SCLK   GPIO49
RST    GPIO55
RCS    GPIO54
"""

import board
import busio
import digitalio
import adafruit_connection_manager
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import struct
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--tz', type=int, help='time zone', default=0)
args = parser.parse_args()
print("args.tz={}".format(args.tz))

# Initialize module
cs_pin = digitalio.DigitalInOut(board.G54)
reset_pin = digitalio.DigitalInOut(board.G55)
spi_bus = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize ethernet interface with DHCP
#eth = WIZNET5K(spi_bus, cs)
eth = WIZNET5K(spi_bus, cs=cs_pin, reset=reset_pin, mac='DE:AD:BE:EF:FE:ED')

# Initialize socket
socket = adafruit_connection_manager.get_radio_socketpool(eth)
#print(dir(socket))

REF_TIME_1970 = 2208988800		# Reference time
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = b'\x1b' + 47 * b'\0'
addr='time.google.com'
client.sendto(data, (addr, 123))
data, address = client.recvfrom(1024)
if data:
	t = struct.unpack('!12I', data)[10]
	t -= REF_TIME_1970
	utc = datetime.datetime.utcfromtimestamp(t)
	print(utc)

	t = t + (args.tz * 60 * 60)
	local = datetime.datetime.utcfromtimestamp(t)
	print(local)

# Adafruit_CircuitPython_Wiznet5k example for LuckFox Pico Mini

"""
W5500  Pico
MISO   GPIO51
MOSI   GPIO50
SCLK   GPIO49
RST    GPIO55
RCS    GPIO54

server side
netcat -ulk 8080
"""


import board
import busio
import digitalio
import adafruit_connection_manager
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--host', help='tcp host', default="192.168.10.46")
parser.add_argument('--port', type=int, help='udp port', default=8080)
args = parser.parse_args()
print("args.host={}".format(args.host))
print("args.port={}".format(args.port))

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

serv_address = (args.host, args.port)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
t = time.time()
local_time = time.localtime(t)
asc_time = time.asctime(local_time)
print("asc_time={}".format(asc_time))
bytes_time = bytes(asc_time, 'utf-8')
send_len = client.sendto(bytes_time, serv_address)
client.close()

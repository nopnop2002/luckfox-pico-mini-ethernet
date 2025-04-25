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
import adafruit_requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K

print("Wiznet5k WebClient Test")

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
#JSON_URL = "http://api.coindesk.com/v1/bpi/currentprice/USD.json"
JSON_URL = "http://httpbin.org/delay/3"

# Initialize module
cs_pin = digitalio.DigitalInOut(board.G54)
reset_pin = digitalio.DigitalInOut(board.G55)
spi_bus = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize ethernet interface with DHCP
#eth = WIZNET5K(spi_bus, cs)
eth = WIZNET5K(spi_bus, cs=cs_pin, reset=reset_pin, mac='DE:AD:BE:EF:FE:ED')

# Initialize a requests session
pool = adafruit_connection_manager.get_radio_socketpool(eth)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(eth)
requests = adafruit_requests.Session(pool, ssl_context)

print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))
print("IP lookup adafruit.com: %s" % eth.pretty_ip(eth.get_host_by_name("adafruit.com")))


# eth._debug = True
print("Fetching text from", TEXT_URL)
r = requests.get(TEXT_URL)
print("-" * 40)
print(r.text)
print("-" * 40)
r.close()

print()
print("Fetching json from", JSON_URL)
r = requests.get(JSON_URL)
print("-" * 40)
print(r.json())
print("-" * 40)
r.close()

print("Done!")

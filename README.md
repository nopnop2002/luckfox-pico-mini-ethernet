# luckfox-pico-mini-ethernet
LuxkFox Pico Mini is a small Linux board.   
This board runs Ubuntu, but it does not have network functionality.   
We can use the W5500 SPI Ethernet module.   

# Software requirements   
- Adafruit Blinka   
- Adafruit CircuitPython Wiznet5k   

# Hardware requirements   
- W5500 SPI Ethernet module   

# Install Ubuntu on PicoMini   
The Ubuntu image is available from the Google Cloud Link [here](https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-RV1103/Luckfox-Pico-prepare).    
The SD card writing tool (SocToolKit.exe) and writing procedures are published [here](https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-SD-Card-burn-image/).   

# Enable network sharing for RNDIS   
Instructions for network sharing using a Windows machine as the host can be found [here](https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-RV1106/Luckfox-Pico-Ultra-W/Luckfox-Pico-quick-start/Network-Sharing/ubuntu).   
You can now download the software you need.   

# Install gcc-12   
The gcc included in the image is gcc-11, but it is broken and unusable.   
Follow the steps below to install gcc-12.   
```
$ sudo apt update

$ sudo apt install g++-12

$ sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 11

$ sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 12

$ sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 11

$ sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 12

$ gcc --version
gcc (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
Copyright (C) 2022 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ g++ --version
g++ (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
Copyright (C) 2022 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

# Recreate the link for arm-linux-gnueabihf-gcc   
arm-linux-gnueabihf-gcc cannot be used because it is linked to gcc-11.   
Recreate the link.   
```
$ sudo unlink /usr/bin/arm-linux-gnueabihf-gcc

$ sudo ln -s gcc-12 /usr/bin/arm-linux-gnueabihf-gcc

$ ls -l /usr/bin/arm-linux-gnueabihf-gcc
lrwxrwxrwx 1 root root 6 Apr 16 14:32 /usr/bin/arm-linux-gnueabihf-gcc -> gcc-12

$ arm-linux-gnueabihf-gcc --version
arm-linux-gnueabihf-gcc (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
Copyright (C) 2022 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

# Install Adafruit Blinka
```
$ python3 -m pip install adafruit-blinka
```

# Adafruit CircuitPython Wiznet5k
```
$ python3 -m pip install adafruit-circuitpython-wiznet5k
```
# Wiring to the W5500 module
|W5500||PicoMini|
|:-:|:-:|:-:|
|MISO|--|GPIO51|
|MOSI|--|GPIO50|
|SCLK|--|GPIO49|
|RST|--|GPIO55|
|RCS|--|GPIO54|
|GND|--|GND|
|3.3V|--|3.3V|


# Test Adafruit CircuitPython Wiznet5k
This script will get a DHCP address from your router.
```
$ cd connect-dhcp

$ sudo -E python3 main.py
eth.ipv4_address=192.168.10.108
```

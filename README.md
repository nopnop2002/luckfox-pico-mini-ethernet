# luckfox-pico-mini-ethernet
LuckFox Pico Mini is a very small Linux board.   
![Image](https://github.com/user-attachments/assets/99665cda-ba36-4de3-a1a9-d8cf117ef590)

This board runs Ubuntu, but it does not have network functionality.   
![Image](https://github.com/user-attachments/assets/7938e371-6be8-4acd-82b5-e38e85d1f44c)

We can use the W5500 SPI Ethernet module.   
We can use `python's low-level network interface` with this module.   

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

# Install gcc-12 on PicoMini   
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

# Install Adafruit Blinka on PicoMini
```
$ python3 -m pip install adafruit-blinka
```

# Install Adafruit CircuitPython Wiznet5k on PicoMini
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


# Test your W5500 module
This script will get an IP address from the DHCP server and display it.   
```
$ git clone https://github.com/nopnop2002/luckfox-pico-mini-ethernet

$ cd connect-dhcp

$ sudo -E python3 main.py
eth.ipv4_address=192.168.10.108
```

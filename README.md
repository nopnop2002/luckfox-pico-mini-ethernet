# luckfox-pico-mini-ethernet
LuckFox Pico Mini is a very small Linux board.   
![Image](https://github.com/user-attachments/assets/99665cda-ba36-4de3-a1a9-d8cf117ef590)

This board runs Ubuntu, but it does not have Ethernet/WiFi functionality.   
![Image](https://github.com/user-attachments/assets/7938e371-6be8-4acd-82b5-e38e85d1f44c)

We can use the W5500 SPI Ethernet module.   
We can use `python's low-level network interface` with this module.   
![Image](https://github.com/user-attachments/assets/310b11db-7583-431e-8087-3f435c90b121)

# Software requirements   
- Adafruit Blinka   
- Adafruit CircuitPython Wiznet5k   

# Hardware requirements   
- LuckFox Pico Mini   
- W5500 SPI Ethernet module   

# Install Ubuntu on PicoMini   
The Ubuntu image is available from the Google Cloud Link [here](https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-RV1103/Luckfox-Pico-prepare).    
The Ubuntu image is in the backup folder.   
The SD card writing tool (SocToolKit.exe) and writing procedures are published [here](https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-SD-Card-burn-image/).   

# Enable network sharing for RNDIS   
The Ubuntu image provides networking using the RNDIS protocol.   
Instructions for network sharing using a Windows machine as the host can be found [here](https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-RV1106/Luckfox-Pico-Ultra-W/Luckfox-Pico-quick-start/Network-Sharing/ubuntu).   
Ubuntu and Debian can also work as network share servers for RNDIS.   
Network sharing using a Linux environment such as Ubuntu/Debian as the host is [here](https://github.com/nopnop2002/luckfox-pico-mini-ethernet/tree/main/Network-sharing).   
You can now download the software you need.   

# Add a swap partition to PicoMini   
I used a 16GB Micro SD card.   
The last partition(mmcblk1p8) is unused.   
So we can use this partition as SWAP.   
```
$ lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
mtdblock0    31:0    0  128M  0 disk
mmcblk1     179:0    0 14.8G  0 disk
tqmmcblk1p1 179:1    0   32K  0 part
tqmmcblk1p2 179:2    0  512K  0 part
tqmmcblk1p3 179:3    0  256K  0 part
tqmmcblk1p4 179:4    0   32M  0 part
tqmmcblk1p5 179:5    0  512M  0 part /oem
tqmmcblk1p6 179:6    0  256M  0 part /userdata
tqmmcblk1p7 179:7    0    6G  0 part /
mqmmcblk1p8 179:8    0  8.1G  0 part

$ sudo mkswap /dev/mmcblk1p8
Setting up swapspace version 1, size = 8.1 GiB (8649404416 bytes)
no label, UUID=711d63de-3b59-40c2-b668-baf626b9be6e

$ sudo swapon /dev/mmcblk1p8
[  105.830584] Adding 53443804k swap on /dev/mmcblk1p8.  Priority:-2 extents:1 across:53443804k SS

$ free -h
               total        used        free      shared  buff/cache   available
Mem:            33Mi        14Mi       1.0Mi       0.0Ki        17Mi        16Mi
Swap:          9.1Gi        22Mi       9.0Gi
```


# Install gcc-12 on PicoMini   
The gcc available in the official images is gcc-11, but it's broken and unusable.   
Follow the steps below to install gcc-12.   
`apt update/install` will take about 60 minutes.   
```
$ sudo apt update

$ sudo apt install g++-12

$ sudo apt install --reinstall libc6-dev -y

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
$ ls -l /usr/bin/arm-linux-gnueabihf-gcc
lrwxrwxrwx 1 root root 6 Aug  5  2021 /usr/bin/arm-linux-gnueabihf-gcc -> gcc-11

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

# Update pip on PicoMini
It will take about 10 minutes.   
```
$ python3 -m pip install -U pip
```


# Install Adafruit Blinka on PicoMini
It will take about 10 minutes.   
```
$ python3 -m pip install adafruit-blinka
```

# Install Adafruit CircuitPython Wiznet5k on PicoMini
It will take about 10 minutes.   
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
This script will get an IP address from your DHCP and display it.   
```
$ git clone https://github.com/nopnop2002/luckfox-pico-mini-ethernet

$ cd luckfox-pico-mini-ethernet/connect-dhcp

$ sudo -E python3 main.py
eth.ipv4_address=192.168.10.108
```

Python's low-level network interface via the W5500 is now available.   
Details is [here](https://docs.python.org/3.13/library/socket.html).   
[Here](https://realpython.com/python-sockets/) is Programming Guide.   

# Using Adafruit CircuitPython Libraries
[Here](https://learn.adafruit.com/circuitpython-essentials/circuitpython-libraries) is a list of drivers and helper libraries that can be used with Adafruit-Blinka.   
Adafruit-Blinka is a library that assumes Adafruit CircuitPython.   
CircuitPython has specific libraries, such as adafruit_neopixel, adafruit_bmp280, and adafruit_dotstar, which are all aimed at specific hardware.   
These are very powerful libraries that allow you to use your hardware with minimal code.   

The python that runs on Linux is CPython, so some of these drivers and libraries will work correctly with CPython, but some will not work with CPython.   
Some helper libraries cannot even be installed in a CPython environment.   
Details of the python implementation are [here](https://picockpit.com/raspberry-pi/whats-the-difference-between-micropython-circuitpython-cpython-anyway/).   

Some drivers and helper libraries work in the CPython environment.   
![Image](https://github.com/user-attachments/assets/a4977714-540c-42fe-8982-65bbaef524f2)
![Image](https://github.com/user-attachments/assets/7103e491-c949-4b9b-8bf4-5d41f15945a5)


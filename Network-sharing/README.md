# Network sharing using a Linux environment such as Ubuntu/Debian as the host
The behavior of the network interface differs between Ubuntu20.04/22.04/24.04, Debian11/12.

# Ubuntu20.04
When you power the Mini board from an Ubuntu 20.04 machine, the usb0 interface will appear on the Ubuntu side as shown below.
```
$ sudo ifconfig usb0
usb0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::a742:1ab5:c616:d016  prefixlen 64  scopeid 0x20<link>
        ether 7a:da:62:7c:d5:bb  txqueuelen 1000  (Ethernet)
        RX packets 21  bytes 2169 (2.1 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 39  bytes 8001 (8.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ nmcli conn show
NAME        UUID                                  TYPE      DEVICE
Wired connection 2  ea035181-2f58-3f41-bf2b-89c5022bb4e0  ethernet  usb0
Wired connection 1  5bfff474-56e9-3a46-81d7-3b3a7d5692d7  ethernet  enp4s0
```

So, use the nmcli command to assign a fixed IP address (172.32.0.100) to usb0.   
The fixed IP address assigned to Ubuntu can be any address as long as it is in the same segment as the Mini board.   
When buildroot is running on the Mini board, the IP address "172.32.0.93" will be assigned to the USB port on the Mini board.   
When Ubuntu is running on the Mini board, the IP address "172.32.0.70" will be assigned to the USB port on the Mini board.   
When using nmcli, specify the connection name (wired connection 2) rather than the device (usb0).   

```
$ sudo nmcli connection down "Wired connection 2"
$ sudo nmcli connection modify "Wired connection 2" ipv4.addresses "172.32.0.100/16"
$ sudo nmcli connection modify "Wired connection 2" ipv4.method manual
$ sudo nmcli connection up "Wired connection 2"

$ nmcli device show usb0
GENERAL.DEVICE:                         usb0
GENERAL.TYPE:                           ethernet
GENERAL.HWADDR:                         DA:1F:7F:84:10:69
GENERAL.MTU:                            1500
GENERAL.STATE:                          100 (connected)
GENERAL.CONNECTION:                     Wired connection 2
GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/6
WIRED-PROPERTIES.CARRIER:               on
IP4.ADDRESS[1]:                         172.32.0.100/16
IP4.GATEWAY:                            --
IP4.ROUTE[1]:                           dst = 172.32.0.0/16, nh = 0.0.0.0, mt = 101
IP6.ADDRESS[1]:                         fe80::f220:3c47:db11:8fbe/64
IP6.GATEWAY:                            --
IP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 101
```

Now you should be able to ping the Mini board and use ssh and scp.
```
$ ping 173.32.0.93 -c 5
PING 173.32.0.93 (173.32.0.93) 56(84) bytes of data.
64 bytes from 173.32.0.93: icmp_seq=1 ttl=49 time=267 ms
64 bytes from 173.32.0.93: icmp_seq=2 ttl=49 time=272 ms
64 bytes from 173.32.0.93: icmp_seq=3 ttl=49 time=267 ms
64 bytes from 173.32.0.93: icmp_seq=4 ttl=49 time=275 ms
64 bytes from 173.32.0.93: icmp_seq=5 ttl=49 time=270 ms

--- 173.32.0.93 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4007ms
rtt min/avg/max/mdev = 266.740/270.134/275.481/3.283 ms

$ ssh root@172.32.0.93
root@172.32.0.93's password:
[root@luckfox root]$ uname -a
Linux luckfox 5.10.110 #1 Mon Jun 17 20:20:43 JST 2024 armv7l GNU/Linux
[root@luckfox root]$ exit

$ echo "hogehoge" > ssh-test.txt

$ scp ssh-test.txt root@172.32.0.93:/root
root@172.32.0.93's password:
```

# Ubuntu22.04
Even if I power the Mini board from an Ubuntu 22.04 machine, the usb0 interface does not appear on the Ubuntu side.   
In Ubuntu 22.04, the interface names have been changed to a "consistent network device naming method", and the usb0 interface name has been changed to the following name.   
This name uses the MAC address of the RNDIS on the LuckFox side.   
The MAC address of the RNDIS on the LuckFox side changes every time LuckFox is started.   
If you compare the display before and after supplying power to the Mini board, you can see that one interface has been added.   
This is the interface for the RNDIS device provided by LuckFox.   

```
$ sudo ifconfig -a

enx0a1c4376e2be: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::f663:a0a0:a112:c7da  prefixlen 64  scopeid 0x20<link>
        ether 8e:4b:24:87:65:cc  txqueuelen 1000  (Ethernet)
        RX packets 22  bytes 2418 (2.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 82  bytes 17016 (17.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ nmcli conn show
NAME        UUID                                  TYPE      DEVICE
Wired connection 2  3bfa1614-912b-3797-b7bc-53bea6b8217d  ethernet  enx0a1c4376e2be
Wired connection 1  2a8a02a6-1692-3945-ac49-740b257bf467  ethernet  enp25s0
```

Therefore, we will use the nmcli command to assign a fixed IP address (172.32.0.100) to this interface (enx0a1c4376e2be).   
```
$ sudo nmcli connection down "Wired connection 2"
$ sudo nmcli connection modify "Wired connection 2" ipv4.addresses "172.32.0.100/16"
$ sudo nmcli connection modify "Wired connection 2" ipv4.method manual
$ sudo nmcli connection up "Wired connection 2"

$ nmcli device show enx0a1c4376e2be
GENERAL.DEVICE:                         enx0a1c4376e2be
GENERAL.TYPE:                           ethernet
GENERAL.HWADDR:                         0A:1C:43:76:E2:BE
GENERAL.MTU:                            1500
GENERAL.STATE:                          100 (connected)
GENERAL.CONNECTION:                     Wired connection 2
GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/4
WIRED- PROPERTIES.CARRIER:               on
IP4.ADDRESS[1]:                         172.32.0.100/16
IP4.GATEWAY:                            --
IP4.ROUTE[1]:                           dst = 172.32.0.0/16, nh = 0.0.0.0, mt = 101
IP6.ADDRESS[1]:                         fe80::366a:8a1:dc16:eb27/64
IP6.GATEWAY:                            --
IP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 1024
```

Now you should be able to ping the Mini board and use ssh and scp.
```
$ ping 173.32.0.93 -c 5
PING 173.32.0.93 (173.32.0.93) 56(84) bytes of data.
64 bytes from 173.32.0.93: icmp_seq=1 ttl=49 time=267 ms
64 bytes from 173.32.0.93: icmp_seq=2 ttl=49 time=272 ms
64 bytes from 173.32.0.93: icmp_seq=3 ttl=49 time=267 ms
64 bytes from 173.32.0.93: icmp_seq=4 ttl=49 time=275 ms
64 bytes from 173.32.0.93: icmp_seq=5 ttl=49 time=270 ms

--- 173.32.0.93 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4007ms
rtt min/avg/max/mdev = 266.740/270.134/275.481/3.283 ms

$ ssh root@172.32.0.93
root@172.32.0.93's password:
[root@luckfox root]$ uname -a
Linux luckfox 5.10.110 #1 Mon Jun 17 20:20:43 JST 2024 armv7l GNU/Linux
[root@luckfox root]$ exit

$ echo "hogehoge" > ssh-test.txt

$ scp ssh-test.txt root@172.32.0.93:/root
root@172.32.0.93's password:
```

# Ubuntu24.04
Same as Ubuntu22.04.

# Debian11
Same as Ubuntu20.04.

# Debian12
This is a "consistent network device naming method".   
However, We can't find the connection name in nmcli.   
I do not know how to assign a fixed IP address to an interface without a connection name.   
```
$ sudo ifconfig -a

enx9efc2b4d1091: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        ether 9e:fc:2b:4d:10:91  txqueuelen 1000  (Ethernet)
        RX packets 16  bytes 1689 (1.6 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ nmcli conn show
NAME                UUID                                  TYPE      DEVICE
Wired connection 1  595b95eb-a0ab-4949-87b9-2a118e21c5f7  ethernet  enp0s25
lo                  16ee843a-0cce-4a66-abec-bd6572b53956  loopback  lo
```

# Network sharing using Linux host
Since LuckFox is also Linux, we will refer to the host Linux as Ubuntu (even though it is Debian).   
First, check the network interface on the Ubuntu side.   
The top (enp25s0) is the actual interface, and the bottom (enx62ca1d071324) is the USB interface for RNDIS used to connect to LuckFox.   
In other words, we will set it up so that packets received from the bottom (enx62ca1d071324) are forwarded to the top (enp25s0).   
```
$ sudo ifconfig -a
enp25s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.10.128  netmask 255.255.255.0  broadcast 192.168.10.255
        inet6 fe80::dbe2:5971:df3e:2e1  prefixlen 64  scopeid 0x20<link>
        ether fc:61:98:2a:3c:b1  txqueuelen 1000  (Ethernet)
        RX packets 3176  bytes 316441 (316.4 KB)
        RX errors 0  dropped 917  overruns 0  frame 0
        TX packets 1699  bytes 326373 (326.3 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

enx62ca1d071324: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.32.0.100  netmask 255.255.0.0  broadcast 172.32.255.255
        inet6 fe80::b943:52d6:d608:24f3  prefixlen 64  scopeid 0x20<link>
        ether 62:ca:1d:07:13:24  txqueuelen 1000  (Ethernet)
        RX packets 467  bytes 31678 (31.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 322  bytes 47213 (47.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Set up forwarding on the Ubuntu side.   
`This setting will disappear when you start Ubuntu, so you will need to do it again every time you start it.`   
```
$ sudo sysctl net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1

$ sudo iptables -P FORWARD ACCEPT

# Please replace enp25s0 with your environment.
$ sudo iptables -t nat -A POSTROUTING -o enp25s0 -j MASQUERADE
```

Next, set up forwarding on LuckFox and check communication to the outside world.   
This setting will disappear when you start LuckFox, so you will need to do it every time.   
This will allow the network to pass through to the outside world.   
Now you can use apt/pip commands with LuckFox.   
```
$ sudo ip r add default via 172.32.0.100

$ sudo sh -c "echo "nameserver 8.8.8.8" >> /etc/resolv.conf"
nameserver

$ ping www.yahoo.co.jp -c 5
PING edge12.g.yimg.jp (182.22.28.252): 56 data bytes
64 bytes from 182.22.28.252: icmp_seq=0 ttl=54 time=22.667 ms
64 bytes from 182.22.28.252: icmp_seq=1 ttl=54 time=33.339 ms
64 bytes from 182.22.28.252: icmp_seq=2 ttl=54 time=21.401 ms
64 bytes from 182.22.28.252: icmp_seq=3 ttl=54 time=24.123 ms
64 bytes from 182.22.28.252: icmp_seq=4 ttl=54 time=22.296 ms
--- edge12.g.yimg.jp ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max/stddev = 21.401/24.765/33.339/4.376 ms
```

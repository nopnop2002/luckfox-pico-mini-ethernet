# udp-client

- Running udp server on linux
```
$ netcat -ulk 8080
```

- Running udp client
```
$ sudo -E python3 main.py --help
usage: main.py [-h] [--host HOST] [--port PORT]

options:
  -h, --help   show this help message and exit
  --host HOST  tcp host
  --port PORT  udp port


$ sudo -E python3 main.py --host 192.168.10.46
args.port=8080
asc_time=Fri Apr 25 15:50:18 2025
```


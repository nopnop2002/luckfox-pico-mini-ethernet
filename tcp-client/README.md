# tcp-client
TCP client example using python's low-level network interface.   

- Running tcp server on linux host.
```
$ netcat -l 8080 -w 1
```

- Running tcp client on PicoMini
```
$ sudo -E python3 main.py --help
usage: main.py [-h] [--host HOST] [--port PORT]

options:
  -h, --help   show this help message and exit
  --host HOST  tcp host
  --port PORT  tcp port


$ sudo -E python3 main.py --host 192.168.10.46
args.host=192.168.10.46
args.port=8080
```


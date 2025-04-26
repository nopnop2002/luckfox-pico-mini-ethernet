# ntp-client
NTP client example using python's low-level network interface.   

```
$ sudo -E python3 main.py --help
usage: main.py [-h] [--tz TZ]

options:
  -h, --help  show this help message and exit
  --tz TZ     time zone


$ sudo -E python3 main.py --tz 9
args.tz=9
2025-04-26 12:48:40
2025-04-26 21:48:40
```


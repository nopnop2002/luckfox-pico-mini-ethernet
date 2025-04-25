# http-client
HTTP client example using python's low-level network interface.   
This project fetch text from [here](http://wifitest.adafruit.com/testwifi/index.html) and [here](http://httpbin.org/delay/3).   

```
$ sudo -E python3 main.py
Wiznet5k WebClient Test
Chip Version: w5500
MAC Address: ['0xde', '0xad', '0xbe', '0xef', '0xfe', '0xed']
My IP address is: 192.168.10.108
IP lookup adafruit.com: 104.20.39.240
Fetching text from http://wifitest.adafruit.com/testwifi/index.html
----------------------------------------
This is a test of Adafruit WiFi!
If you can read this, its working :)
----------------------------------------

Fetching json from http://httpbin.org/delay/3
----------------------------------------
{'args': {}, 'data': '', 'files': {}, 'form': {}, 'headers': {'Host': 'httpbin.org', 'User-Agent': 'Adafruit CircuitPython', 'X-Amzn-Trace-Id': 'Root=1-680b3816-3341f7823e0f974469f913f4'}, 'origin': '61.211.142.54', 'url': 'http://httpbin.org/delay/3'}
----------------------------------------
Done!
```


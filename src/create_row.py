import urllib.request
import urllib.parse

url = 'http://127.0.0.1:5000/api/rows'

values = {
    'latitude': 43.43,
    'longitude': 45.45,
    'emerg_title': 'NEW_EMERGENCY',
    'emerg_timestamp': '1970-01-01 00:00:00',
    'township': 'MOSCOW',
}

data = urllib.parse.urlencode(values).encode()
req = urllib.request.Request(url=url, data=data)
page_string = urllib.request.urlopen(req).read()
print(page_string)

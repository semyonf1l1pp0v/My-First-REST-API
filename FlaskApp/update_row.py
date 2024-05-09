import urllib.request
import urllib.parse

url = 'http://127.0.0.1:5000/api/rows/11'

values = {
    'new_latitude': 10.00,
    'new_longitude': 10.00,
    'new_emerg_title': 'UPDATED_NEW_EMERGENCY',
    'new_emerg_timestamp': '2000-00-00 00:00:00',
    'new_township': 'ZAZHOPINSK',
}

data = urllib.parse.urlencode(values).encode()
req = urllib.request.Request(url=url, data=data, method='PUT')
page_string = urllib.request.urlopen(req).read()
print(page_string)

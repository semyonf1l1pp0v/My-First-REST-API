import urllib.request
import urllib.parse


url = 'http://127.0.0.1:5000/api/rows/11'


req = urllib.request.Request(url=url, method='DELETE')
page_string = urllib.request.urlopen(req).read()
print(page_string)

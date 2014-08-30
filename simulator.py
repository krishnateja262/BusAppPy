import json
import time
import urllib2

def callBusser(lat, lon):
	url = "http://dev.truzign.com/BusApp-1.0-SNAPSHOT/routes/SS-28"
	data = {"lat":lat, "lon":lon, "sendNotification":True}
	data = json.dumps(data)
	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	response = f.read()
	print(response)
	f.close()
	if "INFO" in response:
		return True
	else:
		return False

f = open('tbmsez.json', 'r')
data = json.load(f)
f.close()
# selecting route SS-28 because the coordinates are choosen for those


for coordinate in data['coordinates']:
	print("________")
	if not callBusser(str(coordinate['lat']), str(coordinate['lon'])):
		print("did not work for : " + str(coordinate['lat']))
	time.sleep(60)

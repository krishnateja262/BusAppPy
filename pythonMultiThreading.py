import threading
import time
import json
import urllib2


def connect(url):
	f = urllib2.urlopen(url)
	response = f.read()
	f.close()
	return response

def connectTo(num):
	url = "http://dev.truzign.com/BusApp-1.0-SNAPSHOT/timing/"+str(num)
	return connect(url)

def checkRoutePushActivation(routeNumber):
	url = "http://dev.truzign.com/BusApp-1.0-SNAPSHOT/notifiers/"+routeNumber
	jsonResponse = json.loads(connect(url))
	if jsonResponse['status'] == 'INFO':
		return True
	else:
		return False


def notifyUser(passenger, gcmId, lat, lon):
	data = {"passenger": passenger, "gcmId": gcmId, "lat": lat, "lon": lon}
	data = json.dumps(data)

	url = "http://localhost:8080/notify"

	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})

	f = urllib2.urlopen(req)
	response = f.read()
	f.close()
	print(response)


def sendNotification(passenger, gcmId , routeNumber):
	url = "http://dev.truzign.com/BusApp-1.0-SNAPSHOT/routes/"+routeNumber
	jsonResponse = json.loads(connect(url))
	lat = jsonResponse['driverPositionBean']['lat']
	lon = jsonResponse['driverPositionBean']['lon']
	notifyUser(passenger, gcmId, lat, lon)
	print("sending notifications to Passenger:%s whose GCMId: %s with coordinates : %s,%s" % (passenger, gcmId, lat, lon))

def parseAndSendNotifications(jsonResponse):
	for passenger in jsonResponse:
		gcmId = jsonResponse[passenger]['gcmId']
		routeNumber = jsonResponse[passenger]['routeNumber']
		if checkRoutePushActivation(routeNumber):
			#print(passenger+":"+gcmId+":"+routeNumber)
			sendNotification(passenger, gcmId , routeNumber)

def worker(num):
    """thread worker function"""
    while(True):
    	response = connectTo(num)
    	jsonResponse = json.loads(response)
    	if len(jsonResponse)>0:
    		print(num)
    		parseAndSendNotifications(jsonResponse)
    	#print(str(len(jsonResponse))+" : "+str(num)+' : Worker: %s' % response)
    	time.sleep(num*60)
    return

threads = []
for i in range(1,5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
from bottle import route, run, request
import json
import urllib2


def callGoogle(passenger, gcmId, lat, lon):
	s = str(lat)+":"+str(lon)
	print(s)
	data = {"data":{"message": s},"registration_ids":[gcmId]}
	data = json.dumps(data)

	url = "https://android.googleapis.com/gcm/send"

	req = urllib2.Request(url, data, {'Content-Type': 'application/json','Authorization':'key={your key}'})

	f = urllib2.urlopen(req)
	response = f.read()
	f.close()
	print(response)

@route('/notify', method = 'POST')
def notifyUser():
	callGoogle(request.json['passenger'],request.json['gcmId'],request.json['lat'],request.json['lon'])
	return {"status":"Success"}

run(host='localhost', port=8080, debug=True)
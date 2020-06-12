import sys
import json
import requests

start = sys.argv[1]
end = sys.argv[2]
key = sys.argv[3]

start = start.split(",")
end = end.split(",")
start.reverse()
end.reverse()

revstart = "" + start[0] + "," + start[1]
revend = "" + end[0] + "," + end[1]

url = 'https://api.mapbox.com/directions/v5/mapbox/driving/'
r = requests.get(url + revstart + ';' + revend + '?geometries=geojson&access_token=' + key)
y = r.json()


distance = y['routes'][0]['distance']

time = y['routes'][0]['duration']

resp = {
    "Response":200,
    "distance":distance,
    "time":time
}

print(json.dumps(resp))

sys.stdout.flush()

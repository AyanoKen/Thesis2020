import sys
import json
import requests

center = sys.argv[1]
radius = int(sys.argv[2])
service = (sys.argv[3]).lower()
key = sys.argv[4]

center = center.split(",")

url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'

proximity = center[1] + "," + center[0]

minlong = float(center[1]) - radius/100.0
minlat = float(center[0]) - radius/100.0
maxlong = float(center[1]) + radius/100.0
maxlat = float(center[0]) + radius/100.0

r = requests.get(url + service + '.json?bbox=' + str(minlong) +','+ str(minlat) +','+ str(maxlong) +','+ str(maxlat) + '&access_token=' + key)

x = r.json()

coordinates = center[1] + "," + center[0] + ";"

url2 = 'https://api.mapbox.com/directions/v5/mapbox/driving/'

for i in x["features"]:
    r2 = requests.get(url2 + proximity + ';' + str(i["center"][0]) + "," + str(i["center"][1]) + '?geometries=geojson&access_token=' + key)
    y = r2.json()
    distance = int(y['routes'][0]['distance'])

    if distance < radius * 1000:
        coordinates = coordinates + str(i["center"][0]) + "," + str(i["center"][1]) + ";"

# for i in x["features"]:
#     coordinates = coordinates + str(i["center"][0]) + "," + str(i["center"][1]) + ";"

coordinates = coordinates[:-1]

resp = {
    "Response":200,
    "total": len((coordinates).split(";")),
    "coordinates": coordinates
}

print(json.dumps(resp))

sys.stdout.flush()

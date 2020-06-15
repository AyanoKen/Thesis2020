import sys
import json
import requests

central = sys.argv[1]
radius = float(sys.argv[2])
service = (sys.argv[3]).lower()
key = sys.argv[4]

central = central.split(",")

url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'

invertedCentral = central[1] + "," + central[0]
coordinateList = [invertedCentral]

addressList = []

increments = 2

if radius <= 3:
    minlong = float(central[1]) - radius/100.0
    minlat = float(central[0]) - radius/100.0
    maxlong = float(central[1]) + radius/100.0
    maxlat = float(central[0]) + radius/100.0
    r = requests.get(url + service + '.json?bbox=' + str(minlong) +','+ str(minlat) +','+ str(maxlong) +','+ str(maxlat) + '&access_token=' + key)

    x = r.json()
    url2 = 'https://api.mapbox.com/directions/v5/mapbox/driving/'

    for i in x["features"]:
        r2 = requests.get(url2 + invertedCentral + ';' + str(i["center"][0]) + "," + str(i["center"][1]) + '?geometries=geojson&access_token=' + key)
        y = r2.json()
        distance = int(y['routes'][0]['distance'])

        if distance < radius * 1000:
            coordinateList.append(str(i["center"][0]) + "," + str(i["center"][1]))
            addressList.append(i["place_name"])
else:
    currentRad = increments
    while currentRad <= radius:
        minlong = float(central[1]) - currentRad/100.0
        minlat = float(central[0]) - currentRad/100.0
        maxlong = float(central[1]) + currentRad/100.0
        maxlat = float(central[0]) + currentRad/100.0

        r = requests.get(url + service + '.json?bbox=' + str(minlong) +','+ str(minlat) +','+ str(maxlong) +','+ str(maxlat) + '&access_token=' + key)

        x = r.json()
        url2 = 'https://api.mapbox.com/directions/v5/mapbox/driving/'

        for i in x["features"]:
            if str(i["center"][0]) + "," + str(i["center"][1]) not in coordinateList:
                r2 = requests.get(url2 + invertedCentral + ';' + str(i["center"][0]) + "," + str(i["center"][1]) + '?geometries=geojson&access_token=' + key)
                y = r2.json()
                distance = int(y['routes'][0]['distance'])

                if distance < radius * 1000:
                    coordinateList.append(str(i["center"][0]) + "," + str(i["center"][1]))
                    addressList.append(i["place_name"])

        if currentRad == radius:
            currentRad = radius + 1
        else:
            if currentRad + increments > radius:
                currentRad = radius
            else:
                currentRad += increments

coordinates = ";".join(coordinateList)

resp = {
    "Response":200,
    "total": len(coordinateList),
    "coordinates": coordinates,
    "addresses": addressList
}

print(json.dumps(resp))

sys.stdout.flush()

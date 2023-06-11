import urllib.request
import json

# Your Bing Maps Key
bingMapsKey = "AiGA41BLOBd4YOM8RLBkgIMSD4ic99CKEF2A5xZyFXA6l6vvNli-3MDaisLf5kVl&callback=loadMapScenario"

# input information
longitude = -122.019943
latitude = 37.285989
destination = "1427 Alderbrook Ln San Jose CA 95129"

encodedDest = urllib.parse.quote(destination, safe='')

routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(latitude) + "," + str(longitude) + "&wp.1=" + encodedDest + "&key=" + bingMapsKey

request = urllib.request.Request(routeUrl)
response = urllib.request.urlopen(request)

r = response.read().decode(encoding="utf-8")
result = json.loads(r)

itineraryItems = result["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]

for item in itineraryItems:
    print(item["instruction"]["text"])
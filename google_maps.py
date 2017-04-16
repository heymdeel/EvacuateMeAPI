import urllib.request
import json


def make_request_to_google(lat, lon, dest_lat, dest_lon):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations={2},{3}&key={4}'\
        .format(str(lat), str(lon), str(dest_lat), str(dest_lon), 'AIzaSyCiGqVbAL5HBIqlbAmL8gCWNg7LtgaMh9Q')
    return urllib.request.urlopen(url).read().decode('utf8')


def get_duration(response):
    obj = json.loads(response)
    return obj['rows'][0]['elements'][0]['duration']['text']


def get_distance(response):
    obj = json.loads(response)
    return obj['rows'][0]['elements'][0]['distance']['value']

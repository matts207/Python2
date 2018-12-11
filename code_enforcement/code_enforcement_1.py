import requests
from datetime import datetime, timedelta
import pprint
from bs4 import BeautifulSoup


google_directions_api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={O}&destination={D}&waypoints=optimize:true|{W}&key={K}'


directions_key = 'AIzaSyAYixVeTbunLmxgrk3TcVrUE9sWhGY64bI'


pp = pprint.PrettyPrinter(indent=2)

o = "207 Peak Dr. 15090"

locations = {"1000 Ross Park Mall Dr, Pittsburgh, PA 15237": ['None', '120'],
            '1750 Clairton Rd, West Mifflin, PA 15122': ['None', '120'],
            '|144 Ashley Hill Dr. 15090': ['None', '120'],
            '125 Monroeville Ave, Turtle Creek, PA 15145': ['None', '160']}
# Dict that will eventually have weather or not there is a set time and
# the estimated time needed at each destination


list_of_stops = ["Pittsburgh, PA", "CCAC South"]
waypoints = ''

for key, val in locations.items():
    if val[0] == 'None':
        waypoints += key
        waypoints += '|'
# Sets up the waypoints in correct format from locations dict.


stops_w_set_times = {"8701 Perry Hwy, Pittsburgh, PA 15237": 1543357287}


stops = {}


def routing(api, key, origin, destination, waypoints):
    new_url = api.replace('{O}', origin).replace('{D}', destination).replace("{W}", waypoints).replace("{K}", key)
    request = requests.get(new_url).json()

    for leg in request['routes'][0]['legs']:
        for step in leg['steps']:
            soup = BeautifulSoup(step['html_instructions'], features="html.parser")
            print(soup.text + '\n' + format("%s.\n" % step['distance']['text']))
            # Makes the html directions readable
        print('\n\n')
    print('New Waypoint Order %s\n\n' % request['routes'][0]['waypoint_order'])
    # pp.pprint(request)
'''routing function takes in the api url, the api key, the desired origin,
the destination (that for now is the same as the origin) and the addresses of the 
waypoints.  It assembles the correct url for the api call, requests it, and 
prints out the step by step directions for each leg of the route.  '''

routing(google_directions_api_url, directions_key, o, o, waypoints)



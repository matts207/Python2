import requests, json
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
address_file = 'addresses.json'


def address_formatting():
    number = input("Enter the address number:\n")
    st_name = input("Enter the street name. Ex: \'First St.\':\n")
    city = input("Enter the city:\n")
    state = input("Enter the 2-letter state abbreviation:\n")
    zipcode = input("Enter the 5 number zip-code:\n")
    return format("%s %s %s, %s, %s" % (number, st_name, city, state, zipcode))


def check_origin(json_file):
    with open(json_file, 'r') as file:
        address_list = json.load(file)
    print(address_list)
    answer = input("Is %s your starting address?\nY/N:" % address_list['origin'])
    while answer.upper() != 'Y' and answer.upper() != 'N':
        answer = input("Try again.\nIs %s your starting address?\nEnter Y or N:" % address_list['origin'])
    if answer.upper() == 'N':
        address_list['origin'] = address_formatting()
    with open(json_file, 'w') as f:
        json.dump(address_list, f)


def set_addresses(json_file):
    with open(json_file, 'r') as file:
        address_list = json.load(file)
    loop_bool = True
    while loop_bool:
        time = "None"
        print("Enter your addresses:")
        address = address_formatting()
        set_time_yn = input("Does this address have a set time?\nEnter Y/N:\n")
        while set_time_yn.upper() != 'Y' and set_time_yn.upper() != 'N':
            set_time_yn = input("Try again.\nDoes this address have a set time?\nEnter Y or N:\n")
        if set_time_yn.upper() == 'Y':
            hours = input("Enter the hour of the arrival time:\n")
            minutes = input("Enter the minutes of the arrival time\n")
            time = format("%s:%s" % (hours, minutes))
        estimated_visit_time = int(input("In minutes, how long do you think this stop will take?")) * 60
        address_list['addresses'][address] = [time, estimated_visit_time]
        another_address = input("Would you like to add another address?\nEnter Y/N:\n")
        while another_address.upper() != 'Y' and another_address.upper() != 'N':
            another_address = input("Try again.\nWould you like to add another address?\nEnter Y or N:")
        if another_address.upper() == 'N':
            loop_bool = False
    with open(json_file, 'w') as f:
        json.dump(address_list, f)


def view_addresses():
    pass


def routing(api, key, origin, waypoints):
    new_url = api.replace('{O}', origin).replace('{D}', origin).replace("{W}", waypoints).replace("{K}", key)
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

# routing(google_directions_api_url, directions_key, o, waypoints)

check_origin(address_file)
set_addresses(address_file)
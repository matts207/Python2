import requests, json
from bs4 import BeautifulSoup


google_directions_api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={O}&destination={D}&waypoints=optimize:true|{W}&key={K}'

directions_key = 'AIzaSyAYixVeTbunLmxgrk3TcVrUE9sWhGY64bI'

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
        estimated_visit_time = int(input("In minutes, how long do you think this stop will take?\n")) * 60
        address_list['addresses'][address] = [time, estimated_visit_time]
        another_address = input("Would you like to add another address?\nEnter Y/N:\n")
        while another_address.upper() != 'Y' and another_address.upper() != 'N':
            another_address = input("Try again.\nWould you like to add another address?\nEnter Y or N:")
        if another_address.upper() == 'N':
            loop_bool = False
    with open(json_file, 'w') as f:
        json.dump(address_list, f)


def view_addresses(json_file):
    with open(json_file, 'r') as file:
        addresses = json.load(file)
        print("Your starting address is %s.\nAddress List:" % addresses['origin'])
        for address, info in addresses['addresses'].items():
            print("%s:\n\tSet Arrival Time: %s\n\tEstimated Job Time: %s" % (address, info[0], info[1]))


def edit_addresses(json_file):
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    for address, info in addresses['addresses'].items():
        print(address)
        print("\tSet Time: %s\n\tEstimated Job Time: %s" % (info[0], info[1]))
    address_to_change = input("Enter the address you'd like to change.")
    while address_to_change not in addresses['addresses'].keys():
        address_to_change = input("Address not found.  Try Again.  \nEnter the address you'd like to change.")
    changes = address_formatting()
    addresses['addresses'][changes] = addresses['addresses'].pop(address_to_change)
    set_time_yn = input("Does this address have a set time?\nEnter Y/N:\n")
    time = 'None'
    while set_time_yn.upper() != 'Y' and set_time_yn.upper() != 'N':
        set_time_yn = input("Try again.\nDoes this address have a set time?\nEnter Y or N:\n")
    if set_time_yn.upper() == 'Y':
        hours = input("Enter the hour of the arrival time:\n")
        minutes = input("Enter the minutes of the arrival time\n")
        time = format("%s:%s" % (hours, minutes))
    estimated_visit_time = int(input("In minutes, how long do you think this stop will take?\n")) * 60
    addresses['addresses'][changes] = [time, estimated_visit_time]
    with open(json_file, 'w') as file:
        json.dump(addresses, file)


def clear_addresses(json_file):
    pass


def get_origin(json_file):
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    return addresses['origin']

def get_addresses(json_file):
    with open(json_file,'r') as file:
        addresses = json.load(file)
    waypoints = ''
    for key in addresses['addresses'].keys():
        waypoints += key
        waypoints += '|'
    return waypoints


def routing(api, key):
    new_url = api.replace('{O}', get_origin(address_file)).replace('{D}', get_origin(address_file))
    new_url = new_url.replace("{W}", get_addresses(address_file)).replace("{K}", key)
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


view_addresses(address_file)
set_addresses(address_file)

routing(google_directions_api_url, directions_key)
# clear_addresses(address_file)
# edit_addresses(address_file)
# check_origin(address_file)

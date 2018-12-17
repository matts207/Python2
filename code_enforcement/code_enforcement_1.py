import requests
import json
from bs4 import BeautifulSoup

google_directions_api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&waypoints=optimize:true{}&key={}'

directions_key = 'AIzaSyAYixVeTbunLmxgrk3TcVrUE9sWhGY64bI'

address_file = 'addresses.json'


def address_formatting():
    number = input("Enter the address number:\n")
    st_name = input("Enter the street name. Ex: \'First St.\':\n")
    city = input("Enter the city:\n")
    state = input("Enter the 2-letter state abbreviation:\n")
    zipcode = input("Enter the 5 number zip-code:\n")
    return f"{number} {st_name} {city}, {state}, {zipcode}"


def check_origin(json_file):
    with open(json_file, 'r') as file:
        address_list = json.load(file)
    print(address_list)
    answer = input(f"Is {address_list['origin']} your starting address?\nEnter Y or N:")
    while answer.upper() != 'Y' and answer.upper() != 'N':
        answer = input(f"Try again.\nIs {address_list['origin']} your starting address?\nEnter Y or N:")
    if answer.upper() == 'N':
        address_list['origin'] = address_formatting()
        print(address_list)
    with open(json_file, 'w') as f:
        json.dump(address_list, f)


def set_addresses(json_file):
    with open(json_file, 'r') as file:
        address_list = json.load(file)
    address_list['addresses'] = {}
    loop_bool = True
    print("Enter your addresses:")
    while loop_bool:
        time = "None"
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
        print(f"Your starting address is {addresses['origin']}.\nAddress List:")
        for address, info in addresses['addresses'].items():
            print(f"{address}:\n\tSet Arrival Time: {info[0]}\n\tEstimated Job Time: {info[1]}")


def edit_addresses(json_file):
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    for address, info in addresses['addresses'].items():
        print(address)
        print(f"\tSet Time: {info[0]}\n\tEstimated Job Time: {info[1]}")
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
    with open(json_file, 'r') as file:
        address_list = json.load(file)
    address_list['addresses'] = {}
    with open(json_file, 'w') as file:
        json.dump(address_list, file)


def get_origin(json_file):
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    return addresses['origin']


def get_addresses(json_file):
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    waypoints = ''
    for key in addresses['addresses'].keys():
        waypoints += '|'
        waypoints += key
    return waypoints


def routing(api, key):
    """The arguments are the api url and the api key.
    This calls the get_origin and the get_address functions,
    formats the api url, calls the api, and outputs the step-by-step
    directions to each destination on the route in the new optimized order."""

    origin = get_origin(address_file)
    waypoints = get_addresses(address_file)
    try:
        request = requests.get(api.format(origin, origin, waypoints, key)).json()

        for leg in request['routes'][0]['legs']:
            print("\n")
            for step in leg['steps']:
                soup = BeautifulSoup(step['html_instructions'], features="html.parser")
                print(soup.text + '\n' + f"{step['distance']['text']}\n")
                # Makes the html directions readable
        print(f"\nOptimized Route Order: {request['routes'][0]['waypoint_order']}")
    except:
        print("Error.  Please check connection.")

# check_origin(address_file)
# set_addresses(address_file)
view_addresses(address_file)
routing(google_directions_api_url, directions_key)
# clear_addresses(address_file)

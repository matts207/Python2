import requests
import json
from bs4 import BeautifulSoup
from pprint import PrettyPrinter
from datetime import date
import time
from itertools import combinations

pp = PrettyPrinter()

google_directions_api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&waypoints=optimize:true|{}&key={}'

google_directions_api_url_wo_wps = 'https://maps.googleapis.com/maps/api/directions/json?origin={O}&destination={D}&key={K}'

directions_key = 'AIzaSyAYixVeTbunLmxgrk3TcVrUE9sWhGY64bI'

route_data = 'addresses.json'


def address_formatting():
    # Returns correctly formatted address inputs
    number = input("Enter the address number:\n")
    st_name = input("Enter the street name. Ex: \'First St.\':\n")
    city = input("Enter the city:\n")
    state = input("Enter the 2-letter state abbreviation:\n")
    zipcode = input("Enter the 5 number zip-code:\n")
    return f"{number} {st_name} {city}, {state} {zipcode}"


def check_origin(json_file):
    """Checks if the saved starting address is correct.
    Opens the addresses JSON file, prompts user to see if the
    current origin is correct, if not it calls address_formatting
    to get the new address and saves it as the origin."""

    with open(json_file, 'r') as file:
        address_list = json.load(file)
    answer = input(f"Is your starting address {address_list['origin']}?\nEnter Y or N:\n").upper()
    while answer != 'Y' and answer != 'N':
        answer = input(f"Try again.\nIs {address_list['origin']} your starting address?\nEnter Y or N:\n").upper()
    if answer == 'N':
        address_list['origin'] = address_formatting()
    with open(json_file, 'w') as file:
        json.dump(address_list, file)


def clear_addresses(json_file):
    # Clears the list of addresses
    with open(json_file, 'r') as file:
        address_list = json.load(file)
    address_list['addresses'] = {}
    with open(json_file, 'w') as file:
        json.dump(address_list, file)


def time_formatting(hours, minutes):
    d = str(date.today()).split('-')
    for i in range(len(d)):
        d[i] = int(d[i])
    d.append(hours)
    d.append(minutes)
    d.append(0)
    d.append(0)
    d.append(0)
    d.append(0)

    return time.mktime(tuple(d))


def set_addresses(json_file):
    """Sets the address waypoints and stores them in the JSON file.
    Allows user to set as many addresses as they'd like.  For each one it calls
    address_formatting to ensure they are properly formatted and saves the returned
    string.  Also gets set time and estimated job time info and saves as a list as the
    key for each address."""
    clear_addresses(json_file)
    with open(json_file, 'r') as file:
        address_list = json.load(file)
    loop_bool = True
    print("\nEnter the addresses for the route:")
    while loop_bool:
        time = "None"
        address = address_formatting()
        set_time_yn = input("Does this address have a set time?\nEnter Y/N:\n").upper()
        while set_time_yn != 'Y' and set_time_yn != 'N':
            set_time_yn = input("Try again.\nDoes this address have a set time?\nEnter Y or N:\n").upper()
        if set_time_yn == 'Y':
            while True:
                try:
                    hours = int(input("Enter the hour of the arrival time:\n"))
                    minutes = int(input("Enter the minutes of the arrival time\n"))
                    am_pm = input("AM or PM?\n").upper()
                    while am_pm != 'AM' and am_pm != 'PM':
                        am_pm = input("Please enter AM or PM?\n").upper()
                    if am_pm == 'PM' and hours < 12:
                        hours += 12
                    break
                except ValueError:
                    print("Please Try Again:")
            time = time_formatting(hours, minutes)
        while True:
            try:
                estimated_visit_time = int(input("In minutes, how long do you think this stop will take?\n")) * 60
                break
            except ValueError:
                print("Please Try Again:")

        address_list['addresses'][address] = [time, estimated_visit_time]
        another_address = input("Would you like to add another address?\nEnter Y/N:\n")
        while another_address.upper() != 'Y' and another_address.upper() != 'N':
            another_address = input("Try again.\nWould you like to add another address?\nEnter Y or N:")
        if another_address.upper() == 'N':
            loop_bool = False
    with open(json_file, 'w') as f:
        json.dump(address_list, f)


def view_addresses(json_file):
    # Displays the list of addresses
    with open(json_file, 'r') as file:
        addresses = json.load(file)
        print(f"Your starting address is {addresses['origin']}.\nAddress List:")
        for address, info in addresses['addresses'].items():
            print(f"{address}:\n\tSet Arrival Time: {info[0]}\n\tEstimated Job Time: {info[1]}")


def edit_addresses(json_file):
    # Allows editing of the saved addresses
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    for address, info in addresses['addresses'].items():
        print(address)
        print(f"\tSet Time: {info[0]}\n\tEstimated Job Time: {info[1]}")
    address_to_change = input("Enter the address you'd like to change.\n")
    while address_to_change not in addresses['addresses'].keys():
        address_to_change = input("Address not found.  Try Again.  \nEnter the address you'd like to change.")
    changes = address_formatting()
    addresses['addresses'][changes] = addresses['addresses'].pop(address_to_change)
    time = 'None'
    set_time_yn = input("Does this address have a set time?\nEnter Y/N:\n")
    while set_time_yn.upper() != 'Y' and set_time_yn.upper() != 'N':
        set_time_yn = input("Try again.\nDoes this address have a set time?\nEnter Y or N:\n")
    if set_time_yn.upper() == 'Y':
        while True:
            try:
                hours = int(input("Enter the hour of the arrival time:\n"))
                minutes = int(input("Enter the minutes of the arrival time\n"))
                am_pm = input("AM or PM?\n").upper()
                while am_pm != 'AM' and am_pm != 'PM':
                    am_pm = input("Please enter AM or PM?\n").upper()
                if am_pm == 'PM' and hours < 12:
                    hours += 12
                time = time_formatting(hours, minutes)
                break
            except ValueError:
                print("Please Try Again:")
        while True:
            try:
                estimated_visit_time = int(input("In minutes, how long do you think this stop will take?\n")) * 60
                break
            except ValueError:
                print("Please Try Again:")
    addresses['addresses'][changes] = [time, estimated_visit_time]
    with open(json_file, 'w') as file:
        json.dump(addresses, file)


def get_origin(json_file):
    # Gets the saved origin from the JSON file
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    return addresses['origin']


def get_addresses(json_file):
    # Gets the saved addresses from the JSON file
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    waypoints = ''
    for key in addresses['addresses'].keys():
        waypoints += '|'
        waypoints += key
    return waypoints


def routing(api, key, origin, destination, waypoints):
    """The arguments are the api url and the api key.
    This calls the get_origin and the get_address functions,
    formats the api url, calls the api, and outputs the step-by-step
    directions to each destination on the route in the new optimized order."""
    if waypoints != '':
        try:
            request = requests.get(api.format(origin, destination, waypoints, key)).json()
            for leg in request['routes'][0]['legs']:
                print("\n")
                for step in leg['steps']:
                    soup = BeautifulSoup(step['html_instructions'], features="html.parser")
                    print(soup.text + '\n' + f"{step['distance']['text']}\n")
                    # Makes the html directions readable
            print(f"\nOptimized Route Order: {request['routes'][0]['waypoint_order']}")
        except:
            print("Error.  Please check connection.")
        # Exception handling is to prevent issues in case of no internet connection.
    else:
        api = api.replace('waypoints=optimize:true|{}', '')
        try:
            request = requests.get(api.format(origin, destination, key)).json()
            for leg in request['routes'][0]['legs']:
                print("\n")
                for step in leg['steps']:
                    soup = BeautifulSoup(step['html_instructions'], features="html.parser")
                    print(soup.text + '\n' + f"{step['distance']['text']}\n")
                    # Makes the html directions readable
            print(f"\nOptimized Route Order: {request['routes'][0]['waypoint_order']}")
        except:
            print("Error.  Please check connection.")


def one_set_time(api, key, points_with_times, points_without_times, origin):
    starting_time = round(time.time())
    for k, v in points_with_times.items():
        set_time_address = str(k)
        set_time = float(v[0])
    time_left = set_time - starting_time
    print(time_left)
    waypoints = ''
    waypoint_total_time = 0
    for address in points_without_times.keys():
        waypoints += '|' + address
        waypoint_total_time += int(points_without_times[address][1])
    request_all = requests.get(api.format(origin, set_time_address, waypoints, key)).json()
    for leg in request_all['routes'][0]['legs']:
        waypoint_total_time += leg['duration']['value']
    if waypoint_total_time < time_left:
        routing(api, key, origin, set_time_address, waypoints)
        waypoints = ''
        routing(api, key, set_time_address, origin, waypoints)
    else:
        combos = []
        '''for num_in_combos in range(1, len(points_without_times)):
            combos += combinations(points_without_times, num_in_combos)'''
        for num_in_combos in range(1, len(points_without_times)):
            for com in combinations(points_without_times, num_in_combos):
                d = {x:[points_without_times[x], num_in_combos] for x in com}
                combos.append(d)
        combos = combos[::-1]
        pp.pprint(combos)
        best_choice = []
        addresses_after = []
        for combo in combos:
            wp = '|'.join('{}'.format(waypoint) for waypoint in combo.keys())
            wp_time = 0
            for com in combo.values():
                wp_time += com[0][1]
            if best_choice:
                #####################################################
                #   start working here   #
                if len(best_choice[0]) > com[0][1]:
                    break
                    print("broke")
            r = requests.get(api.format(origin, set_time_address, wp, key)).json()
            for leg in r['routes'][0]['legs']:
                wp_time += leg['duration']['value']
            if wp_time < time_left:
                if not best_choice:
                    best_choice = [list(combo.keys()), wp_time, num_in_combos]
                elif best_choice[1] < wp_time and len(combo) >= len(best_choice[0]):
                    best_choice = [list(combo.keys()), wp_time, num_in_combos]
        print(best_choice)
        if not best_choice:
            wp = '|'.join('{}'.format(waypoint) for waypoint in points_without_times.keys())
            w = ''
            routing(api, key, origin, set_time_address, w)
            routing(api, key, set_time_address, origin, wp)
        else:
            for a in points_without_times:
                if a not in best_choice[0]:
                    addresses_after.append(a)
            waypoints = '|'.join('{}'.format(waypoint) for waypoint in best_choice[0])
            wps_after = '|'.join('{}'.format(waypoint) for waypoint in addresses_after)
            routing(api, key, origin, set_time_address, waypoints)
            routing(api, key, set_time_address, origin, wps_after)


def two_set_times(api, key, points_with_times, points_without_times, origin):
    starting_time = round(time.time())
    set_time_points = []
    for k, v in points_with_times.items():
        set_time_points.append((k, float(v[0]), v[1]))
    set_time_points.sort(key=lambda x: x[1])
    print(set_time_points)
    time_before_stop1 = set_time_points[0][1] - starting_time
    time_between_1and2 = set_time_points[1][1] - set_time_points[0][1]
    print(time_before_stop1)
    print(time_between_1and2)
    waypoints = '|'.join('{}'.format(address) for address in points_without_times.keys())
    req = requests.get(api.format(origin, set_time_points[0], waypoints, key)).json()
    print(req)
    wp_total_time = 0
    print(points_without_times)
    for point in points_without_times.values():
        wp_total_time += point[1]
    print(wp_total_time)
    for leg in req['routes'][0]['legs']:
        wp_total_time += leg['duration']['value']
    print(wp_total_time)
    if wp_total_time < time_before_stop1:
        routing(api, key, origin, set_time_points[0][0], waypoints)
        waypoints = ''
        routing(api, key, set_time_points[0][0], set_time_points[1][0], waypoints)
        routing(api, key, set_time_points[1][0], origin, waypoints)
    else:
        combos = []
        for num_in_combos in range(1, len(points_without_times)):
            for com in combinations(points_without_times, num_in_combos):
                d = {x:points_without_times[x] for x in com}
                combos.append(d)
        combos = combos[::-1]
        pp.pprint(combos)
        best_choice = []
        addresses_left = []
        for combo in combos:
            wp = '|'.join('{}'.format(waypoint) for waypoint in combo.keys())
            wp_time = 0
            r = requests.get(api.format(origin, set_time_points[0][0], wp, key)).json()
            for leg in r['routes'][0]['legs']:
                wp_time += leg['duration']['value']
            if wp_time < time_before_stop1:
                if not best_choice:
                    best_choice = [combo, wp_time]
                elif best_choice[1] < wp_time and len(combo) >= len(best_choice[0]):
                    best_choice = [combo, wp_time]
        wp1 = ''
        if best_choice:
            wp1 = '|'.join('{}'.format(address) for address in best_choice[0])
            for a in points_without_times.keys():
                if a not in best_choice[0]:
                    addresses_left.append({a: points_without_times[a]})
        print(addresses_left)
        print(time_between_1and2)
        combos = []
        for num_in_combos in range(1, len(addresses_left)):
            for com in combinations(addresses_left, num_in_combos):
                d = {x:addresses_left[x] for x in com}
                combos.append(d)
        pp.pprint(combos)
        if not combos:
            api_1 = api.format(set_time_points[0][0], set_time_points[1][0], addresses_left, key)
            r = requests.get(api_1).json()
            if r['routes'][0]['legs'][0]['duration']['value'] < time_between_1and2:
                routing(api, key, origin, set_time_points[0][0], wp1)
                routing(api, key, set_time_points[0][0], set_time_points[1][0], addresses_left)
                waypoints = ''
                routing(api, key, set_time_points[1][0], origin, waypoints)
            else:
                routing(api, key, origin, set_time_points[0][0], wp1)
                waypoints = ''
                routing(api, key, set_time_points[0][0], set_time_points[1][0], waypoints)
                routing(api, key, set_time_points[1][0], origin, addresses_left)
        else:
            pass


def setting_route(api, key, json_file):
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    points_without_times = {}
    points_with_times = {}
    origin = get_origin(json_file)
    for address in addresses['addresses'].keys():
        if addresses['addresses'][address][0] == "None":
            points_without_times[address] = addresses['addresses'][address]
        else:
            points_with_times[address] = addresses['addresses'][address]
    if len(points_with_times) == 0:
        waypoints = '|'.join('{}'.format(address) for address in points_without_times.keys())
        routing(api, key, origin, origin, waypoints)
    else:
        if len(points_with_times) == 1:
            one_set_time(api, key, points_with_times, points_without_times, origin)
        elif len(points_with_times) == 2:
            two_set_times(api, key, points_with_times, points_without_times, origin)

# check_origin(route_data)
# set_addresses(route_data)
# edit_addresses(route_data)
view_addresses(route_data)
setting_route(google_directions_api_url, directions_key, route_data)


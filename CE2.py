import requests
import json
from bs4 import BeautifulSoup
from datetime import date
from pprint import PrettyPrinter
import time
from itertools import combinations

pp = PrettyPrinter()

google_directions_api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&waypoints=optimize:true|{}&key={}'

google_directions_api_url_wo_wps = 'https://maps.googleapis.com/maps/api/directions/json?origin={O}&destination={D}&key={K}'

directions_key = 'AIzaSyAYixVeTbunLmxgrk3TcVrUE9sWhGY64bI'

route_data = 'addresses.json'

s_time = time.time()


h_file = 'testing.html'


def mapping(h_file, key, o, w, directions):
    message = """<!DOCTYPE html>
    <html>
    <body>
    <div align=left>
    <h1>Map Testing</h1>
    <iframe
        width="600"
        height="450"
        frameborder="0" style="border:0"
        src="https://www.google.com/maps/embed/v1/directions?key={}&origin={}&destination={}&waypoints={}" allowfullscreen>
    </iframe>
    </div><div>
    {}
    </body>
    </html>""".format(key, o, o, w, directions)

    with open(h_file,"w") as page:
        page.write(message)


def address_formatting():
    # Returns correctly formatted address inputs
    number = input("Enter the address number:\n")
    st_name = input("Enter the street name. Ex: \'First St.\':\n")
    city = input("Enter the city:\n")
    state = input("Enter the 2-letter state abbreviation:\n")
    zipcode = input("Enter the 5 number zip-code:\n")
    return "%s %s %s, %s %s" % (number, st_name, city, state, zipcode)


def check_origin(json_file):
    """Checks if the saved starting address is correct.
    Opens the addresses JSON file, prompts user to see if the
    current origin is correct, if not it calls address_formatting
    to get the new address and saves it as the origin."""

    with open(json_file, 'r') as file:
        address_list = json.load(file)
    answer = input("Is your starting address %s?\nEnter Y or N:\n" % address_list['origin']).upper()
    while answer != 'Y' and answer != 'N':
        answer = input("Try again.\nIs %s your starting address?\nEnter Y or N:\n" % address_list['origin']).upper()
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
        print("Your starting address is %s.\nAddress List:" % addresses['origin'])
        for address, info in addresses['addresses'].items():
            print("%s:\n\tSet Arrival Time: %s\n\tEstimated Job Time: %s" % (address, info[0], info[1]))


def edit_addresses(json_file):
    # Allows editing of the saved addresses
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    for address, info in addresses['addresses'].items():
        print(address)
        print("\tSet Time: %s\n\tEstimated Job Time: %s" % (info[0], info[1]))
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
    order = []
    op = []

    if waypoints != '':
        try:
            response = requests.get(api.format(origin, destination, waypoints, key)).json()
            order.append(response['routes'][0]['waypoint_order'])
            for leg in response['routes'][0]['legs']:
                print("\n")
                for step in leg['steps']:
                    soup = BeautifulSoup(step['html_instructions'], features="html.parser")
                    print(soup.text + '\n' + "{}\n".format(step['distance']['text']))
                    op.append(soup.text + '\n' + "{}\n".format(step['distance']['text']))
                    # Makes the html directions readable
                op.append('<br>')
        except:
            print("Error.  Please check connection.")
        # Exception handling is to prevent issues in case of no internet connection.
    else:
        api = api.replace('waypoints=optimize:true|{}', '')
        try:
            response = requests.get(api.format(origin, destination, key)).json()
            order.append(response['routes'][0]['waypoint_order'])
            for leg in response['routes'][0]['legs']:
                print("\n")
                for step in leg['steps']:
                    soup = BeautifulSoup(step['html_instructions'], features="html.parser")
                    print(soup.text + '\n' + "{}\n".format(step['distance']['text']))
                    op.append(soup.text + '\n' + "{}\n".format(step['distance']['text']))
                    # Makes the html directions readable
                op.append('<br>')
        except:
            print("Error.  Please check connection.")
    d = '<br>'.join('{}'.format(p) for p in op)
    order.append(d)
    print("\nOptimized Route Order: {}".format(order[0]))
    return order



def one_set_time(api, key, points_with_times, points_without_times, origin):
    starting_time = round(time.time())
    print(points_with_times)
    set_time_address = points_with_times[0][0]
    set_time = points_with_times[0][1][0]
    print(set_time)
    print(set_time_address)
    time_left = set_time - starting_time
    print("time left {}".format(time_left))
    waypoints = ''
    waypoint_total_time = 0
    for address in points_without_times:
        waypoints += '|' + address[0]
        waypoint_total_time += int(address[1][1])
    print("wp job times %d" % waypoint_total_time)
    response_all = requests.get(api.format(origin, set_time_address, waypoints, key)).json()
    for leg in response_all['routes'][0]['legs']:
        waypoint_total_time += leg['duration']['value']
    print(waypoint_total_time)
    if waypoint_total_time < time_left:
        w1 = routing(api, key, origin, set_time_address, waypoints)
        waypoints = ''
        w2 = routing(api, key, set_time_address, origin, waypoints)
        optimized_wp_order = '|'.join('{}'.format(points_without_times[i][0]) for i in w1[0])
        optimized_wp_order += '|' + set_time_address
        directions = w1[1] + w2[1]
        mapping(h_file, key, origin, optimized_wp_order, directions)
    else:
        combos = []
        for num_in_combos in range(1, len(points_without_times)):
            for com in combinations(points_without_times, num_in_combos):
                combos.append(com)
        combos = combos[::-1]
        pp.pprint(combos)
        best_choice = []
        addresses_after = []
        api_counter = 0
        for combo in combos:
            wp = '|'.join('{}'.format(waypoint[0]) for waypoint in combo)
            print(wp)
            wp_time = 0
            if best_choice and len(combo) < len(best_choice[0]):
                print("\n\nBREAK\n\n")
                break
            for com in combo:
                wp_time += com[1][1]
            r = requests.get(api.format(origin, set_time_address, wp, key)).json()
            api_counter += 1
            for leg in r['routes'][0]['legs']:
                wp_time += leg['duration']['value']
            if wp_time < time_left:
                if not best_choice:
                    best_choice = [list(x[0] for x in combo), wp_time]
                elif best_choice[1] < wp_time and len(combo) >= len(best_choice[0]):
                    best_choice = [list(x[0] for x in combo), wp_time]
                print(best_choice)
            print(wp_time)
        print(api_counter)
        print(best_choice)
        if not best_choice:
            wp = '|'.join('{}'.format(waypoint[0]) for waypoint in points_without_times)
            w = ''
            w1 = routing(api, key, origin, set_time_address, w)
            w2 = routing(api, key, set_time_address, origin, wp)
            optimized_wp_order = set_time_address + '|'
            print('\n\n\n\n\n')

            optimized_wp_order += '|'.join('{}'.format(points_without_times[i][0]) for i in w2[0])
            print(optimized_wp_order)
            print('\n\n\n\n\n')
            directions = w1[1] + w2[1]
            mapping(h_file, key, origin, optimized_wp_order, directions)
        else:
            for a in points_without_times:
                if a[0] not in best_choice[0]:
                    addresses_after.append(a[0])
            waypoints = '|'.join('{}'.format(waypoint) for waypoint in best_choice[0])
            wps_after = '|'.join('{}'.format(waypoint) for waypoint in addresses_after)
            w1 = routing(api, key, origin, set_time_address, waypoints)
            w2 = routing(api, key, set_time_address, origin, wps_after)
            optimized_wp_order = '|'.join('{}'.format(best_choice[0][i]) for i in w1[0]) + '|'
            optimized_wp_order += '|'.join('{}'.format(address) for address in addresses_after)
            directions = w1[1] + w2[1]
            mapping(h_file, key, origin, optimized_wp_order, directions)


def two_set_times(api, key, points_with_times, points_without_times, origin):
    starting_time = round(time.time())
    points_with_times.sort(key=lambda x:x[1][0])
    print(points_with_times)
    stop1_address = points_with_times[0][0]
    stop2_address = points_with_times[1][0]
    time_before_stop1 = points_with_times[0][1][0] - starting_time
    time_between_1and2 = points_with_times[1][1][0] - points_with_times[0][1][1] - points_with_times[0][1][0]
    waypoints = '|'.join('{}'.format(address[0]) for address in points_without_times)
    response = requests.get(api.format(origin, points_with_times[0][0], waypoints, key)).json()
    wp_total_time = 0
    print(points_without_times)
    for point in points_without_times:
        wp_total_time += point[1][1]
    print(wp_total_time)
    for leg in response['routes'][0]['legs']:
        wp_total_time += leg['duration']['value']
    print(wp_total_time)
    if wp_total_time < time_before_stop1:
        w1 = routing(api, key, origin, points_with_times[0][0], waypoints)
        waypoints = ''
        w2 = routing(api, key, points_with_times[0][0], points_with_times[1][0], waypoints)
        w3 = routing(api, key, points_with_times[1][0], origin, waypoints)
        optimized_wp_order = '|'.join('{}'.format(points_without_times[i][0]) for i in w1[0]) + '|'
        optimized_wp_order += points_with_times[0][0] + '|' + points_with_times[1][0]
        directions = w1[1] + w2[1] + w3[1]
        mapping(h_file, key, origin, optimized_wp_order, directions)
    else:
        combos = []
        remaining_addresses = []
        for num_in_combos in range(1, len(points_without_times)):
            for com in combinations(points_without_times, num_in_combos):
                combos.append(com)
        combos = combos[::-1]
        pp.pprint(combos)
        best_choice = []
        for combo in combos:
            if best_choice and len(combo) < len(best_choice[0]):
                print("\n\nBREAK\n\n")
                break
            wp = '|'.join('{}'.format(waypoint[0]) for waypoint in combo)
            print(wp)
            wp_time = 0
            for com in combo:
                wp_time += com[1][1]
            r = requests.get(api.format(origin, stop1_address, wp, key)).json()
            for leg in r['routes'][0]['legs']:
                wp_time += leg['duration']['value']
            if wp_time < time_before_stop1:
                if not best_choice:
                    best_choice = [list(x[0] for x in combo), wp_time]
                elif best_choice[1] < time_before_stop1 and len(combo) >= len(best_choice[0]):
                    best_choice = [list(x[0] for x in combo), wp_time]
            print(best_choice)
            print(wp_time)
        print(best_choice)
        if best_choice:
            for point in points_without_times:
                if point[0] not in best_choice[0]:
                    remaining_addresses.append(point)
            print('\n\n')
            print(best_choice)
            print(remaining_addresses)
            if len(remaining_addresses) == 1:
                response = requests.get(api.format(points_with_times[0][0], points_with_times[1][0], remaining_addresses[0], key)).json()
                pp.pprint(response)
                wp_time = remaining_addresses[0][1][1]
                for leg in response['routes'][0]['legs']:
                    wp_time += leg['duration']['value']
                print(wp_time)
                if wp_time < time_between_1and2:
                    waypoints = '|'.join('{}'.format(address) for address in best_choice[0])
                    w1 = routing(api, key, origin, points_with_times[0][0], waypoints)
                    waypoints = remaining_addresses[0]
                    w2 = routing(api, key, points_with_times[0][0], points_with_times[1][0], waypoints)
                    waypoints = ''
                    w3 = routing(api, key, points_with_times[1][0], origin, waypoints)
                    optimized_wp_order = '|'.join('{}'.format(points_without_times[i][0]) for i in w1[0]) + '|' 
                    optimized_wp_order += points_with_times[0][0] + '|' + remaining_addresses[0] + '|' + points_with_times[1][0]
                    directions = w1[1] + w2[1] + w3[1]
                    mapping(h_file, key, origin, optimized_wp_order, directions)
                else:
                    waypoints = '|'.join('{}'.format(address) for address in best_choice[0])
                    w1 = routing(api, key, origin, points_with_times[0][0], waypoints)
                    waypoints = ''
                    w2 = routing(api, key, points_with_times[0][0], points_with_times[1][0], waypoints)
                    w3 = routing(api, key, points_with_times[1][0], origin, remaining_addresses[0])
                    optimized_wp_order = '|'.join('{}'.format(points_without_times[i][0]) for i in w1[0]) + '|' 
                    optimized_wp_order += points_with_times[0][0] + '|' + points_with_times[1][0]+ '|' + remaining_addresses[0][0]
                    directions = w1[1] + w2[1] + w3[1]
                    mapping(h_file, key, origin, optimized_wp_order, directions)
            else:
                combos = []
                best_choice_leg2 = []
                for num_in_combos in range(1, len(remaining_addresses)):
                    for com in combinations(remaining_addresses, num_in_combos):
                        combos.append(com)
                combos = combos[::-1]
                pp.pprint(combos)
                for combo in combos:
                    if best_choice_leg2 and len(combo) < len(best_choice_leg2[0]):
                        print("\n\nBREAK\n\n")
                        break
                    wp = '|'.join('{}'.format(waypoint[0]) for waypoint in combo)
                    print(wp)
                    wp_time = 0
                    for com in combo:
                        wp_time += com[1][1]
                        r = requests.get(api.format(origin, stop1_address, wp, key)).json()
                    for leg in r['routes'][0]['legs']:
                        wp_time += leg['duration']['value']
                    if wp_time < time_between_1and2:
                        if not best_choice_leg2:
                            best_choice_leg2 = [list(x[0] for x in combo), wp_time]
                        elif best_choice_leg2[1] < time_between_1and2 and len(combo) >= len(best_choice_leg2[0]):
                            best_choice_leg2 = [list(x[0] for x in combo), wp_time]
                    print(best_choice_leg2)
                    print(wp_time)
                print(best_choice_leg2)
                if best_choice_leg2:
                    last_addresses = []
                    for point in points_without_times:
                        if point[0] not in best_choice[0] and point[0] not in best_choice_leg2[0]:
                            last_addresses.append(point)
                    if not last_addresses:
                        waypoints = '|'.join('{}'.format(address) for address in best_choice[0])
                        w1 = routing(api, key, origin, points_with_times[0][0], waypoints)
                        waypoints = '|'.join('{}'.format(address) for address in best_choice_leg2[0])
                        w2 = routing(api, key, points_with_times[0][0], points_with_times[1][0], waypoints)
                        w3 = routing(api, key, points_with_times[1][0], origin, '')
                        optimized_wp_order = '|'.join('{}'.format(best_choice[0][i]) for i in w1[0]) + '|' 
                        optimized_wp_order += points_with_times[0][0] + '|' + '|'.join('{}'.format(best_choice[0][i]) for i in w1[0])
                        optimized_wp_order += '|' + points_with_times[1][0]
                        directions = w1[1] + w2[1] + w3[1]
                        mapping(h_file, key, origin, optimized_wp_order, directions)
                    elif len(last_addresses) == 1:
                        waypoint1 = '|'.join('{}'.format(address) for address in best_choice[0])
                        w1 = routing(api, key, origin, points_with_times[0][0], waypoint1)
                        waypoint2 = '|'.join('{}'.format(address) for address in best_choice_leg2[0])
                        w2 = routing(api, key, points_with_times[0][0], points_with_times[1][0], waypoint2)
                        w3 = routing(api, key, points_with_times[1][0], origin, last_addresses[0])
                        optimized_wp_order = '|'.join('{}'.format(best_choice[0][i]) for i in w1[0]) + '|'
                        optimized_wp_order +=  points_with_times[0][0] + '|' + '|'.join('{}'.format(best_choice_leg2[i][0]) for i in w2[0])
                        optimized_wp_order += '|' + points_with_times[1][0] + last_addresses[0][0]
                        directions = w1[1] + w2[1] + w3[1]
                        mapping(h_file, key, origin, optimized_wp_order, directions)
                    else:
                        waypoint1 = '|'.join('{}'.format(address) for address in best_choice[0])
                        w1 = routing(api, key, origin, points_with_times[0][0], waypoint1)
                        waypoint2 = '|'.join('{}'.format(address) for address in best_choice_leg2[0])
                        w2 = routing(api, key, points_with_times[0][0], points_with_times[1][0], waypoint2)
                        waypoint3 = '|'.join('{}'.format(address[0]) for address in last_addresses)
                        w3 = routing(api, key, points_with_times[1][0], origin, waypoint3)
                        optimized_wp_order = '|'.join('{}'.format(best_choice[0][i]) for i in w1[0]) + '|' + points_with_times[0][0] + '|'
                        optimized_wp_order +=  '|'.join('{}'.format(best_choice_leg2[0][i]) for i in w2[0]) + '|' + points_with_times[1][0]
                        optimized_wp_order += '|'.join('{}'.format(last_addresses[i][0]) for i in w3[0])
                        directions = w1[1] + w2[1] + w3[1]
                        mapping(h_file, key, origin, optimized_wp_order, directions)
                else:
                    waypoint1 = '|'.join('{}'.format(address) for address in best_choice[0])
                    w1 = routing(api, key, origin, points_with_times[0][0], waypoint1)
                    








def three_set_times(api, key, points_with_times, points_without_times, origin):
    pass


def four_set_times(api, key, points_with_times, points_without_times, origin):
    pass


def five_set_times(api, key, points_with_times, points_without_times, origin):
    pass


def six_set_times(api, key, points_with_times, points_without_times, origin):
    pass
    

def setting_route(api, key, json_file):
    with open(json_file, 'r') as file:
        addresses = json.load(file)
    points_without_times = []
    points_with_times = []
    origin = get_origin(json_file)
    for address in addresses['addresses'].keys():
        if addresses['addresses'][address][0] == "None":
            points_without_times.append([address, addresses['addresses'][address]])
        else:
            points_with_times.append([address, addresses['addresses'][address]])
    if len(points_with_times) == 0:
        waypoints = '|'.join('{}'.format(address[0]) for address in points_without_times)
        order = routing(api, key, origin, origin, waypoints)
        optimized_wp_order = '|'.join('{}'.format(points_without_times[i][0]) for i in order[0])
        print(len(order))
        print(type(order))
        mapping(h_file, key, origin, optimized_wp_order, order[1])
        print(waypoints)
        print('\n\n')
        print(optimized_wp_order)
        print(points_without_times)
    else:
        if len(points_with_times) == 1:
            one_set_time(api, key, points_with_times, points_without_times, origin)
        elif len(points_with_times) == 2:
            two_set_times(api, key, points_with_times, points_without_times, origin)


def testing_time_change(jsonf):
    with open(jsonf, 'r') as file:
        addresses = json.load(file)
    print("grace del")
    hours = int(input("Enter new hours. \n"))
    minutes = int(input("Enter new min. \n"))
    am_pm = input("AM or PM?\n").upper()
    while am_pm != 'AM' and am_pm != 'PM':
        am_pm = input("Please enter AM or PM?\n").upper()
    if am_pm == 'PM' and hours < 12:
        hours += 12
    job = int(input("Enter job length. \n"))


    addresses['addresses']['301 grace del ln pittsburgh, pa 15237'] = [time_formatting(hours, minutes), job * 60]

    print("cbry")
    hours = int(input("Enter new hours. \n"))
    minutes = int(input("Enter new min. \n"))
    am_pm = input("AM or PM?\n").upper()
    while am_pm != 'AM' and am_pm != 'PM':
        am_pm = input("Please enter AM or PM?\n").upper()
    if am_pm == 'PM' and hours < 12:
        hours += 12
    job = int(input("Enter job length. \n"))


    addresses['addresses']['100 briarwood ln cranberry twp, pa 16066'] = [time_formatting(hours, minutes), job * 60]
    with open(jsonf, 'w') as f:
        json.dump(addresses, f)
    print(addresses)




# check_origin(route_data)
# set_addresses(route_data)
view_addresses(route_data)
#testing_time_change(route_data)
#edit_addresses(route_data)
setting_route(google_directions_api_url, directions_key, route_data)


print("%s" % (time.time() - s_time))

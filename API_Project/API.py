import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import tkinter as tk
import tkinter.messagebox


url = 'https://maps.googleapis.com/maps/api/directions/json?origin={o}&destination={d}&mode={m}&key=AIzaSyAYixVeTbunLmxgrk3TcVrUE9sWhGY64bI'


def run(url, origin, destination, travel_mode):
    url = url.replace('{o}', origin).replace('{d}', destination).replace('{m}', travel_mode)
    request = requests.get(url).json()
    directions = ''
    num_of_secs = request['routes'][0]['legs'][0]['duration']['value']
    arrival = format(datetime.now() + timedelta(seconds=num_of_secs), '%H:%M')
    # gets the time you would arrive at the destination
    directions += "If you leave now you will arrive at %s. \n\n" % arrival
    # sets first line of output as the arrival time
    for step in request['routes'][0]['legs'][0]['steps']:
        soup = BeautifulSoup(step['html_instructions'], features="html.parser")
        # gets the text from the html directions
        directions += soup.text + '\n' + format("%s.\n" % step['distance']['text'])
        # adds each direction step to the output
    tk.messagebox.showinfo('Directions', directions)
    # shows messagebox as output


def empty_field_check(url, origin, destination, mode):  # makes sure info is properly inputted in GUI
    if origin != '' and destination != '':
        run(url,origin,destination,mode)
        # calls run if origin and destination fields are not blank
    else:
        tkinter.messagebox.showerror('ERROR', 'Please enter a starting and ending location. ')


def gui():  # makes GUI
    root = tk.Tk()
    root.wm_title('Directions')
    frame = tk.Frame(root)
    frame.pack()
    origin_location = tk.Label(frame, text="Starting Point", font='Times 20')
    destination_location = tk.Label(frame, text="Destination", font='Times 20')
    origin_location.grid(column=0,row=0,pady=10,padx=10)
    destination_location.grid(column=0,row=1,pady=10,padx=10)
    origin = tk.StringVar()
    destination = tk.StringVar()
    origin_box = tk.Entry(frame, textvariable=origin)
    dest_box = tk.Entry(frame, textvariable=destination)
    origin_box.grid(column=1,row=0,padx=10)
    dest_box.grid(column=1,row=1,padx=10)
    selected_mode = tk.StringVar(root)
    selected_mode.set('Driving')
    mode_selection = tk.OptionMenu(root, selected_mode, 'Driving', 'Walking', 'Bicycling')
    mode_selection.configure(font='Times 16')
    mode_selection.pack(pady=10)
    button = tk.Button(root, text='Get Directions', font='Times 18', command=lambda: empty_field_check(url, origin.get(), destination.get(), selected_mode.get().lower()))
    # when button is pressed it calls empty_field_check to make sure that the locations are filled in
    button.pack(pady=10)
    root.mainloop()


gui()

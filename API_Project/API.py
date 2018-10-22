import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox


url = 'https://maps.googleapis.com/maps/api/directions/json?origin={o}&destination={d}&mode={m}&key=AIzaSyAYixVeTbunLmxgrk3TcVrUE9sWhGY64bI'


def run(url, origin, destination, travel_mode):
    url = url.replace('{o}', origin).replace('{d}', destination).replace('{m}', travel_mode)
    request = requests.get(url).json()
    directions = ''
    arrival = format(datetime.now() + timedelta(seconds=request['routes'][0]['legs'][0]['duration']['value']), '%H:%M')
    directions += "If you leave now you will arrive at %s. \n" % arrival
    for step in request['routes'][0]['legs'][0]['steps']:
        soup = BeautifulSoup(step['html_instructions'], features="html.parser")
        directions += soup.text + '\n' + format("%s.\n" % step['distance']['text'])
    tk.messagebox.showinfo('Directions', directions)


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
button = tk.Button(root, text='Get Directions', font='Times 18', command=lambda: run(url,origin.get(),destination.get(),selected_mode.get().lower()))
button.pack(pady=10)
root.mainloop()

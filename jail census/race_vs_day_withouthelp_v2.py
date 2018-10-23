from tkinter import *
import tkinter.messagebox

main_win = Tk()
main_win.title("Python 2 mini-project")
main_win.geometry('300x250')

day_var = StringVar(main_win) # Chosen date gets saved as this var.
day_var.set("Choose A Date") # Default in drop-down menu.
day_choices = []  # Options of dates in the file

with open('9-18.csv', 'r') as file:  # opens the file.
    lines = file.readlines()[1:]  # Takes the remaining rows and saves in array
    for line in lines:
        if line.split(",")[1] not in day_choices:  # checks to see if the day is already in the choices
            day_choices.append(line.split(',')[1])  # adds date to days if not already in there


def error():  # Outputs error messagebox.
    tkinter.messagebox.showerror(title='ERROR', message='Choose a date!')


def output(tot_white_inmates, tot_black_inmates, total_inmates):  # Outputs the answer in a messagebox.
    w_percentage = tot_white_inmates / total_inmates * 100  # Gets the percentage of white inmates
    b_percentage = tot_black_inmates / total_inmates * 100  # Gets the percentage of black inmates
    main_win.withdraw()  # Closes the original window when the messagebox pops up.
    tkinter.messagebox.showinfo("Allegheny County Jail Census", """There are %s black inmates.\n
There are %s white inmates.\n
Allegheny County's population is 84.33 percent white and 12.41 percent black.\n
%.2f percent of inmates in Allegheny County are black and only %.2f percent are white.\n
This is NOT okay!
""" % (tot_black_inmates, tot_white_inmates, b_percentage, w_percentage))  # formats output.
    main_win.destroy()  # Quits when messagebox closes.


def create_dict():
    days = []
    list_of_dictionaries = []
    with open('9-18.csv', 'r') as jail_file:
        key = jail_file.readline().split(',')  # Takes in the first row and splits up the keys
        rows = jail_file.readlines()  # Takes the remaining rows and saves in array
        for row in rows:
            if row.split(',')[1] == day_var.get():  # if the date in the current row is the same as the selected date
                days.append(row.rstrip('\n').split(','))
                # it strips off the end-line, splits it into a list, and adds it to days.
        for day in days:
            d = zip(key, day)  # each item in each day gets zipped with the corresponding keys
            list_of_dictionaries.append(dict(d))  # takes each zipped key and val and makes dictionary out of them
        return list_of_dictionaries


def run():
    list_of_dicts = create_dict()  # calls create_dicts and returns the list of dictionaries needed
    tot_black_inmates = 0
    tot_white_inmates = 0
    total_inmates = 0
    print(list_of_dicts)
    for row in list_of_dicts:
        total_inmates += 1  # Increments total_inmates counter
        if row['Race'] == 'B':  # adds one to tot_black_inmates if inmates 'Race' == 'B'
            tot_black_inmates += 1
        if row['Race'] == 'W':  # adds one to tot_black_inmates if inmates 'Race' == 'W'
            tot_white_inmates += 1
    output(tot_white_inmates, tot_black_inmates, total_inmates)  # calls output with the total numbers


def error_test():  # Checks to see if a date is selected before running.
    if day_var.get() == 'Choose A Date': # If no date is selected it calls error()
        error()
    else: # If there is a date selected it calls run()
        run()


#  rest of the stuff for GUI
label = Label(main_win, text='Allegheny County Jail Census', font='Times 12 bold')
label.pack(pady=20)
drop_down_day = OptionMenu(main_win, day_var, *day_choices)  # dropdown for date selection
drop_down_day.pack(pady=20)
drop_down_day.configure(font='Times 11')
button = Button(main_win,text="OK", width=10, height=2, command=error_test)
# Button push calls error_test
button.pack(padx=4, pady=30)
main_win.mainloop()

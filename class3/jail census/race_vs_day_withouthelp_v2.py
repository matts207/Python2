from tkinter import *
import tkinter.messagebox

main_win = Tk()
main_win.title("Python 2 mini-project")
main_win.geometry('300x250')

day_var = StringVar(main_win) # Chosen date gets saved as this var.
day_var.set("Choose A Date") # Default in drop-down menu.
day_choices = []  # Options of dates in the file

with open('9-18.csv', 'r') as file:
    lines = file.readlines()[1:]  # Takes the remaining rows and saves in array
    for line in lines:
        if line.split(",")[1] not in day_choices:
            day_choices.append(line.split(',')[1])


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
""" % (tot_black_inmates, tot_white_inmates, b_percentage, w_percentage))
    main_win.destroy()  # Quits when messagebox closes.


def run():
    days = []
    dictionary = []
    tot_black_inmates = 0
    tot_white_inmates = 0
    total_inmates = 0
    with open('9-18.csv', 'r') as jail_file:
        key = jail_file.readline().split(',')  # Takes in the first row and splits up the keys
        rows = jail_file.readlines()  # Takes the remaining rows and saves in array
        [days.append(row.rstrip('\n').split(',')) for row in rows if row.split(',')[1] == day_var.get()]
        # in-line if statement splitting up the data in the row if the date is correct
        # in-line for loop adding those dates to the list 'd'
        [dictionary.append(dict(zip(key, k))) for k in days]  # in-line for loop adding the dicts
    for row in dictionary:
        total_inmates += 1
        if row['Race'] == 'B':
            tot_black_inmates += 1
        if row['Race'] == 'W':
            tot_white_inmates += 1
    output(tot_white_inmates, tot_black_inmates, total_inmates)


def error_test():  # Checks to see if a date is selected before running.
    if day_var.get() == 'Choose A Date':
        error()
    else:
        run()


label = Label(main_win, text='Allegheny County Jail Census', font='Times 12 bold')
label.pack(pady=20)
drop_down_day = OptionMenu(main_win, day_var, *day_choices)
drop_down_day.pack(pady=20)
drop_down_day.configure(font='Times 11')
button = Button(main_win,text="OK", width=10, height=2, command=error_test)
button.pack(padx=4, pady=30)
main_win.mainloop()


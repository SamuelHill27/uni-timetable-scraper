from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import datetime

from html_scraper import scrape
from csv_formatter import format

directory = ''

window = Tk()
window.eval('tk::PlaceWindow . center')
window.title("Python Scraper Form")
window.geometry('400x200')

frame = Frame(window)
frame.pack(padx=20, pady=20)

lbl = Label(frame)
lbl.grid(row=5, column=1, padx=5, pady=5)

Label(frame, text="Start date of term:", font=("Arial", 10), justify=LEFT, anchor="w").grid(sticky=W, row=0, column=0)
Label(frame, text="Format: 'dd/mm/yyyy', future", justify=LEFT, anchor="w").grid(sticky=W, row=1, column=0)
Label(frame, text="Number of weeks in term:", font=("Arial", 10), justify=LEFT, anchor="w").grid(sticky=W, row=2, column=0)
Label(frame, text="Format: integer, max 50", justify=LEFT, anchor="w").grid(sticky=W, row=3, column=0)

start_week_entry = Entry(frame)
start_week_entry.grid(row=0, column=1, padx=5)
number_of_weeks_entry = Entry(frame)
number_of_weeks_entry.grid(row=2, column=1, padx=5)

def get_file_name(directory):
    directory_parts = directory.split('/')
    file_name = directory_parts[len(directory_parts) - 1]
    return file_name

def upload_action():
    global directory
    directory = filedialog.askopenfilename()
    file_name = get_file_name(directory)
    Label(frame, text=file_name, justify=LEFT, anchor="w").grid(sticky=W, row=4, column=1, padx=5, pady=5)

ttk.Button(frame, text="Upload HTML file", command=upload_action).grid(row=4, column=0, padx=5, pady=5)

def validate_directory():
    if directory != '' and get_file_name(directory).split('.')[1] == 'html':
        return True
    return False

def validate_start_week():
    try:
        valid_date_format = bool(datetime.datetime.strptime(start_week_entry.get(), '%d/%m/%Y'))
    except ValueError:
        valid_date_format = False

    if start_week_entry.get() != '' and valid_date_format and datetime.datetime.strptime(start_week_entry.get(), '%d/%m/%Y') > datetime.datetime.now():
        return True
    return False

def validate_number_of_weeks():
    if number_of_weeks_entry.get().isdigit():
        if int(number_of_weeks_entry.get()) < 51:
            return True
    return False

def execute():
    lbl.config(text='')
    if validate_start_week() is False or validate_number_of_weeks() is False or validate_directory() is False:
        lbl.config(text='Error: Missing data')
        return

    df = scrape(directory)
    formatted_df = format(df, datetime.datetime.strptime(start_week_entry.get(), '%d/%m/%Y'), int(number_of_weeks_entry.get()))
    formatted_df.to_csv('timetable.csv')
    lbl.config(text='Success!')
    window.after(1000,lambda:window.destroy())

ttk.Button(frame, text="Submit", command=execute).grid(row=5, column=0, padx=5, pady=5)

window.mainloop()
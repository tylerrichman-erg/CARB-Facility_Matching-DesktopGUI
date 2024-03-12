import os
from openpyxl import load_workbook
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

### Set up environment ###
current_directory = os.path.dirname(os.path.realpath(__file__))

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_entry.config(state='normal')
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)
        file_path_entry.config(state='readonly')

        excel_file_path = file_path_entry.get()
        workbook = load_workbook(excel_file_path)
        sheet_names = workbook.sheetnames

        selected_option.set('')
        dropdown['menu'].delete(0, 'end')

        new_choices = sheet_names #('one', 'two', 'three')

        for choice in new_choices:
            dropdown['menu'].add_command(label=choice, command=tk._setit(selected_option, choice))

def load_excel_file():

    excel_path = file_path_entry.get()
    sheet_name = selected_option.get()

    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    selected_option_CO.set('')
    dropdown_CO['menu'].delete(0, 'end')

    selected_option_AB.set('')
    dropdown_AB['menu'].delete(0, 'end')

    selected_option_DIS.set('')
    dropdown_DIS['menu'].delete(0, 'end')

    selected_option_FACID.set('')
    dropdown_FACID['menu'].delete(0, 'end')

    selected_option_FNAME.set('')
    dropdown_FNAME['menu'].delete(0, 'end')

    selected_option_FSTREET.set('')
    dropdown_FSTREET['menu'].delete(0, 'end')

    selected_option_FCITY.set('')
    dropdown_FCITY['menu'].delete(0, 'end')

    selected_option_FZIP.set('')
    dropdown_FZIP['menu'].delete(0, 'end')

    selected_option_FSIC.set('')
    dropdown_FSIC['menu'].delete(0, 'end')

    selected_option_FNAICS.set('')
    dropdown_FNAICS['menu'].delete(0, 'end')

    selected_option_Latitude.set('')
    dropdown_Latitude['menu'].delete(0, 'end')

    selected_option_Longitude.set('')
    dropdown_Longitude['menu'].delete(0, 'end')

    new_choices = df.columns

    for choice in new_choices:
        dropdown_CO['menu'].add_command(label=choice, command=tk._setit(selected_option_CO, choice))
        dropdown_AB['menu'].add_command(label=choice, command=tk._setit(selected_option_AB, choice))
        dropdown_DIS['menu'].add_command(label=choice, command=tk._setit(selected_option_DIS, choice))
        dropdown_FACID['menu'].add_command(label=choice, command=tk._setit(selected_option_FACID, choice))
        dropdown_FNAME['menu'].add_command(label=choice, command=tk._setit(selected_option_FNAME, choice))
        dropdown_FSTREET['menu'].add_command(label=choice, command=tk._setit(selected_option_FSTREET, choice))
        dropdown_FCITY['menu'].add_command(label=choice, command=tk._setit(selected_option_FCITY, choice))
        dropdown_FZIP['menu'].add_command(label=choice, command=tk._setit(selected_option_FZIP, choice))
        dropdown_FSIC['menu'].add_command(label=choice, command=tk._setit(selected_option_FSIC, choice))
        dropdown_FNAICS['menu'].add_command(label=choice, command=tk._setit(selected_option_FNAICS, choice))
        dropdown_Latitude['menu'].add_command(label=choice, command=tk._setit(selected_option_Latitude, choice))
        dropdown_Longitude['menu'].add_command(label=choice, command=tk._setit(selected_option_Longitude, choice))

def execute_facility_matching():
    print("Running Facility Matching")

root = tk.Tk()
root.title("CARB Facility Matching")

### Set the height and width of the window ###
window_width = 800
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)
root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

### Create a frame to hold title ###
title_frame = tk.Frame(root)\
              .pack(pady=10)

### Create a label ###
label = tk.Label(title_frame, text="CARB Facility Matching")
label.pack(side='top', pady=10)
label.config(font=("Verdana", 14, "bold"))

### Create a frame to hold the entry and button widgets ###
file_selection_frame = tk.Frame(root)
file_selection_frame.pack(pady=10)

### Create a label ###
label = tk.Label(file_selection_frame, text="Select File")
label.grid(row=0, column=0, sticky='w')
label.config(font=("Verdana", 10, "bold"))

### Load the folder icon image ###
folder_icon_path = os.path.join(current_directory, "icons/Custom-Icon-Design-Flatastic-1-Folder.512.png")
folder_icon = Image.open(folder_icon_path)
folder_icon = folder_icon.resize((14, 14))
folder_icon = ImageTk.PhotoImage(folder_icon)

### Create a button to open the file dialog ###
open_button = tk.Button(file_selection_frame, image=folder_icon, command=open_file_dialog, width=15, height=15)
open_button.grid(row=0, column=1, padx=5)

### Create a text box for displaying the selected file path ###
file_path_entry = tk.Entry(file_selection_frame, width=50, font=("Verdana", 11), state='readonly')
file_path_entry.grid(row=0, column=2, sticky='e')

### Create a label ###
label = tk.Label(file_selection_frame, text="Select Sheet")
label.grid(row=1, column=0, sticky='w')
label.config(font=("Verdana", 10, "bold"))

### Create dropdown ###
options = [""]

selected_option = tk.StringVar(file_selection_frame)
selected_option.set(options[0])

dropdown = tk.OptionMenu(file_selection_frame, selected_option, *options)
dropdown.config(width=50)
dropdown.grid(row=1, column=2, sticky="ew", padx=0, pady=5) 

### Execute Read in ###
load_button = tk.Button(file_selection_frame, text="Load", command=load_excel_file)
load_button.config(font=("Verdana", 10, "bold"))
load_button.grid(row=2, column=0, columnspan=3, pady=5, sticky='nsew')

### Create a frame to hold the entry and button widgets ###
field_selection_frame = tk.Frame(root)
field_selection_frame.pack(pady=10)

### Create entires for fields ###
field_options = [""]

selected_option_CO = tk.StringVar(field_selection_frame)
selected_option_CO.set(options[0])

label_CO = tk.Label(field_selection_frame, text="CO")
label_CO.grid(row=0, column=0, padx=5, sticky='w')
label_CO.config(font=("Verdana", 10, "bold"))

dropdown_CO = tk.OptionMenu(field_selection_frame, selected_option_CO, *field_options)
dropdown_CO.config(width=50)
dropdown_CO.grid(row=0, column=1)

selected_option_AB = tk.StringVar(field_selection_frame)
selected_option_AB.set(options[0])

label_AB = tk.Label(field_selection_frame, text="AB")
label_AB.grid(row=1, column=0, padx=5, sticky='w')
label_AB.config(font=("Verdana", 10, "bold"))

dropdown_AB = tk.OptionMenu(field_selection_frame, selected_option_AB, *field_options)
dropdown_AB.config(width=50)
dropdown_AB.grid(row=1, column=1)

selected_option_DIS = tk.StringVar(field_selection_frame)
selected_option_DIS.set(options[0])

label_DIS = tk.Label(field_selection_frame, text="DIS")
label_DIS.grid(row=2, column=0, padx=5, sticky='w')
label_DIS.config(font=("Verdana", 10, "bold"))

dropdown_DIS = tk.OptionMenu(field_selection_frame, selected_option_DIS, *field_options)
dropdown_DIS.config(width=50)
dropdown_DIS.grid(row=2, column=1)

selected_option_FACID = tk.StringVar(field_selection_frame)
selected_option_FACID.set(options[0])

label_FACID = tk.Label(field_selection_frame, text="Facility ID")
label_FACID.grid(row=3, column=0, padx=5, sticky='w')
label_FACID.config(font=("Verdana", 10, "bold"))

dropdown_FACID = tk.OptionMenu(field_selection_frame, selected_option_FACID, *field_options)
dropdown_FACID.config(width=50)
dropdown_FACID.grid(row=3, column=1)

selected_option_FNAME = tk.StringVar(field_selection_frame)
selected_option_FNAME.set(options[0])

label_FNAME = tk.Label(field_selection_frame, text="Facility Name")
label_FNAME.grid(row=4, column=0, padx=5, sticky='w')
label_FNAME.config(font=("Verdana", 10, "bold"))

dropdown_FNAME = tk.OptionMenu(field_selection_frame, selected_option_FNAME, *field_options)
dropdown_FNAME.config(width=50)
dropdown_FNAME.grid(row=4, column=1)

selected_option_FSTREET = tk.StringVar(field_selection_frame)
selected_option_FSTREET.set(options[0])

label_FSTREET = tk.Label(field_selection_frame, text="Facility Street")
label_FSTREET.grid(row=5, column=0, padx=5, sticky='w')
label_FSTREET.config(font=("Verdana", 10, "bold"))

dropdown_FSTREET = tk.OptionMenu(field_selection_frame, selected_option_FSTREET, *field_options)
dropdown_FSTREET.config(width=50)
dropdown_FSTREET.grid(row=5, column=1)

selected_option_FCITY = tk.StringVar(field_selection_frame)
selected_option_FCITY.set(options[0])

label_FCITY = tk.Label(field_selection_frame, text="Facility City")
label_FCITY.grid(row=6, column=0, padx=5, sticky='w')
label_FCITY.config(font=("Verdana", 10, "bold"))

dropdown_FCITY = tk.OptionMenu(field_selection_frame, selected_option_FCITY, *field_options)
dropdown_FCITY.config(width=50)
dropdown_FCITY.grid(row=6, column=1)

selected_option_FZIP = tk.StringVar(field_selection_frame)
selected_option_FZIP.set(options[0])

label_FZIP = tk.Label(field_selection_frame, text="Facility ZIP")
label_FZIP.grid(row=7, column=0, padx=5, sticky='w')
label_FZIP.config(font=("Verdana", 10, "bold"))

dropdown_FZIP = tk.OptionMenu(field_selection_frame, selected_option_FZIP, *field_options)
dropdown_FZIP.config(width=50)
dropdown_FZIP.grid(row=7, column=1)

selected_option_FSIC = tk.StringVar(field_selection_frame)
selected_option_FSIC.set(options[0])

label_FSIC = tk.Label(field_selection_frame, text="Facility SIC")
label_FSIC.grid(row=8, column=0, padx=5, sticky='w')
label_FSIC.config(font=("Verdana", 10, "bold"))

dropdown_FSIC = tk.OptionMenu(field_selection_frame, selected_option_FSIC, *field_options)
dropdown_FSIC.config(width=50)
dropdown_FSIC.grid(row=8, column=1)

selected_option_FNAICS = tk.StringVar(field_selection_frame)
selected_option_FNAICS.set(options[0])

label_FNAICS = tk.Label(field_selection_frame, text="Facility NAICS")
label_FNAICS.grid(row=9, column=0, padx=5, sticky='w')
label_FNAICS.config(font=("Verdana", 10, "bold"))

dropdown_FNAICS = tk.OptionMenu(field_selection_frame, selected_option_FNAICS, *field_options)
dropdown_FNAICS.config(width=50)
dropdown_FNAICS.grid(row=9, column=1)

selected_option_Latitude = tk.StringVar(field_selection_frame)
selected_option_Latitude.set(options[0])

label_Latitude = tk.Label(field_selection_frame, text="Facility Latitude")
label_Latitude.grid(row=10, column=0, padx=5, sticky='w')
label_Latitude.config(font=("Verdana", 10, "bold"))

dropdown_Latitude = tk.OptionMenu(field_selection_frame, selected_option_Latitude, *field_options)
dropdown_Latitude.config(width=50)
dropdown_Latitude.grid(row=10, column=1)

selected_option_Longitude = tk.StringVar(field_selection_frame)
selected_option_Longitude.set(options[0])

label_Longitude = tk.Label(field_selection_frame, text="Facility Longitude")
label_Longitude.grid(row=11, column=0, padx=5, sticky='w')
label_Longitude.config(font=("Verdana", 10, "bold"))

dropdown_Longitude = tk.OptionMenu(field_selection_frame, selected_option_Longitude, *field_options)
dropdown_Longitude.config(width=50)
dropdown_Longitude.grid(row=11, column=1)

### Execute Read in ###
execute_button = tk.Button(field_selection_frame, text="Execute", command=execute_facility_matching)
execute_button.config(font=("Verdana", 10, "bold"))
execute_button.grid(row=12, column=0, columnspan=3, pady=10, sticky='nsew')

root.mainloop()

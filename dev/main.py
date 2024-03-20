import configparser
import os
from openpyxl import load_workbook
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

import time

import algorithm


#############################################
########## Set Up Work Environment ##########
#############################################


current_directory = os.path.dirname(os.path.realpath(__file__))
git_directory = os.path.join(os.path.split(current_directory)[0], "config.ini")

config = configparser.ConfigParser()
config.read(git_directory)


######################################################
########## CARB Facility Matching Functions ##########
######################################################


def open_file_dialog():
    """
    Select input facility file for matching.
    """
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

        new_choices = sheet_names

        for choice in new_choices:
            dropdown['menu'].add_command(label=choice, command=tk._setit(selected_option, choice))

def select_output_file():
    """
    Select output file from matching.
    """
    output_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if output_file_path:
        file_path_output.config(state='normal')
        file_path_output.delete(0, tk.END)
        file_path_output.insert(0, output_file_path)
        file_path_output.config(state='readonly')

def load_button_actions():
    """
    Functions to run once load button is clicked.
    """
    load_excel_file()
    add_field_matching()
    add_output_file_selection()

def load_excel_file():
    """
    Load excel file columns and append to dropdowns.
    """
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

def add_field_matching():
    """
    Add field configuration to the window.
    """
    selection_label.grid(row=0, column=0, columnspan=2, pady=5, sticky='nsew')
    
    label_CO.grid(row=1, column=0, padx=5, sticky='w')
    dropdown_CO.grid(row=1, column=1)

    label_AB.grid(row=2, column=0, padx=5, sticky='w')
    dropdown_AB.grid(row=2, column=1)

    label_DIS.grid(row=3, column=0, padx=5, sticky='w')
    dropdown_DIS.grid(row=3, column=1)

    label_FACID.grid(row=4, column=0, padx=5, sticky='w')
    dropdown_FACID.grid(row=4, column=1)

    label_FNAME.grid(row=5, column=0, padx=5, sticky='w')
    dropdown_FNAME.grid(row=5, column=1)

    label_FSTREET.grid(row=6, column=0, padx=5, sticky='w')
    dropdown_FSTREET.grid(row=6, column=1)

    label_FCITY.grid(row=7, column=0, padx=5, sticky='w')
    dropdown_FCITY.grid(row=7, column=1)

    label_FZIP.grid(row=8, column=0, padx=5, sticky='w')
    dropdown_FZIP.grid(row=8, column=1)

    label_FSIC.grid(row=9, column=0, padx=5, sticky='w')
    dropdown_FSIC.grid(row=9, column=1)

    label_FNAICS.grid(row=10, column=0, padx=5, sticky='w')
    dropdown_FNAICS.grid(row=10, column=1)

    label_Latitude.grid(row=11, column=0, padx=5, sticky='w')
    dropdown_Latitude.grid(row=11, column=1)

    label_Longitude.grid(row=12, column=0, padx=5, sticky='w')
    dropdown_Longitude.grid(row=12, column=1)

    

def add_output_file_selection():
    """
    Add output file configuration to the window.
    """
    label_output.grid(row=0, column=0, sticky='w')
    open_button_output.grid(row=0, column=1, padx=5)
    file_path_output.grid(row=0, column=2, sticky='e')

    execute_button.grid(row=13, column=0, columnspan=3, pady=10, sticky='nsew')

def execute_facility_matching():
    """
    Run facility matching.
    """
    print("\n\n #### Starting Facility Matching #####\n\n")
    
    excel_path = file_path_entry.get()
    sheet_name = selected_option.get()
    
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    print("Standardizing Input Table...\n")
    
    df = algorithm.standardize_table(
        df = df,
        CO_name = selected_option_CO.get(),
        AB_name = selected_option_AB.get(),
        DIS_name = selected_option_DIS.get(),
        FACID_name = selected_option_FACID.get(),
        FNAME_name = selected_option_FNAME.get(),
        FSTREET_name = selected_option_FSTREET.get(),
        FCITY_name = selected_option_FCITY.get(),
        FZIP_name = selected_option_FZIP.get(),
        FSIC_name = selected_option_FSIC.get(),
        FNAICS_name = selected_option_FNAICS.get(),
        LAT_name = selected_option_Latitude.get(),
        LON_name = selected_option_Longitude.get()
        )

    print("Loading Parcel Dataset...\n")

    parcel_gdf = algorithm.load_parcel_dataset(
        pqt_folder_path = config["Locations"].get("Parcel_Parquet_Folder")
        )

    print("Performing Spatial Join with Parcel Dataset...\n")

    df = algorithm.run_spatial_join(df, parcel_gdf)

    print("Standardizing Facility Name and Address Fields...\n")

    df = algorithm.standardize_text_fields(df, logic_path = os.path.join(current_directory, "standardization/Word_Replacement_Table.csv"))

    print("Rounding Coordinates to 5 Decimal Places...\n")

    df["LATITUDE_ROUND_5"] = df["LAT_NAD83"].round(5)
    df["LONGITUDE_ROUND_5"] = df["LON_NAD83"].round(5)

    print("Reading in Master Facilities Table...\n")

    df_master = algorithm.read_in_master_table(
        db_loc = config["Locations"].get("Database_File"),
        table_name = config["Database"].get("Master_Facilities_Table_Name"),
        ARBID_name = config["Database"].get("AB_name"),
        CO_name = config["Database"].get("CO_name"),
        AB_name = config["Database"].get("AB_name"),
        DIS_name = config["Database"].get("DIS_name"),
        FACID_name = config["Database"].get("FACID_name"),
        FNAME_name = config["Database"].get("FNAME_name"),
        FSTREET_name = config["Database"].get("FSTREET_name"),
        FCITY_name = config["Database"].get("FCITY_name"),
        FZIP_name = config["Database"].get("FZIP_name"),
        FSIC_name = config["Database"].get("FSIC_name"),
        FNAICS_name = config["Database"].get("FNAICS_name"),
        LAT_name = config["Database"].get("LAT_name"),
        LON_name = config["Database"].get("LON_name"),
        PARCEL_name = config["Database"].get("PARCEL_name")
        )

    print("Executing Matching Algorithm...\n")

    df_matched = algorithm.execute_matching_algorithm(
        df,
        df_master,
        match_scores_fields_path = os.path.join(current_directory, "matching/logic.json")
        )

    df_matched.to_excel(file_path_output.get(), index=False)


#################################################
########## CARB Facility Matching Code ##########
#################################################   


########## Main Application Window Frame ##########
    
## Create root for window
root = tk.Tk()
root.title("CARB Facility Matching")

## Set the height and width of the window
window_width = 800
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)
root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))


########## Title Frame ##########

## Create frame for title
title_frame = tk.Frame(root)
title_frame.pack(pady=10)

## Create a label for title
label = tk.Label(title_frame, text="CARB Facility Matching")
label.pack(side='top', pady=10)
label.config(font=("Verdana", 14, "bold"))


########## File Entry Frame ##########

## Create frame for file entry
file_selection_frame = tk.Frame(root)
file_selection_frame.pack(pady=10)

## Create a label for file selection
label = tk.Label(file_selection_frame, text="Select File")
label.grid(row=0, column=0, sticky='w')
label.config(font=("Verdana", 10, "bold"))

## Load the folder icon image
folder_icon_path = os.path.join(current_directory, "icons/Custom-Icon-Design-Flatastic-1-Folder.512.png")
folder_icon = Image.open(folder_icon_path)
folder_icon = folder_icon.resize((14, 14))
folder_icon = ImageTk.PhotoImage(folder_icon)

## Create a button to open the file dialog
open_button = tk.Button(file_selection_frame, image=folder_icon, command=open_file_dialog, width=15, height=15)
open_button.grid(row=0, column=1, padx=5)

## Create a text box for displaying the selected file path
file_path_entry = tk.Entry(file_selection_frame, width=50, font=("Verdana", 11), state='readonly')
file_path_entry.grid(row=0, column=2, sticky='e')

## Create a label to select sheet
label = tk.Label(file_selection_frame, text="Select Sheet")
label.grid(row=1, column=0, sticky='w')
label.config(font=("Verdana", 10, "bold"))

## Create dropdown to select sheet
options = [""]
selected_option = tk.StringVar(file_selection_frame)
selected_option.set(options[0])

## Update dropdown to contain list of sheets from excel file
dropdown = tk.OptionMenu(file_selection_frame, selected_option, *options)
dropdown.config(width=50)
dropdown.grid(row=1, column=2, sticky="ew", padx=0, pady=5) 

## Create load button to read in table
load_button = tk.Button(file_selection_frame, text="Load", command=load_button_actions)
load_button.config(font=("Verdana", 10, "bold"))
load_button.grid(row=2, column=0, columnspan=3, pady=5, sticky='nsew')


########## Field Configuration Frame ##########

## Create frame for field configuration
field_selection_frame = tk.Frame(root)
field_selection_frame.pack(pady=10)

## Initialize dropdown options
field_options = [""]

## Create title for field configuration
selection_label = tk.Label(field_selection_frame, text="Field and Output Configuration")
selection_label.config(font=("Verdana", 12, "bold"))

## CO -- Create field configuration
selected_option_CO = tk.StringVar(field_selection_frame)
selected_option_CO.set(options[0])
label_CO = tk.Label(field_selection_frame, text="CO")
label_CO.config(font=("Verdana", 10, "bold"))
dropdown_CO = tk.OptionMenu(field_selection_frame, selected_option_CO, *field_options)
dropdown_CO.config(width=50)

## AB -- Create field configuration
selected_option_AB = tk.StringVar(field_selection_frame)
selected_option_AB.set(options[0])
label_AB = tk.Label(field_selection_frame, text="AB")
label_AB.config(font=("Verdana", 10, "bold"))
dropdown_AB = tk.OptionMenu(field_selection_frame, selected_option_AB, *field_options)
dropdown_AB.config(width=50)

## DIS -- Create field configuration
selected_option_DIS = tk.StringVar(field_selection_frame)
selected_option_DIS.set(options[0])
label_DIS = tk.Label(field_selection_frame, text="DIS")
label_DIS.config(font=("Verdana", 10, "bold"))
dropdown_DIS = tk.OptionMenu(field_selection_frame, selected_option_DIS, *field_options)
dropdown_DIS.config(width=50)

## FACID -- Create field configuration
selected_option_FACID = tk.StringVar(field_selection_frame)
selected_option_FACID.set(options[0])
label_FACID = tk.Label(field_selection_frame, text="Facility ID")
label_FACID.config(font=("Verdana", 10, "bold"))
dropdown_FACID = tk.OptionMenu(field_selection_frame, selected_option_FACID, *field_options)
dropdown_FACID.config(width=50)

## FNAME -- Create field configuration
selected_option_FNAME = tk.StringVar(field_selection_frame)
selected_option_FNAME.set(options[0])
label_FNAME = tk.Label(field_selection_frame, text="Facility Name")
label_FNAME.config(font=("Verdana", 10, "bold"))
dropdown_FNAME = tk.OptionMenu(field_selection_frame, selected_option_FNAME, *field_options)
dropdown_FNAME.config(width=50)

## FSTREET -- Create field configuration
selected_option_FSTREET = tk.StringVar(field_selection_frame)
selected_option_FSTREET.set(options[0])
label_FSTREET = tk.Label(field_selection_frame, text="Facility Street")
label_FSTREET.config(font=("Verdana", 10, "bold"))
dropdown_FSTREET = tk.OptionMenu(field_selection_frame, selected_option_FSTREET, *field_options)
dropdown_FSTREET.config(width=50)

## FCITY -- Create field configuration
selected_option_FCITY = tk.StringVar(field_selection_frame)
selected_option_FCITY.set(options[0])
label_FCITY = tk.Label(field_selection_frame, text="Facility City")
label_FCITY.config(font=("Verdana", 10, "bold"))
dropdown_FCITY = tk.OptionMenu(field_selection_frame, selected_option_FCITY, *field_options)
dropdown_FCITY.config(width=50)

## FZIP -- Create field configuration
selected_option_FZIP = tk.StringVar(field_selection_frame)
selected_option_FZIP.set(options[0])
label_FZIP = tk.Label(field_selection_frame, text="Facility ZIP")
label_FZIP.config(font=("Verdana", 10, "bold"))
dropdown_FZIP = tk.OptionMenu(field_selection_frame, selected_option_FZIP, *field_options)
dropdown_FZIP.config(width=50)

## FSIC -- Create field configuration
selected_option_FSIC = tk.StringVar(field_selection_frame)
selected_option_FSIC.set(options[0])
label_FSIC = tk.Label(field_selection_frame, text="Facility SIC")
label_FSIC.config(font=("Verdana", 10, "bold"))
dropdown_FSIC = tk.OptionMenu(field_selection_frame, selected_option_FSIC, *field_options)
dropdown_FSIC.config(width=50)

## FNAICS -- Create field configuration
selected_option_FNAICS = tk.StringVar(field_selection_frame)
selected_option_FNAICS.set(options[0])
label_FNAICS = tk.Label(field_selection_frame, text="Facility NAICS")
label_FNAICS.config(font=("Verdana", 10, "bold"))
dropdown_FNAICS = tk.OptionMenu(field_selection_frame, selected_option_FNAICS, *field_options)
dropdown_FNAICS.config(width=50)

## Latitude -- Create field configuration
selected_option_Latitude = tk.StringVar(field_selection_frame)
selected_option_Latitude.set(options[0])
label_Latitude = tk.Label(field_selection_frame, text="Facility Latitude")
label_Latitude.config(font=("Verdana", 10, "bold"))
dropdown_Latitude = tk.OptionMenu(field_selection_frame, selected_option_Latitude, *field_options)
dropdown_Latitude.config(width=50)

## Longitude -- Create field configuration
selected_option_Longitude = tk.StringVar(field_selection_frame)
selected_option_Longitude.set(options[0])
label_Longitude = tk.Label(field_selection_frame, text="Facility Longitude")
label_Longitude.config(font=("Verdana", 10, "bold"))
dropdown_Longitude = tk.OptionMenu(field_selection_frame, selected_option_Longitude, *field_options)
dropdown_Longitude.config(width=50)


########## Create Output File Frame ##########

## Create frame for file output
file_output_frame = tk.Frame(root)
file_output_frame.pack(pady=10)

## Create title for file output
selection_output_label = tk.Label(file_output_frame, text="Output File Location")
selection_output_label.config(font=("Verdana", 12, "bold"))

## Create a label for file output
label_output = tk.Label(file_output_frame, text="Output File")
label_output.config(font=("Verdana", 10, "bold"))

## Create a button to open the file dialog
open_button_output = tk.Button(file_output_frame, image=folder_icon, command=select_output_file, width=15, height=15)

## Create a text box for displaying the selected file path
file_path_output = tk.Entry(file_output_frame, width=50, font=("Verdana", 11), state='readonly')


########## Create Execute Button Frame ##########

## Create frame for execute button
execute_button_frame = tk.Frame(root)
execute_button_frame.pack(pady=5)

## Execute read in
execute_button = tk.Button(execute_button_frame, text="Execute", command=execute_facility_matching)
execute_button.config(font=("Verdana", 14, "bold"))


########## root.mainloop() ##########

root.mainloop()

"""
Description: Part 2 - GUI for final project.
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March April 5, 2024
Credit:
Updates:
"""
import tkinter
from tkinter import Button
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from plot_operations import PlotOperations
from weather_processor import WeatherProcessor
from scrape_weather import fetch_weather_data
from db_operations import DBOperations

def update_weather_data():
    """Updates the current missing weather data to the database."""
    # Logic for seeing if data needs to be updated.
    weather_processor = WeatherProcessor()
    update_dates_return = weather_processor.update_dates()

    if not update_dates_return :
        print("There is no new data available. You are up to date!")
        print()
        input("Press enter to exit...")
    else:
        weather_processor.update_data()
        print("Weather data successfully updated. :)")
        print()
        input("Press enter to exit...")

def all_weather_data():
    """Fetches and saves all weather data to the database."""
    print("Fetching weather data...")
    weather_data = fetch_weather_data()
    db = DBOperations()
    db.save_data(weather_data)
    print("Weather data successfully updated. :)")
    print()
    input("Press enter to exit...")


def display_box_plot():
    """Generates a box plot of weather data based on user input."""
    # Get the current year from datetime.
    current_year = datetime.now().year

    valid_starting_year = False
    valid_end_year = False

    while not valid_starting_year:
        try:
            starting_year = int(input(f"Please enter a starting year" \
                                    f" (between 1996-{current_year}): "))
            if 1996 <= starting_year <= current_year:
                valid_starting_year = True
            else:
                print(f"Error: Please enter a year between 1996 and {current_year}.")
        except ValueError:
            print("Invalid input. Please enter a valid year.")

    while not valid_end_year:
        try:
            end_year = int(input(f"Please enter an end year (between 1996-{current_year}): "))
            if 1996 <= end_year <= current_year and end_year >= starting_year:
                valid_end_year = True
            else:
                print(f"Error: Please enter a year between 1996 and {current_year}" \
                    f" that is not less than the starting year.")
        except ValueError:
            print("Invalid input. Please enter a valid year.")

    # Generate the plot.
    plot = PlotOperations()
    plot.plot_temperature_boxplots(starting_year, end_year)

    print("Box plot successfully generated.")
    print()
    input("Press enter to exit...")

def display_line_plot():
    """Generates a line graph of weather data based on user input."""
    # Get the current year from datetime.
    current_year = datetime.now().year

    valid_year = False
    valid_month = False

    while not valid_year:
        try:
            year = int(input(f"Please enter a year (between 1996-{current_year}): "))
            if 1996 <= year <= current_year:
                valid_year = True
            else:
                print(f"Error: Please enter a year between 1996 and {current_year}.")
        except ValueError:
            print("Invalid input. Please enter a valid year.")

    while not valid_month:
        try:
            month = int(input("Please enter a month (between 1-12): "))
            if 1 <= month <= 12:
                valid_month = True
            else:
                print("Error: Please enter a month between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a valid month.")

app = tkinter.Tk()
app.geometry("500x500") # Give the window a fixed size.
app.resizable(0, 0)

# Add widgets here.***
update_weather_button = Button(app, text="Update Weather Data", command="update_weather_data")
update_weather_button.place(x=75, y=100)

all_weather_data_button = Button(app, text="Get All Weather Data (15+ mins.)",
                                 command="all_weather_data")
all_weather_data_button.place(x=250, y=100)

display_box_plot_button = Button(app, text="Generate Box Plot", command="display_box_plot")
display_box_plot_button.place(x=75, y=350)

display_line_plot_button = Button(app, text="Generate Line Graph", command="display_line_plot")
display_line_plot_button.place(x=250, y=350)



app.mainloop()

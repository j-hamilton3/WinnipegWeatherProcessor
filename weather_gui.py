"""
Description: Part 2 - GUI for final project.
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March April 5, 2024
Credit:
Updates:
"""
import tkinter
from tkinter import Button, Label, messagebox, StringVar
from tkinter.simpledialog import askstring
import threading
from datetime import datetime
from plot_operations import PlotOperations
from weather_processor import WeatherProcessor
from scrape_weather import fetch_weather_data
from db_operations import DBOperations

def update_weather_data():
    """Updates the current missing weather data to the database."""
    weather_processor = WeatherProcessor()
    update_dates_return = weather_processor.update_dates()

    if not update_dates_return:
        messagebox.showinfo("Update Status", "There is no new data available. You are up to date!")
    else:
        weather_processor.update_data()
        messagebox.showinfo("Update Status", "Weather data successfully updated. :)")

def all_weather_data():
    """Starts the process of fetching and saving all weather data in a separate thread."""
    all_weather_data_button.config(state='disabled')  # Disable the button.
    threading.Thread(target=all_weather_data_thread).start()

def all_weather_data_thread():
    """Fetches and saves all weather data to the database in a background thread."""
    # Notify the user that the process has started.
    update_status.set("Fetching weather data... This will take 10+ minutes.")
    weather_data = fetch_weather_data()
    db = DBOperations()
    db.save_data(weather_data)
    # Update the status once the task is complete.
    messagebox.showinfo("Update Status", "Weather data successfully updated. :)")
    all_weather_data_button.config(state='normal') # Re enable the button.
    update_status.set("")

def get_year_input(title, message, start_year=1996):
    """Custom dialog to get year input."""
    while True:
        input_year = askstring(title, message)
        if input_year is None:
            return None
        try:
            year = int(input_year)
            if start_year <= year <= datetime.now().year:
                return year
            else:
                messagebox.showerror("Invalid Year",
                                     f"Please enter a year between" \
                                     f" {start_year} and {datetime.now().year}.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid year.")

def display_box_plot():
    """Generates a box plot of weather data based on user input."""
    starting_year = get_year_input("Starting Year", f"Please enter a starting year" \
                                    f" (between 1996-{datetime.now().year}):")
    if starting_year is None:
        return

    end_year = get_year_input("End Year",
                              f"Please enter an end year" \
                              f" (between {starting_year}-{datetime.now().year}):",
                              starting_year)
    if end_year is None:
        return

    plot = PlotOperations()
    plot.plot_temperature_boxplots(starting_year, end_year)

def display_line_plot():
    """Generates a line graph of weather data based on user input."""
    year = get_year_input("Select Year",
                          f"Please enter a year (between 1996-{datetime.now().year}):")
    if year is None:
        return  # User cancelled

    month = askstring("Select Month", "Please enter a month (between 1-12):")
    if month is None:
        return  # User cancelled

    try:
        month = int(month)
        if not 1 <= month <= 12:
            raise ValueError

        # Generate the plot.
        plot = PlotOperations()
        plot.plot_line_plot(month, year)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid month.")


app = tkinter.Tk()
app.geometry("500x500") # Give the window a fixed size.
app.resizable(0, 0)
app.title("Winnipeg Weather Processor")

update_status = StringVar(app)
update_status.set("")

status_label = Label(app, textvariable=update_status, font=("Helvetica", 10))
status_label.place(x=90, y=450)

# Main title header.
main_title_header = Label(app, text="Winnipeg Weather Processor", font=("Helvetica", 18, "bold"))
main_title_header.place(x=75, y=10)

# Headers
get_weather_data_header = Label(app, text="Get Weather Data", font=("Helvetica", 16))
get_weather_data_header.place(x=150, y=100)

get_weather_data_subheader = Label(app, text="Import scraped data from climate.weather.gc.ca.",
                                   font=("Helvetica", 10))
get_weather_data_subheader.place(x=90, y=130)


generate_graphs_header = Label(app, text="Generate Graphs", font=("Helvetica", 16))
generate_graphs_header.place(x=150, y=300)

generate_graphs_subheader = Label(app, text="Create graphs from historical weather data.",
                                  font=("Helvetica", 10))
generate_graphs_subheader.place(x=110, y=330)

# Buttons
update_weather_button = Button(app, text="Update Weather Data", command=update_weather_data)
update_weather_button.place(x=100, y=170)

all_weather_data_button = Button(app, text="Get All Weather Data",
                                 command=all_weather_data)
all_weather_data_button.place(x=250, y=170)

display_box_plot_button = Button(app, text="Generate Box Plot", command=display_box_plot)
display_box_plot_button.place(x=100, y=370)

display_line_plot_button = Button(app, text="Generate Line Graph", command=display_line_plot)
display_line_plot_button.place(x=250, y=370)

app.mainloop()

"""
Description: Part 4 - User Interaction
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March 27, 2024
Credit:
Updates:
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from hypercli import hypercli #https://github.com/HYP3R00T/hypercli
from db_operations import DBOperations
from plot_operations import PlotOperations
from scrape_weather import fetch_weather_data_by_month, fetch_weather_data

class WeatherProcessor():
    """Contains methods to facilitate user interaction with weather data."""

    def update_dates(self):
        """ UTILITY -> Returns months of available weather data."""
        # Grab the latest date of data from DB.
        db = DBOperations()
        latest_date_str = db.check_latest_data()

        latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")

        # Get yesterdays date. As user will never have todays weather data.
        yesterday = datetime.now() - timedelta(days=1)

        # Check if yesterday and latest_date are in the same month and year
        if yesterday.year == latest_date.year and yesterday.month == latest_date.month:
            if yesterday.day == latest_date.day:
                return []  # If dates are the same, return empty list
            else:
                return [yesterday.strftime("%Y-%m")]
            # If in the same month but not the same day, include the current month.

        # If yesterday is greater than the latest_date and they are not in the same month.
        months_list = []

        # Adding latest date to current date for iteration.
        current_date = latest_date

        while current_date <= yesterday:
            months_list.append(current_date.strftime("%Y-%m"))
            current_date += relativedelta(months=+1)  # Increment month by one

        return months_list # If it returns an empty list, there is no more data to update.

    def update_data(self):
        """ UTILITY -> Adds new available weather to the DB."""

        # Check dates for available data.
        dates = self.update_dates()

        # Scrape the weather for those dates.
        new_data = fetch_weather_data_by_month(dates)

        # Save the new data to the DB.
        db = DBOperations()
        db.save_data(new_data)


# *** I am using a third party module (hypercli) to render the menu. ***
# *** It cannot be nested in the WeatherProcessor class due to how it is built. ***

# Create instance of hypercli
cli = hypercli()

# Configure the instance.
cli.config["banner_text"] = "James' WeatherProcessor"
cli.config["intro_title"] = "Explore"
cli.config["intro_content"] = "Explore Winnipeg's Historical Mean Temperatures!"
cli.config["show_menu_table_header"] = True
cli.config["exit_message"] = "Run me again soon! :)"

# Add navigation options to the menu.
cli.link("Main Menu", "Update Weather Data.")
cli.link("Main Menu", "Generate Graphs.")

@cli.entry(menu="Update Weather Data.", option="Update Weather Data.")
def update_weather_data():
    """Updates the current missing weather data to the database."""
    # Logic for seeing if data needs to be updated.
    weather_processor = WeatherProcessor()
    update_dates_return = weather_processor.update_dates()

    if not update_dates_return :
        print("There is no new data available. You are up to date!")
        print()
        input("Press enter to exit...")
        cli.exit()
    else:
        weather_processor.update_data()
        print("Weather data successfully updated. :)")
        print()
        input("Press enter to exit...")
        cli.exit()

@cli.entry(menu="Update Weather Data.", option="Download All Weather Data. (10+ mins)")
def all_weather_data():
    """Fetches and saves all weather data to the database."""
    print("Fetching weather data...")
    weather_data = fetch_weather_data()
    db = DBOperations()
    db.save_data(weather_data)
    print("Weather data successfully updated. :)")
    print()
    input("Press enter to exit...")
    cli.exit()

@cli.entry(menu="Generate Graphs.", option="Generate a Box Plot.")
def display_box_plot():
    """Generates a box plot of weather data based on user input."""
    # Get the current year from datetime.
    current_year = datetime.now().year

    starting_year = int(input(f"Please enter a starting year (between 1996-{current_year}): "))
    end_year = int(input(f"Please enter an end year (between 1996-{current_year}): "))

    # Generate the plot.
    plot = PlotOperations()
    plot.plot_temperature_boxplots(starting_year, end_year)

    print("Box plot successfully generated.")
    print()
    input("Press enter to exit...")
    cli.exit()

@cli.entry(menu="Generate Graphs.", option="Generate a Line Graph.")
def display_line_plot():
    """Generates a line graph of weather data based on user input."""
    # Get the current year from datetime.
    current_year = datetime.now().year

    year = int(input(f"Please enter a year (between 1996-{current_year}): "))
    month = int(input("Please enter a month(between 1-12): "))

    # Generate the plot.
    plot = PlotOperations()
    plot.plot_line_plot(month, year)

    print("Line plot successfully generated.")
    print()
    input("Press enter to exit...")
    cli.exit()

# Run the cli.
cli.run()

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
from menu import Menu
from db_operations import DBOperations
from scrape_weather import fetch_weather_data_by_month

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

# TEST
# Logic for seeing if data needs to be updated.
#weather_processor = WeatherProcessor()
#update_dates_return = weather_processor.update_dates()

#if not update_dates_return :
    #print("There is no new data available.")
#else:
    #weather_processor.update_data()

weather = WeatherProcessor()

main_menu_options = [("Update weather data.", Menu.CLOSE), \
                     ("Download all weather data. (10+ minutes)", Menu.CLOSE), \
                     ("Generate a box plot.", Menu.CLOSE), \
                     ("Generate a line plot.", Menu.CLOSE), \
                     ("Exit.", Menu.CLOSE)]

main_menu = Menu (
    message = "Welcome to James' WeatherProcessor." \
               " \n** Explore Winnipeg's historical temperature data! **",
    options = main_menu_options
)

main_menu.open()

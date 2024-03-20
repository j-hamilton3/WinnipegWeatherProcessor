"""
Description: A Weather Scraper created for Milestone 1.
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March 20th, 2024
Credit:
Updates:
"""
from datetime import datetime

# Get the current date and time.
now = datetime.now()

current_year = now.year
current_month = now.month
current_day = now.day
print(f"Year: {current_year}, Month: {current_month}, Day: {current_day}")

starting_url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174" \
               f"&timeframe=2&StartYear=1840&EndYear={current_year}&Day={current_day}&" \
               f"Year={current_year}&Month={current_month}"

print(starting_url)

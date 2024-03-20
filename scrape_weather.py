"""
Description: A Weather Scraper created for Milestone 1.
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March 20th, 2024
Credit:
Updates:
"""
from datetime import datetime
from html.parser import HTMLParser
import urllib.request
import re

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

# HTMLParser class.
class ScrapeWeatherParser(HTMLParser):
    """An HTMLParser class used to parse weather data."""

    def __init__(self):
        super().__init__()
        self.weather = {}
        self.current_date = ""
        self.tbody_flag = False
        self.th_flag = False
        self.td_flag = False
        self.abbr_flag = False

    def handle_starttag(self, tag, attrs) :
        if tag == "tbody":
            self.tbody_flag = True
        if tag == "th":
            self.th_flag = True
        if tag == "td":
            self.td_flag = True
        if tag == "abbr":
            self.abbr_flag = True
            for name, value in attrs:
                if name == "title":
                    # Regex to check the title value matches a date format.
                    if re.match(r"January|February|March|April|May|June|" \
                                r"July|August|September|October|November|December", value):
                        # If it matches, convert into the correct format.
                        date_obj = datetime.strptime(value, "%B %d, %Y")
                        formatted_date = date_obj.strftime("%Y-%m-%d")
                        # Add the date as a key to the weather dictonary.
                        self.current_date = formatted_date
                        self.weather[self.current_date] = {"Max": None, "Min": None, "Mean": None}
                    else:
                        # Reset the current_date if title is not in a correct format.
                        self.current_date = ""

    def handle_endtag(self, tag) :
        if tag == "tbody":
            self.tbody_flag = False
        if tag == "th":
            self.th_flag = False
        if tag == "td":
            self.td_flag = False
        if tag == "abbr":
            self.abbr_flag = False

    def handle_data(self, data) :
        if self.tbody_flag and self.td_flag and self.current_date:
            pass


    def get_weather(self) :
        """Returns the dictonary of the weather data."""
        return self.weather


weather_parser = ScrapeWeatherParser()

with urllib.request.urlopen(starting_url) as response:
    HTML = str(response.read())

weather_parser.feed(HTML)

weather_dict = weather_parser.get_weather()

print(weather_dict)

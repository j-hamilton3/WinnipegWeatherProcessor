"""
Description: A Weather Scraper created for Milestone 1.
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March 20th, 2024
Credit:
     OpenAI. (2024). ChatGPT (April 2023 version) [Large language model].
     This work was supported in part by assistance from ChatGPT,
     an AI language model developed by OpenAI.  https://chat.openai.com/chat
     This AI was used to generate ideas, and help format logic. No code was copy-pasted.
Updates:
"""
from datetime import datetime
from html.parser import HTMLParser
import urllib.request
import re

# HTMLParser class.
class ScrapeWeatherParser(HTMLParser):
    """An HTMLParser class used to parse weather data."""

    def __init__(self):
        super().__init__()
        self.weather = {}
        self.current_date = ""
        self.td_count = 0 # This keeps track of how many tds are encountered.

    def handle_starttag(self, tag, attrs) :
        if tag == "th":
            self.td_count = 0 # Reset count to zero when a new th is encountered.
        if tag == "td":
            self.td_count += 1 # Add to the counter at each td.
        if tag == "abbr":
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
                        # Define the nested dictionary separately.
                        daily_temps_init = {"daily_temps": {"Max": None, "Min": None, "Mean": None}}
                        # Assign it to the current date in the weather dictionary.
                        self.weather[self.current_date] = daily_temps_init
                    else:
                        # Reset the current_date if title is not in a correct format.
                        self.current_date = ""

    def handle_data(self, data) :
        try:
            # Attempt to convert the cleaned data to a float.
            # If conversion succeeds and we're in the right td element.
            # We only want the first three tds.
            if self.current_date and self.td_count in [1, 2, 3]:
                # Trim whitespace and replace non-breaking spaces.
                clean_data = data.strip().replace('\xa0', '')
                temp_value = float(clean_data)
                temps = self.weather[self.current_date]["daily_temps"]
                if self.td_count == 1:
                    temps["Max"] = temp_value
                elif self.td_count == 2:
                    temps["Min"] = temp_value
                elif self.td_count == 3:
                    temps["Mean"] = temp_value
        except ValueError:
            pass # Maybe log the error later on...

    def get_previous_month(self, year, month):
        """Return the year and month for the previous month."""
        if month == 1:
            return year - 1, 12
        else:
            return year, month - 1

    def get_weather(self) :
        """Returns the dictonary of the weather data."""
        return self.weather

    def fetch_weather_data(self):
        """Returns weather data from the current day until the earliest recorded date."""
        weather_parser = ScrapeWeatherParser()
        now = datetime.now()
        current_year = now.year #-26 # Change as needed for speed.
        current_month = now.month
        last_data_snapshot = None
        all_weather_data = {}

        while True:
            # Generate the URL for the current month and year
            url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174" \
                  f"&timeframe=2&StartYear=1840&EndYear={current_year}&Day=1&Year={current_year}" \
                  f"&Month={current_month}"
            print(f"Fetching data for {current_year}-{current_month}")

            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')
                # Reset the parser for a new month's data.
                weather_parser = ScrapeWeatherParser()
                weather_parser.feed(html)

            current_weather = weather_parser.get_weather()

            # Proceed if no data for the current month or if it's the first iteration.
            if not current_weather:
                print(f"No data for {current_year}-{current_month}," \
                      f"continuing to previous month...")
            # Stop if we have data and it's identical to the last snapshot (and not empty).
            elif current_weather == last_data_snapshot and current_weather:
                print("Duplicate non-empty data found, stopping...")
                break
            else:
                # Update the last data snapshot for the next iteration's comparison.
                last_data_snapshot = current_weather
                # Add the current months data to the collection.
                all_weather_data.update(current_weather)

            # Update to the previous month
            current_year, current_month = self.get_previous_month(current_year, current_month)

        return all_weather_data # Return all weather data.

# TESTING
if __name__ == "__main__":
    # Instantiating and using the parser.
    weather_scraper = ScrapeWeatherParser()

    weather_data = weather_scraper.fetch_weather_data()

    print(weather_data)

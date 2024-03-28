"""
Description: Part 3 - Plotting
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March 26, 2024
Credit:
Updates:
"""
from datetime import datetime
import matplotlib.pyplot as plt
from db_operations import DBOperations

class PlotOperations():
    """Contains operations for graphing weather data."""
    def __init__(self):
        # Get data upon instantiation.
        db = DBOperations()
        self.data = db.fetch_data()

    def filter_by_year(self, start_year, end_year, all_data):
        """Filters weather data by range of years (inclusive)."""
        # Function to extract year from date string.
        def get_year(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').year

        # Filter data to only include records within the specified year range.
        filtered_data = [record for record in all_data if start_year <= get_year(record[0])
                         <= end_year]
        return filtered_data

    def filter_by_month(self, month, year, all_data):
        """Filters data to include only records from a specific month and year."""
        # Function to check if a record's date matches the specified month and year.
        def is_match(date_str, year, month):
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.year == year and date_obj.month == month

        # Filter data to only include records from the specified month and year.
        filtered_data = [record for record in all_data if is_match(record[0], year, month)]
        return filtered_data

    def convert_to_dict(self, to_convert):
        """Converts weather data to a dictionary of lists."""
        converted_dict = {}

        for record in to_convert:
            date_str = record[0]
            mean_temp = record[4]

            # Get the month from date_str.
            month = datetime.strptime(date_str, '%Y-%m-%d').month

            if month not in converted_dict:
                converted_dict[month] = []

            converted_dict[month].append(mean_temp)

        return converted_dict

    def plot_temperature_boxplots(self, start_year, end_year):
        """Generates a boxplot of monthly temperature distributions."""
        unfiltered_weather_data = self.data
        # Filter data by year.
        filtered_year_data = self.filter_by_year(start_year, end_year, unfiltered_weather_data)
        #Conver to dictionary.
        weather_data = self.convert_to_dict(filtered_year_data)
        # Extract months and temperatures
        months = list(weather_data.keys())
        # Filter out None data.
        temperatures = [[temp for temp in weather_data[month] if temp is not None]
                        for month in months]

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.boxplot(temperatures, labels=months)
        plt.title(f'Monthly Temperature Distribution for: {start_year} to {end_year}')
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')
        plt.show()

    def plot_line_plot(self, month, year):
        """Generates a line plot for daily mean temperatures of a specific month and year."""
        weather_data = self.data

        # Use the filter_by_month function to get data for the specified month and year
        filtered_by_month = self.filter_by_month(month, year, weather_data)

        # Extract dates and mean temperatures from the filtered data
        dates = [datetime.strptime(record[0], '%Y-%m-%d').date() for record in filtered_by_month]
        mean_temperatures = [record[4] for record in filtered_by_month]

        # Plotting
        plt.figure(figsize=(15, 9))
        plt.plot(dates, mean_temperatures)
        plt.title(f'Daily Avg Temperatures for {year}-{month:02d}')
        plt.xlabel('Day of Month')
        plt.ylabel('Avg Daily Temp')
        plt.xticks(dates, rotation=45)
        plt.grid(True)
        plt.show()


# TESTING
if __name__ == "__main__":
    plot = PlotOperations()

    # Test Displaying boxplot.
    plot.plot_temperature_boxplots(2000, 2017)

    # Test Displaying lineplot.
    plot.plot_line_plot(3, 2020)

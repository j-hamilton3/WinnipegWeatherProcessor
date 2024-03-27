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

# Getting ALL the data from the DB.
db = DBOperations()
data = db.fetch_data()

# Date range for the boxplot.
START_YEAR = 2000
END_YEAR = 2002

def filter_by_year(start_year, end_year, all_data):
    """Filters weather data by range of years (inclusive)."""
    # Function to extract year from date string
    def get_year(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').year

    # Filter data to only include records within the specified year range
    filtered_data = [record for record in all_data if start_year <= get_year(record[0]) <= end_year]
    return filtered_data

# Test the filter function.
filtered_date_data = filter_by_year(START_YEAR, END_YEAR, data)
#print(filtered_date_data)

# Convert data into a dictionary of lists.
def convert_to_dict(to_convert):
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

# Test the convert_to_dict function.
print(convert_to_dict(filtered_date_data))


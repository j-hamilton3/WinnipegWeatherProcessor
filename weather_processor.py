"""
Description: Part 4 - User Interaction
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March 27, 2024
Credit:
Updates:
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from db_operations import DBOperations

def update_dates():
    """Returns months of available weather data."""
    # Grab latest date of data from DB.
    db = DBOperations()
    latest_date_str = db.check_latest_data()

    latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")

    today = datetime.now()

    # Check if today and latest_date are in the same month and year.
    if today.year == latest_date.year and today.month == latest_date.month:
        if today == latest_date:
            return []  # If dates are the same, return empty list.
        else:
            return [today.strftime("%Y-%m")]
        # If in the same month but not the same day, include the current month.

    # If today is greater than the latest_date and they are not in the same month.
    months_list = []

    # Adding latest date to current date for iteration.
    current_date = latest_date

    while current_date <= today:
        months_list.append(current_date.strftime("%Y-%m"))
        current_date += relativedelta(months=+1)  # Increment month by one.

    return months_list

# TEST
print(update_dates())

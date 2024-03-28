"""
Description: Part 2 - Database for Final Project.
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March 25th, 2024
Credit:
Updates:
"""


import sqlite3
from scrape_weather import fetch_weather_data
from dbcm import DBCM

class DBOperations():
    """Defines various database functions."""

    def __init__(self):
        self.db_name = "weather.sqlite"

        self.initialize_db() # Runs everytime!

    def initialize_db(self):
        """Initializes the database."""
        with DBCM(self.db_name) as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS weather
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sample_date TEXT,
                        location TEXT,
                        max_temp REAL,
                        min_temp REAL,
                        avg_temp REAL,
                        UNIQUE(sample_date, location))""")

    def purge_data(self):
        """Deletes all the data in the DB."""
        with DBCM(self.db_name) as cur:
            cur.execute("DELETE FROM weather")
            print("Data deleted from weather.")

    def save_data(self, weather_dict):
        """Saves new data to the DB."""
        location = "Winnipeg, Manitoba"
        with DBCM(self.db_name) as cur:
            for date, data in weather_dict.items():
                max_temp = data['daily_temps']['Max']
                min_temp = data['daily_temps']['Min']
                mean_temp = data['daily_temps']['Mean']
                try:
                    cur.execute("""INSERT INTO weather
                                    (sample_date, location, max_temp, min_temp, avg_temp)
                                    VALUES (?, ?, ?, ?, ?)""",
                                    (date, location, max_temp, min_temp, mean_temp))
                except sqlite3.IntegrityError:
                    pass

    def check_latest_data(self):
        """Finds the latest date of DB data for updating purposes."""
        with DBCM(self.db_name) as cur:
            cur.execute("""SELECT MAX(sample_date) FROM weather""")
            result = cur.fetchone()[0]

        return result

    def fetch_data(self):
        """Returns requested data for plotting."""
        with DBCM(self.db_name) as cur:
            cur.execute("""SELECT sample_date, location, max_temp, min_temp, avg_temp
                            FROM weather
                            ORDER BY sample_date""")
            rows = cur.fetchall()
            return rows


# TESTING
if __name__ == "__main__":
    # Gets the dictionary of weather data from the external module.
    weather_data = fetch_weather_data()

    db = DBOperations()
    db.purge_data()
    db.save_data(weather_data)

    # Returns the data for plotting.
    print(db.fetch_data())

    print("Latest data in DB: " + db.check_latest_data())

"""
Description: Part 2 - Database Context Manager for Final Project.
Author: James Hamilton
Section Number: ADEV-3005, N. Cai, FTO01
Date Created: March 26th, 2024
Credit:
Updates:
"""

import sqlite3

class DBCM:
    """DB context manager for the weather data."""
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.conn.commit()
        self.conn.close()

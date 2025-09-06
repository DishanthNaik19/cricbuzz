# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 05:50:39 2025

@author: Dishanth
"""

import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",          # replace with your MySQL username
        password="qwerty123456@#$", # replace with your MySQL password
        database="cricbuzz"
    )

def run_query(query, params=None, fetch=True):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    if fetch:
        result = cursor.fetchall()
        df = pd.DataFrame(result)
    else:
        conn.commit()
        df = None
    cursor.close()
    conn.close()
    return df


if __name__ == "__main__":
    df = run_query("SELECT * FROM teams;")
    print(df)

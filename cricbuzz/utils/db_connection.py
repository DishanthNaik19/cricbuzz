# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 05:50:39 2025

@author: Dishanth
"""
import mysql.connector
import streamlit as st

# Use Streamlit cache to reuse connections (avoids reconnecting every run)
@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",        # use 127.0.0.1 instead of localhost
            user="root",             # your MySQL username
            password="qwerty123456@#$",  # your MySQL password
            database="cricbuzz",     # your database name
            port=3306
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        return None


def run_query(query, params=None, fetch=True):
    conn = get_connection()
    if conn is None:
        return None
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    
    if fetch:
        result = cursor.fetchall()
        cursor.close()
        return result
    else:
        conn.commit()
        cursor.close()
        return None



if __name__ == "__main__":
    df = run_query("SELECT * FROM teams;")
    print(df)

# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 06:01:28 2025

@author: Dishanth
"""
import streamlit as st
import pandas as pd
from utils.db_connection import run_query
from queries_dict import queries

# ================================
# Page Configuration
# ================================
st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")

# Sidebar navigation
st.sidebar.title(" Cricbuzz LiveStats")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Live Matches", "Top Players", "SQL Queries", "CRUD Operations"]
)

# ================================
# Home Page
# ================================
if page == "Home":
    st.title(" Cricbuzz LiveStats Dashboard")
    st.write("Welcome! Explore cricket data with **MySQL + Streamlit + Cricbuzz API**.")
    st.info("Use the sidebar to navigate between modules.")

# ================================
# Live Matches Page
# ================================
elif page == "Live Matches":
    st.title(" Live Match Updates")

    try:
        from pyCricbuzz import Cricbuzz
        c = Cricbuzz()
        matches = c.matches()

        if matches:
            st.success(f"Found {len(matches)} live/ongoing matches")
            for match in matches:
                st.subheader(f"{match['team1']['name']} vs {match['team2']['name']}")
                st.write(f"Series: {match['srs']}")
                st.write(f"Match: {match['mnum']}")
                st.write(f"Status: {match['status']}")
                if 'score' in match:
                    for s in match['score']:
                        st.write(f"Innings: {s['inning']}, Score: {s['runs']}/{s['wickets']} in {s['overs']} overs")
        else:
            st.info("No live matches at the moment.")
    except Exception as e:
        st.error(f" Error fetching live matches: {str(e)}")

# ================================
# Top Players Page
# ================================
elif page == "Top Players":
    st.title(" Top Player Stats")

    option = st.radio("Choose a stat", ["Top Run Scorers", "Top Wicket Takers"])

    if option == "Top Run Scorers":
        df = run_query("""
            SELECT p.full_name, ps.runs_scored, ps.batting_average, ps.centuries
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE ps.format='ODI'
            ORDER BY ps.runs_scored DESC
            LIMIT 5;
        """)
        st.subheader(" Top 5 Run Scorers (ODI)")
        st.dataframe(df, use_container_width=True)

    elif option == "Top Wicket Takers":
        df = run_query("""
            SELECT p.full_name, ps.wickets_taken, ps.bowling_average, ps.economy_rate
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE ps.format='ODI'
            ORDER BY ps.wickets_taken DESC
            LIMIT 5;
        """)
        st.subheader(" Top 5 Wicket Takers (ODI)")
        st.dataframe(df, use_container_width=True)

# ================================
# SQL Queries Page
# ================================
elif page == "SQL Queries":
    st.title(" SQL Analytics")
    st.write("Explore cricket data using **25 predefined SQL queries**.")

    choice = st.selectbox(" Choose a query", list(queries.keys()))

    tab1, tab2 = st.tabs([" Query Description", " Results"])

    with tab1:
        st.subheader(" Query Details")
        st.code(queries[choice], language="sql")

    with tab2:
        if st.button("▶️ Run Query"):
            try:
                df = run_query(queries[choice])
                if df is not None and not df.empty:
                    st.dataframe(df, use_container_width=True)

                    # CSV download
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label=" Download Results as CSV",
                        data=csv,
                        file_name=f"{choice.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info(" No results found for this query.")
            except Exception as e:
                st.error(f" Error running query: {str(e)}")

# ================================
# CRUD Operations Page
# ================================
elif page == "CRUD Operations":
    st.title(" Manage Data")
    st.write("Perform **Create, Read, Update, Delete (CRUD)** operations on Players and Teams.")

    crud_choice = st.radio("Choose a table to manage:", ["Players", "Teams"])

    # ----------------------------
    # Manage Players
    # ----------------------------
    if crud_choice == "Players":
        st.subheader(" Player Management")
        action = st.selectbox("Action", ["Add", "Update", "Delete", "View All"])

        if action == "Add":
            with st.form("add_player"):
                full_name = st.text_input("Full Name")
                playing_role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
                batting_style = st.text_input("Batting Style")
                bowling_style = st.text_input("Bowling Style")
                team_id = st.number_input("Team ID", min_value=1, step=1)
                submitted = st.form_submit_button("Add Player")
                if submitted:
                    query = """
                        INSERT INTO players (full_name, playing_role, batting_style, bowling_style, team_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    run_query(query, (full_name, playing_role, batting_style, bowling_style, team_id), fetch=False)
                    st.success(f" Player '{full_name}' added successfully.")

        elif action == "Update":
            player_id = st.number_input("Enter Player ID to update", min_value=1, step=1)
            with st.form("update_player"):
                new_name = st.text_input("New Full Name")
                new_role = st.selectbox("New Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
                new_batting = st.text_input("New Batting Style")
                new_bowling = st.text_input("New Bowling Style")
                new_team = st.number_input("New Team ID", min_value=1, step=1)
                submitted = st.form_submit_button("Update Player")
                if submitted:
                    query = """
                        UPDATE players
                        SET full_name=%s, playing_role=%s, batting_style=%s, bowling_style=%s, team_id=%s
                        WHERE player_id=%s
                    """
                    run_query(query, (new_name, new_role, new_batting, new_bowling, new_team, player_id), fetch=False)
                    st.success(f" Player ID {player_id} updated successfully.")

        elif action == "Delete":
            player_id = st.number_input("Enter Player ID to delete", min_value=1, step=1)
            if st.button("Delete Player"):
                run_query("DELETE FROM players WHERE player_id=%s", (player_id,), fetch=False)
                st.warning(f"🗑️ Player ID {player_id} deleted.")

        elif action == "View All":
            df = run_query("SELECT * FROM players")
            st.dataframe(df, use_container_width=True)

    # ----------------------------
    # Manage Teams
    # ----------------------------
    elif crud_choice == "Teams":
        st.subheader(" Team Management")
        action = st.selectbox("Action", ["Add", "Update", "Delete", "View All"])

        if action == "Add":
            with st.form("add_team"):
                team_name = st.text_input("Team Name")
                country = st.text_input("Country")
                submitted = st.form_submit_button("Add Team")
                if submitted:
                    run_query("INSERT INTO teams (team_name, country) VALUES (%s, %s)", 
                              (team_name, country), fetch=False)
                    st.success(f" Team '{team_name}' added successfully.")

        elif action == "Update":
            team_id = st.number_input("Enter Team ID to update", min_value=1, step=1)
            with st.form("update_team"):
                new_name = st.text_input("New Team Name")
                new_country = st.text_input("New Country")
                submitted = st.form_submit_button("Update Team")
                if submitted:
                    run_query("UPDATE teams SET team_name=%s, country=%s WHERE team_id=%s", 
                              (new_name, new_country, team_id), fetch=False)
                    st.success(f" Team ID {team_id} updated successfully.")

        elif action == "Delete":
            team_id = st.number_input("Enter Team ID to delete", min_value=1, step=1)
            if st.button("Delete Team"):
                run_query("DELETE FROM teams WHERE team_id=%s", (team_id,), fetch=False)
                st.warning(f" Team ID {team_id} deleted.")

        elif action == "View All":
            df = run_query("SELECT * FROM teams")
            st.dataframe(df, use_container_width=True)

  
     
       
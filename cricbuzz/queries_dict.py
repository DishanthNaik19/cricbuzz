# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 06:38:58 2025

@author: Dishanth
"""

queries = {
        "Q1: Players from India": """
            SELECT p.full_name, p.playing_role, p.batting_style, p.bowling_style
            FROM players p
            JOIN teams t ON p.team_id = t.team_id
            WHERE t.team_name = 'India';
        """,
        "Q2: Matches in last 30 days": """
            SELECT match_description, match_date
            FROM matches
            WHERE match_date >= CURDATE() - INTERVAL 30 DAY
            ORDER BY match_date DESC;
        """,
        "Q3: Top 10 run scorers (ODI)": """
            SELECT p.full_name, ps.runs_scored, ps.batting_average, ps.centuries
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE ps.format = 'ODI'
            ORDER BY ps.runs_scored DESC
            LIMIT 10;
        """,

    "Q4: Venues with capacity > 50,000": """
        SELECT venue_name, city, country, capacity
        FROM venues
        WHERE capacity > 50000
        ORDER BY capacity DESC;
    """,

    "Q5: Matches each team has won": """
        SELECT t.team_name, COUNT(*) AS total_wins
        FROM matches m
        JOIN teams t ON m.result LIKE CONCAT(t.team_name, '%')
        GROUP BY t.team_name
        ORDER BY total_wins DESC;
    """,

    "Q6: Count of players per role": """
        SELECT playing_role, COUNT(*) AS total_players
        FROM players
        GROUP BY playing_role;
    """,

    "Q7: Highest score in each format": """
        SELECT format, MAX(runs_scored) AS highest_score
        FROM player_stats
        GROUP BY format;
    """,

    "Q8: Series started in 2024": """
        SELECT series_name, host_country, match_type, start_date, total_matches
        FROM series
        WHERE YEAR(start_date) = 2024;
    """,

    # Intermediate Level
    "Q9: All-rounders with >1000 runs & >50 wickets": """
        SELECT p.full_name, ps.runs_scored, ps.wickets_taken, ps.format
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE playing_role = 'All-rounder'
          AND ps.runs_scored > 1000 
          AND ps.wickets_taken > 50;
    """,

    "Q10: Last 20 completed matches": """
        SELECT match_description,
               (SELECT team_name FROM teams WHERE team_id = m.team1_id) AS Team1,
               (SELECT team_name FROM teams WHERE team_id = m.team2_id) AS Team2,
               result, match_date
        FROM matches m
        ORDER BY match_date DESC
        LIMIT 20;
    """,

    "Q11: Compare player runs across formats": """
        SELECT p.full_name,
               SUM(CASE WHEN ps.format = 'Test' THEN ps.runs_scored ELSE 0 END) AS Test_Runs,
               SUM(CASE WHEN ps.format = 'ODI' THEN ps.runs_scored ELSE 0 END) AS ODI_Runs,
               SUM(CASE WHEN ps.format = 'T20I' THEN ps.runs_scored ELSE 0 END) AS T20_Runs,
               AVG(ps.batting_average) AS Overall_Avg
        FROM players p
        JOIN player_stats ps ON p.player_id = ps.player_id
        GROUP BY p.full_name
        HAVING COUNT(DISTINCT ps.format) >= 2;
    """,

    "Q12: Team performance Home vs Away": """
        SELECT t.team_name,
               SUM(CASE WHEN v.country = t.country AND m.result LIKE CONCAT(t.team_name, '%') THEN 1 ELSE 0 END) AS Home_Wins,
               SUM(CASE WHEN v.country <> t.country AND m.result LIKE CONCAT(t.team_name, '%') THEN 1 ELSE 0 END) AS Away_Wins
        FROM matches m
        JOIN teams t ON t.team_id IN (m.team1_id, m.team2_id)
        JOIN venues v ON m.venue_id = v.venue_id
        GROUP BY t.team_name;
    """,

    "Q13: Batting partnerships >100 runs (simplified)": """
        SELECT 'Partnership analysis requires ball-by-ball data (not in current schema)' AS Note;
    """,

    "Q14: Bowling performance at venues": """
        SELECT p.full_name, v.venue_name,
               AVG(ps.economy_rate) AS avg_economy,
               SUM(ps.wickets_taken) AS total_wickets,
               COUNT(*) AS matches_played
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        JOIN matches m ON m.venue_id IS NOT NULL
        JOIN venues v ON m.venue_id = v.venue_id
        WHERE ps.wickets_taken > 0
        GROUP BY p.full_name, v.venue_name;
    """,

    "Q15: Player performance in close matches (simplified)": """
        SELECT 'Close match analysis needs margin details (not fully in current schema)' AS Note;
    """,

    "Q16: Player performance year-wise": """
        SELECT p.full_name, YEAR(m.match_date) AS Year,
               AVG(ps.runs_scored) AS Avg_Runs,
               AVG(ps.strike_rate) AS Avg_SR
        FROM players p
        JOIN player_stats ps ON p.player_id = ps.player_id
        JOIN matches m ON YEAR(m.match_date) >= 2020
        GROUP BY p.full_name, Year
        HAVING COUNT(m.match_id) >= 5;
    """,

    # Advanced Level
    "Q17: Toss advantage (requires toss data)": """
        SELECT 'Toss winner data not available in schema' AS Note;
    """,

    "Q18: Most economical bowlers (ODI & T20)": """
        SELECT p.full_name, AVG(ps.economy_rate) AS Economy, SUM(ps.wickets_taken) AS Wickets
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.format IN ('ODI', 'T20I')
        GROUP BY p.full_name
        HAVING COUNT(*) >= 10
        ORDER BY Economy ASC;
    """,

    "Q19: Consistent batsmen (StdDev of runs)": """
        SELECT p.full_name, AVG(ps.runs_scored) AS Avg_Runs, STDDEV(ps.runs_scored) AS StdDev
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.runs_scored IS NOT NULL
        GROUP BY p.full_name
        HAVING COUNT(*) >= 5
        ORDER BY StdDev ASC;
    """,

    "Q20: Matches played & batting averages": """
        SELECT p.full_name,
               SUM(CASE WHEN ps.format='Test' THEN ps.matches_played ELSE 0 END) AS Test_Matches,
               SUM(CASE WHEN ps.format='ODI' THEN ps.matches_played ELSE 0 END) AS ODI_Matches,
               SUM(CASE WHEN ps.format='T20I' THEN ps.matches_played ELSE 0 END) AS T20_Matches,
               AVG(ps.batting_average) AS Avg_Batting
        FROM players p
        JOIN player_stats ps ON p.player_id = ps.player_id
        GROUP BY p.full_name
        HAVING (Test_Matches + ODI_Matches + T20_Matches) >= 20;
    """,

    "Q21: Performance ranking system": """
        SELECT p.full_name,
               (ps.runs_scored*0.01 + ps.batting_average*0.5 + ps.strike_rate*0.3) +
               (ps.wickets_taken*2 + (50-IFNULL(ps.bowling_average,50))*0.5 + ((6-IFNULL(ps.economy_rate,6))*2)) AS Performance_Score
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        ORDER BY Performance_Score DESC;
    """,

    "Q22: Head-to-head match analysis": """
        SELECT t1.team_name AS Team1, t2.team_name AS Team2,
               COUNT(*) AS Matches_Played
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        GROUP BY Team1, Team2
        HAVING Matches_Played >= 1;
    """,

    "Q23: Recent player form (needs last 10 innings)": """
        SELECT 'Requires detailed match-by-match data (not in schema)' AS Note;
    """,

    "Q24: Successful batting partnerships": """
        SELECT 'Partnership analysis requires batting order data (not in schema)' AS Note;
    """,

    "Q25: Time-series performance evolution": """
        SELECT p.full_name, YEAR(m.match_date) AS Year,
               AVG(ps.runs_scored) AS Avg_Runs, AVG(ps.strike_rate) AS Avg_SR
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        JOIN matches m ON m.match_id > 0
        GROUP BY p.full_name, YEAR(m.match_date);
    """
}
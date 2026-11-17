from src.data_processing import (load_matches, get_team_matches, 
get_league_matches, get_upcoming_matches, run_data_quality_checks)

# Explore data
matches = load_matches()
print("\n--- Data overview ---")
print(matches.info())

rapid_matches = get_team_matches(matches, "Rapid Wien")
austria_matches = get_team_matches(matches, "Austria Wien")

print("\n--- Rapid Wien matches ---")
print(rapid_matches[["home_team", "away_team", "date", "kickoff"]])

bundesliga_matches = get_league_matches(matches, "Bundesliga")
print("\n--- Bundesliga matches ---")
print(bundesliga_matches[["home_team", "away_team", "date", "kickoff"]])

upcoming_matches = get_upcoming_matches(matches)
print("\n--- Upcoming matches in the next 7 days ---")
print(upcoming_matches[["home_team", "away_team", "date", "kickoff"]])

run_data_quality_checks(matches)
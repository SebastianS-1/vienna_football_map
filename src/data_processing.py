import pandas as pd

# Load + prepare data
def load_matches():
    matches = pd.read_csv("data/matches.csv")
    matches["date"] = pd.to_datetime(matches["date"])
    matches["kickoff"] = pd.to_datetime(matches["kickoff"], format="%H:%M").dt.time
    matches = matches.sort_values("date")
    return matches

# Get matches for a specific team + league
def get_team_matches(matches, team):
    team_matches = matches[(matches["home_team"] == team) | (matches["away_team"] == team)]
    return team_matches.sort_values("date")

def get_league_matches(matches, league):
    league_matches = matches[matches["league"] == league]
    return league_matches.sort_values("date")

# get upcoming matches
def get_upcoming_matches(matches, days=7):
    today = pd.Timestamp.today().normalize()
    end_date = today + pd.Timedelta(days=days)
    upcoming_matches = matches[(matches["date"] >= today) & (matches["date"] <= end_date)]
    return upcoming_matches.sort_values("date")

# data quality checks
def check_missing_values(matches):
    missing_values = matches.isnull().sum()
    return missing_values
def get_duplicate_matches(matches):
    duplicate_count =matches.duplicated(subset=["date", "home_team",
                         "away_team", "kickoff"], keep=False).sum()
    return duplicate_count
def check_coordinates(matches):
    outliers= matches[(matches["latitude"] < -90.0) | 
                      (matches["latitude"] > 90.0) | 
                      (matches["longitude"] < -180.0) | 
                      (matches["longitude"] > 180.0)]
    return outliers

def run_data_quality_checks(matches):
    missing_values = check_missing_values(matches)
    duplicate_count =get_duplicate_matches(matches)
    outliers= check_coordinates(matches)
    print("\n--- Data quality checks ---")
    print("\n--- Missing values ---")
    print(missing_values)
    print("\n--- Duplicate matches ---")
    print(f"Number of duplicate matches: {duplicate_count}")
    print("\n--- Outliers in coordinates ---")
    print(outliers)
    return missing_values, duplicate_count, outliers

def prepare_matches_for_map(matches):
    valid_coordinates = matches[(matches["latitude"] >= -90.0) &
                                (matches["latitude"] <= 90.0) &
                                (matches["longitude"] >= -180.0) &
                                (matches["longitude"] <= 180.0)]
    map_matches = valid_coordinates[
        ["date", "kickoff", "home_team", "away_team",
         "stadium", "latitude", "longitude"]
    ].copy()
    return map_matches
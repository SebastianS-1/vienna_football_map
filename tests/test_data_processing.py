import pandas as pd

from src.data_processing import (get_team_matches, get_upcoming_matches,
                                  check_coordinates, get_duplicate_matches,
                                  check_missing_values, run_data_quality_checks)


def test_get_team_matches():

    test_data = pd.DataFrame({
        "home_team": ["Rapid Wien", "Austria Wien", "Sturm Graz"],
        "away_team": ["Sturm Graz", "Rapid Wien", "LASK"],
        "date": pd.to_datetime([
            "2026-11-21",
            "2026-11-22",
            "2026-11-28"
        ])
    })

    result = get_team_matches(test_data, "Rapid Wien")

    assert len(result) == 2

    assert (
        (result["home_team"] == "Rapid Wien") |
        (result["away_team"] == "Rapid Wien")
        ).all()

def test_get_team_matches_no_results():
    test_data = pd.DataFrame({
        "home_team": ["Rapid Wien", "Austria Wien", "Sturm Graz"],
        "away_team": ["Sturm Graz", "Rapid Wien", "LASK"],
        "date": pd.to_datetime([
            "2026-11-21",
            "2026-11-22",
            "2026-11-28"
        ])
    })

    result = get_team_matches(test_data, "FC Barcelona")

    assert result.empty

def test_get_upcoming_matches():
    today = pd.Timestamp.today().normalize()

    test_data = pd.DataFrame({
        "date": [
            today - pd.Timedelta(days=1),
            today + pd.Timedelta(days=2),
            today + pd.Timedelta(days=5),
            today + pd.Timedelta(days=10)
        ]
    })

    result = get_upcoming_matches(test_data, days=7)

    assert len(result) == 2
    assert (((result["date"] >= today).all()) & 
            ((result["date"] <= today + pd.Timedelta(days=7)).all()))

def test_coordinate_check():
    test_data = pd.DataFrame({
        "latitude": [48.16, 91.0, 48.16, -91.0],
        "longitude": [16.38, 16.38, 181.0, -181.0]
    })

    outliers = check_coordinates(test_data)

    assert (
    (outliers["latitude"] < -90) |
    (outliers["latitude"] > 90) |
    (outliers["longitude"] < -180) |
    (outliers["longitude"] > 180)
    ).all()

def test_missing_values():
    test_data = pd.DataFrame({
        "home_team": ["Rapid Wien", "Austria Wien", None],
        "away_team": ["Sturm Graz", None, "LASK"],
        "stadium": ["Allianz Stadion", "Generali Arena", None]
    })

    missing_values = check_missing_values(test_data)
    assert missing_values["home_team"] == 1
    assert missing_values["away_team"] == 1
    assert missing_values["stadium"] == 1

def test_duplicate_matches():
    test_data = pd.DataFrame({
        "date": ["2026-11-21", "2026-11-22", "2026-11-21"],
        "home_team": ["Rapid Wien", "Austria Wien", "Rapid Wien"],
        "away_team": ["Sturm Graz", "LASK", "Sturm Graz"],
        "kickoff": ["17:00", "14:30", "17:00"]
    })

    duplicate_count = get_duplicate_matches(test_data)
    assert duplicate_count == 2

def test_quality_checks():
    test_data = pd.DataFrame({
        "date": ["2026-11-21", "2026-11-22", "2026-11-21", None],
        "home_team": ["Rapid Wien", None, "Rapid Wien", "LASK"],
        "away_team": ["Sturm Graz", None, "Sturm Graz",None],
        "kickoff": ["17:00", None, "17:00","14:30"],
        "latitude": [48.16, 91.0, 48.16, -91.0],
        "longitude": [16.38, 16.38, 16.38, -181.0]
    })

    missing_values, duplicate_count, outliers = run_data_quality_checks(test_data)
    assert missing_values["home_team"] == 1
    assert missing_values["away_team"] == 2
    assert missing_values["kickoff"] == 1
    assert duplicate_count == 2
    assert len(outliers) == 2
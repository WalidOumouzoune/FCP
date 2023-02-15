from FCPpk.FCP import get_games, get_games_by_country, isvalid_URL, style, headers, parameters
import pytest


def test_get_games_TIMEZONE():

    parameters["timezone"] = "Invalid_TimeZone"
    URL = f"https://v3.football.api-sports.io/fixtures?live=all"
    with pytest.raises(ValueError):
        get_games(URL)

def test_get_games_with_Invalid_API_KEY():

    URL = f"https://v3.football.api-sports.io/fixtures?live=all"
    headers["x-rapidapi-key"] = "xXxXxXxXxX___Invalid_API_KEY___xXxXxXxXxX"
    with pytest.raises(ValueError):
        get_games(URL)

def test_get_games_URL():

    URL = f"_______________Invalid_URL__________________"
    with pytest.raises(ValueError):
        get_games(URL)


def test_get_games_by_country():
    with pytest.raises(ValueError):
        get_games_by_country("InvalidCountry")


def test_isvalid_URL():

    assert isvalid_URL("https://v3.football.api-sports.io/fixtures") == False
    assert isvalid_URL("http://v3.football.api-sports.io/fixtures") == False
    assert isvalid_URL("https://www.v3.football.api-sports.io/fixtures") == False
    assert isvalid_URL("www.google.com") == False
    assert isvalid_URL("https://v3.football.api-sports.io/fixtures?") == False
    assert isvalid_URL("https://v3.football.api-sports.io/fixtures?date=2002") == True


def test_style():

    b_1 = {
        'team_a': 'Manchester United',
        'goals_a': None,
        'team_b': 'Leeds',
        'goals_b': None,
        'time': None,
        'status': 'Not Started',
        'date': '21:00',
        'penalty_b': None,
        'penalty_a': None
    }
    r_1 = {
        "TIME": "Not Started",
        "TEAM_A": "Manchester United",
        "VS": "21:00",
        "TEAM_B": "Leeds",
    }


    b_2 = {
        'team_a': 'Man City',
        'goals_a': '0',
        'team_b': 'Liverpool',
        'goals_b': '2',
        'time': None,
        'status': 'Match Finished',
        'date': '21:00',
        'penalty_b': None,
        'penalty_a': None
    }
    r_2 = {
        "TIME": "Match Finished",
        "TEAM_A": "Man City",
        "VS": "0 - 2",
        "TEAM_B": "Liverpool",
    }


    b_3 = {
        'team_a': 'Raja',
        'goals_a': '0',
        'team_b': 'Far',
        'goals_b': '2',
        'time': '51',
        'status': 'First Half',
        'date': '21:00',
        'penalty_b': None,
        'penalty_a': None
    }
    r_3 = {
        "TIME": "51'",
        "TEAM_A": "Raja",
        "VS": "0 - 2",
        "TEAM_B": "Far",
    }


    b_4 = {
        'team_a': 'Man City',
        'goals_a': '0',
        'team_b': 'Liverpool',
        'goals_b': '0',
        'time': None,
        'status': 'Match Finished After Penalty',
        'date': '21:00',
        'penalty_a': 3,
        'penalty_b': 0,
    }
    r_4 = {
        "TIME": "Match Finished After Penalty",
        "TEAM_A": "Man City",
        "VS": "0 - 0 P(3-0)",
        "TEAM_B": "Liverpool",
    }


    b_5 = {
        'team_a': 'Manchester United',
        'goals_a': None,
        'team_b': 'Leeds',
        'goals_b': None,
        'time': None,
        'status': 'Cancelled',
        'date': '21:00',
        'penalty_b': None,
        'penalty_a': None
    }
    r_5 = {
        "TIME": "Cancelled",
        "TEAM_A": "Manchester United",
        "VS": "-  -",
        "TEAM_B": "Leeds",
    }


    assert r_1 == style(b_1)
    assert r_2 == style(b_2)
    assert r_3 == style(b_3)
    assert r_4 == style(b_4)
    assert r_5 == style(b_5)

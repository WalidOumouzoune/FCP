
"""

FC Python
~~~~~~~~~~

FCP is a python library to facilitate working with "www.api-football.com"
API docs : https://www.api-football.com/documentation-v3

    >>> import FCP
    >>> import tabulate
    >>> FCP.headers = {
        "x-rapidapi-key": "XxxXxXXxXxXxXxXxXXxXxXxX",
    }
    >>> games = FCP.get_live_game()
    >>> print(tabulate.tabulate(games))
    +-------------+-----------------+--------------+----------------+
    |   TIME      |     TEAM_A      |     VS       |      TEAM_B    |
    +-------------+-----------------+--------------+----------------+
    |     51'     |    Liverpool    |    2 - 1     |   Chelsea      |
    |     33'     |    Newcastle    |    1 - 0     |   West Ham     |
    |     14'     |     Arsenal     |    1 - 2     |   Man City     |
    +-------------+-----------------+--------------+----------------+

 ______ _____ ______      ______      _   _
|  ___/  __ \| ___ \  _  | ___ \    | | | |
| |_  | /  \/| |_/ / (_) | |_/ /   _| |_| |__   ___  _ __
|  _| | |    |  __/      |  __/ | | | __| '_ \ / _ \| '_ \\
| |   | \__/\| |      _  | |  | |_| | |_| | | | (_) | | | |
\_|    \____/\_|     (_) \_|   \__, |\__|_| |_|\___/|_| |_|
                                __/ |
                               |___/
______          _   _           _ _   _____  _     _   _______
|  ___|        | | | |         | | | /  __ \| |   | | | | ___ \\
| |_ ___   ___ | |_| |__   __ _| | | | /  \/| |   | | | | |_/ /
|  _/ _ \ / _ \| __| '_ \ / _` | | | | |    | |   | | | | ___ \\
| || (_) | (_) | |_| |_) | (_| | | | | \__/\| |___| |_| | |_/ //
\_| \___/ \___/ \__|_.__/ \__,_|_|_|  \____/\_____/\___/\____//


"""

import os
import sys
import requests
from datetime import date
from FCPpk.consts import TOP_COMPETITIONS, COMPETITIONS, TIMEZONES, TODAYS_TOP


# "d6945347736976d8f423047935da8706"

api_key = os.environ.get("API_KEY")
if not api_key:
    sys.exit("Export API_KEY first 🙏")

time_zone = os.environ.get("TIMEZONE")
if not time_zone:
    sys.exit("Export TIMEZONE first 🙏")


headers = {
    "x-rapidapi-key": api_key
}

parameters = {
    "timezone": time_zone
}


def get_games(URL: str) -> None | list:

    """
    API docs : https://www.api-football.com/documentation-v3#tag/Fixtures
    :params URL:  where host is 'https://v3.football.api-sports.io/fixtures'
    :type URL: str
    :raise ValueErorr: if timezone does not exist, API_KEY,  and Invalid URL
    :return: None if the api was unsuccessful to provied data
    :return: Games in a the given URL
    :rtype: dict|None:
    """

    if not isvalid_URL(URL):
        raise ValueError("Invalid URL")

    timezone = parameters["timezone"]
    if timezone not in TIMEZONES:
        raise ValueError(f'{parameters["timezone"]} does not exist')

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        GAMES = response.json()
    except requests.RequestException:
        return None
    else:
        if "token" in GAMES["errors"]:
            raise ValueError(f'API_KEY is not correct')
        if len(GAMES["errors"]) != 0:
            return None

    today_games = []
    try:
        for game in GAMES["response"]:
            today_games.append(
                style(
                    {
                        "team_a": game["teams"]["home"]["name"],
                        "goals_a": game["goals"]["home"],
                        "team_b": game["teams"]["away"]["name"],
                        "goals_b": game["goals"]["away"],
                        "time": game["fixture"]["status"]["elapsed"],
                        "status": game["fixture"]["status"]["long"],
                        "date": game["fixture"]["date"].split("T")[1][0:5],
                        # penalties after extratime
                        "penalty_b": game["score"]["penalty"]["away"],
                        "penalty_a": game["score"]["penalty"]["home"],
                    }
                )
            )
    except (KeyError, TypeError, ValueError):
        return None

    return today_games


def get_competitions_ids(competitions: dict) -> str:

    """ helper function return competitions' ids as string """

    s = ""
    for country in competitions:
        for competition in competitions[country]:
            s = f"{s}-{str(competition)}"
    return s[1:]


def get_games_by_country(country: str) -> None | list:

    """
    API docs : https://www.api-football.com/documentation-v3#tag/Fixtures
    :params country: abbreviation of the country name
    :type country: str
    :raise ValueErorr: if country doesn't exist
    :return: None if the api was unsuccessful to provied data
    :return: Games in the given country
    :rtype: dict|None:
    """

    timezone = parameters["timezone"]
    today = date.today()

    if not country.lower() in COMPETITIONS:
        raise ValueError(f"{country} doesn't exist")

    # the season is always a year late than the current one
    season = today.year - 1
    competitions = COMPETITIONS[country.lower()]

    games = []
    for competition in competitions:
        URL = f"https://v3.football.api-sports.io/fixtures?league={competition}&season={season}&date={today}&timezone={timezone}"
        matches = get_games(URL)
        if matches is None:
            return None
        games.extend(matches)
    return games


def get_live_games() -> list | None:

    """
    API docs : https://www.api-football.com/documentation-v3#tag/Fixtures
    :return: None if the api was unsuccessful to provied data
    :return: live games
    :rtype: dict|None:

    """

    ids = get_competitions_ids(TOP_COMPETITIONS)
    URL = f"https://v3.football.api-sports.io/fixtures?live={ids}&timezone={parameters['timezone']}"
    games = get_games(URL)
    if games is None:
        return None
    matches = []
    for game in games:
        matches.append(game)
    return matches


def get_top_todays_games() -> list | None:

    """
    API docs : https://www.api-football.com/documentation-v3#tag/Fixtures
    :raise requests.RequestException: if request was unsuccessful
    :return: dict of Today's matches OR None if the api was unsuccessful to provied data
    :rtype: dict|None:

    NOTE: it's not recommended using this function if you have free plan
    """

    timezone = parameters["timezone"]
    # the season is always a year late than the current one
    today = date.today()
    season = today.year - 1
    games = []

    for country in TODAYS_TOP:
        for competition in TODAYS_TOP[country]:
            URL = f"https://v3.football.api-sports.io/fixtures?league={competition}&season={season}&date={today}&timezone={timezone}"
            matches = get_games(URL)
            if matches is None:
                return None
            games.extend(matches)
    return games


def isvalid_URL(url) -> bool:

    HOST = "https://v3.football.api-sports.io/fixtures"
    try:
        host, params = url.split("?")
        if not params:
            return False
        return host == HOST
    except:
        return False


def style(game: dict) -> dict:

    """ b """

    game_info = {
        "TIME": game["status"],
        "TEAM_A": game["team_a"],
        "VS": "-  -",
        "TEAM_B": game["team_b"],
    }

    if "Not Started" == game["status"]:
        game_info["VS"] = game["date"]
    elif "Finished" in game["status"]:
        game_info["VS"] = f"{game['goals_a']} - {game['goals_b']}"
    elif game["time"] is not None:
        game_info["TIME"] = f"{game['time']}'"
        game_info["VS"] = f"{game['goals_a']} - {game['goals_b']}"
    if game["penalty_a"] is not None:
        game_info["VS"] = f'{game_info["VS"]} P({game["penalty_a"]}-{game["penalty_b"]})'


    return game_info
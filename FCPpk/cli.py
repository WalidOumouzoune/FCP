import argparse
import sys
from pyfiglet import Figlet
from tabulate import tabulate
from FCPpk.consts import COMPETITIONS
from FCPpk.FCP import get_games_by_country, get_live_games, get_top_todays_games


def main():

    parser = argparse.ArgumentParser(
        description="Track football games from the terminal",
        prog="FCP"
    )
    parser.add_argument("-t", default="default", help="reprsent time take two options ['now', 'today']", nargs='?', type=str)
    parser.add_argument("-c", default="default", help="Today's games in a specific country", nargs='?', type=str)
    args = parser.parse_args()

    figlet = Figlet()
    figlet.setFont = "big"

    games = filter_flags(args)
    if games == False:
         sys.exit(parser.print_help())
    elif games is None:
        sys.exit(figlet.renderText("Opps Try after 1 minute"))
    elif len(games) == 0:
        sys.exit(figlet.renderText("Nothing Now"))


    print(
        tabulate(
            games,
            headers="keys",
            tablefmt="mixed_outline",
            colalign=("center", "center", "center", "center"),
        )
    )


def filter_flags(args) -> bool | dict:

    if len(sys.argv) > 4 or len(sys.argv) < 2:
        return False

    time = args.t
    if time != "default":
        if args.t == "now":
            games = get_live_games()
        elif time == "today":
            games = get_top_todays_games()
        else:
            return False
    else:
        country = args.c
        if country not in COMPETITIONS:
            sys.exit("country doesn't exit visit country_list: https://github.com/code50/73303972/tree/main/CS50p/project#country-code")
        games = get_games_by_country(country)

    return games


if __name__ == "__main__":
    main()


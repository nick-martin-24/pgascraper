from scrapeutils.ncaa import urls
import requests

def get_tournament(year=2019):
    return requests.get(urls.base(year)).json()

def get_games_by_team(team):
    team_games = []
    t = get_tournament()
    for game in t['games']:
        if team in [game['game']['home']['names']['short'], game['game']['away']['names']['short']]:
            team_games.append(game)

    return team_games

def get_team_names():
    team_names = []
    t = get_tournament()
    for game in t['games']:
        team1 = game['game']['away']['names']['short']
        team2 = game['game']['home']['names']['short']
        if team1 not in team_names:
            team_names.append(team1)
        if team2 not in team_names:
            team_names.append(team2)

    return team_names


from scrapeutils.ncaa import urls
import requests


def get_tournament(year=2019):
    ''' Get dictionary of json structure for a march madness tournament.
    '''
    return requests.get(urls.base(year)).json()

def get_games_by_team(team):
    ''' Get list of games for a given team

        :param team: team for which to retrieve games
        : type team: str

        :returns: list of game dictionaries
    '''
    team_games = []
    t = get_tournament()
    for game in t['games']:
        if in_game(team,game):
            team_games.append(game)
    return team_games

def get_team_names(name_type='short'):
    ''' Get list of team names in march madness tournament.

        :param name_type: type of name to return (char6: 'CINCY', full: 'University of Cincinnati', seo: 'cincinnati', short: 'Cincinnati')
        : type name_type: str

        :returns: list of team names
    '''
    team_names = []
    t = get_tournament()
    for game in t['games']:
        team1 = game['game']['away']['names'][name_type]
        team2 = game['game']['home']['names'][name_type]
        if team1 not in team_names:
            team_names.append(team1)
        if team2 not in team_names:
            team_names.append(team2)
    return team_names

def get_seed_by_team(team):
    ''' Get seed for team

        :param team: team for which to retrieve seed
        : type team: str

        :returns: int; seed
    '''
    t = get_tournament()
    for game in t['games']:
        if in_game(team,game):
            team_type = get_team_type(team,game)
            return int(game['game'][team_type]['seed'])

def in_game(team,game):
    ''' Determine if a team is playing in current game.

        :param team: team to check if playing in game
        : type team: str
        :param game: game to check
        : type game: dict

        :returns: bool
    '''
    if team in [game['game']['home']['names']['short'], game['game']['away']['names']['short']]:
        return True
    return False

def get_team_type(team,game):
    ''' Determine if team is home or away in a given game.

        :param team: team to check if playing in game
        : type team: str
        :param game: game to check
        : type game: dict

        :returns: str; home or away
    '''
    if team in game['game']['home']['names']['short']:
        return 'home'
    return 'away'


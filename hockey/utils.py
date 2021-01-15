from scrapeutils.hockey import urls
from datetime import datetime as dt
import requests
import collections


def get_schedule():
    ''' Get schedule information for current date.

    :returns: dict
    '''
    return requests.get(urls.schedule()).json()

def get_todays_games():
    ''' Get information for all games on current date.
    
    :returns: list of dicts
    '''
    return requests.get(urls.schedule()).json()['dates'][0]['games']

def flyers_game_today():
    ''' Determine if there is a flyers game today.

    :returns: bool
    '''
    flyers_play = False
    for game in get_todays_games():
        teams = game['teams']
        if 'Philadelphia Flyers' in [teams['away']['team']['name'],teams['home']['team']['name']]:
            flyers_play = True
            break
    return flyers_play

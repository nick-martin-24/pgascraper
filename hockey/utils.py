from scrapeutils.hockey import urls
from datetime import datetime as dt
import requests
import collections
import math


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

def print_today_summary():
    ''' Print summary of games on current date (Away@Home: game_id) '''
    for game in get_todays_games():
        away = game['teams']['away']['team']['name']
        home = game['teams']['home']['team']['name']
        game_id = game['gamePk']
        print('{} @ {}: {}'.format(away, home, game_id))

def get_game_by_id(game_id):
    ''' Get information for game given by game_id

    :returns: dict
    '''
    return requests.get(urls.game(game_id)).json()

def summarize_game(game_id):
    ''' Print out event types and number of each events. '''
    events = {}
    game = get_game_by_id(game_id)
    plays = game['liveData']['plays']['allPlays']
    for play in plays:
        event = play['result']['event']
        if event not in events.keys():
            events[event] = 1
        else:
            events[event] += 1
        if event == 'Goal':
            print('!!! GOAL !!! {} scored from {}'.format(play['players'][0]['player']['fullName'], play['players'][1]['player']['fullName']))

    for event in events:
        print('{}: {}'.format(event, events[event]))

def get_person_by_id(person_id):
    ''' Get information for person given by person_id

    :returns: dict
    '''
    return requests.get(urls.people(person_id)).json()

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

def get_shot_distance(x,y):
    goal_location = (89,0)
    shot_location = (abs(x),y)
    return math.dist(shot_location,goal_location)

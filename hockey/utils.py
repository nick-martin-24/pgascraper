from scrapeutils.hockey import urls
from datetime import datetime as dt
import requests
import collections
import math
import matplotlib.pyplot as plt
from PIL import Image


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

def summarize_game(game_id,stats='Goal'):
    ''' Print out event types and number of each events. '''
    events = {}
    colors = {'Philadelphia Flyers': 'orange', 'Pittsburgh Penguins': 'yellow'}
    shot_colors = {'Goal': 'green','Shot': 'blue', 'Missed Shot': 'red', 'Blocked Shot': 'yellow'}
    period_scale = {1: 1, 2: -1, 3: 1}
    game = get_game_by_id(game_id)
    plays = game['liveData']['plays']['allPlays']
    fig, ax, xscale, yscale = make_rink()
    for play in plays:
        event = play['result']['event']
        if event not in events.keys():
            events[event] = 1
        else:
            events[event] += 1
        if event in stats:
            x = play['coordinates']['x'] * xscale * (period_scale[play['about']['period']])
            y = play['coordinates']['y'] * yscale + (period_scale[play['about']['period']])
            ax.scatter(x,y,label=event,color=shot_colors[event],s=300,linewidth=3,edgecolors='black')
            #if event == 'Goal':
                #ax.annotate(play['players'][0]['player']['fullName'],(x,y))

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.text(0.13, 1.01, game['gameData']['teams']['home']['name'], fontsize=14, weight='bold', transform=plt.gca().transAxes)
    plt.text(0.69, 1.01, game['gameData']['teams']['away']['name'], fontsize=14, weight='bold', transform=plt.gca().transAxes)
    for event in events:
        print('{}: {}'.format(event, events[event]))
    plt.show()

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

def make_rink():
    fig = plt.figure(figsize=(12,7))
    ax = fig.add_subplot(111)
    ax.set_position([0,0,1,1])


    I = Image.open('/Users/nickmartin/projects/python/scrapeutils/hockey/NHL_Hockey_Rink.png')
    left = 46
    top = 117
    right = I.width - 37
    bottom = I.height - 132
    I = I.crop((left, top, right, bottom))
    #I = I.resize((int(I.width*2),int(I.height*2)), Image.ANTIALIAS)
    width, height = I.size
    xscale = width/200
    yscale = height/85
    ax.imshow(I, extent=[-width/2, width/2, -height/2, height/2])
    return fig, ax, xscale, yscale

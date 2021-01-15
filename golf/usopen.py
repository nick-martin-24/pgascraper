import json
import utils
import requests


def scrape(leaderboard, tee_times):
    setup = leaderboard['debug']
    leaderboard = leaderboard['leaderboard']
    t = {}

    # tournament data
    t['name'] = None 
    t['par'] = None
    t['is_started'] = None
    t['is_finished'] = None
    t['current_round'] = json['current_round']['number'] # int
    t['round_state'] = None
    t['cut_line'] = json['cutLine']['score'] # str
    t['players'] = {}

    # player data
    players = json['standings']
    for player in players:
        name = '{} {}'.format(player['player']['firstName'], player['player']['lastName'])
        position = player['position']['displayValue']
        t['players'][name] = {}
        if position is not 'MC':
            t['players'][name]['status'] = 'active'
        else:
            t['players'][name]['status'] = 'cut'
        t['players'][name]['current_round'] = None
        t['players'][name]['thru'] = player['holesThrough']['value'] # int (displayValue is str, and displays 'F')
        t['players'][name]['today'] = player['toParToday']['value'] # int (displayValue is str)
        t['players'][name]['total'] = player['toPar']['value'] # int (displayValue is str)
        t['players'][name]['total_strokes'] = player['totalScore']['value'] # int (displayValue is str)
        t['players'][name]['rounds'] = []

        for round in player['rounds']:
            i = 0
            t['players'][name]['rounds'].append({})
            t['players'][name]['rounds'][round[i]['strokes'] = round['score']['value'] # int (displayValue is str)
            t['players'][name]['rounds'][i]['tee_time'] = None
            t['players'][name]['rounds'][i]['to_par'] = round['toPar']['value'] # int (displayValue is str, and probably displays 'E' (confirm this))

    return t

import json
from pgascraper.src.scrapeutils import utils
import requests


def scrape(json):
    setup = json['debug']
    leaderboard = json['leaderboard']
    t = {}

    # tournament data
    t['name'] = leaderboard['tournament_name']
    t['par'] = leaderboard['courses'][0]['par_total'] 
    t['is_started'] = leaderboard['is_started']
    t['is_finished'] = leaderboard['is_finished']
    t['current_round'] = leaderboard['current_round']
    t['round_state'] = leaderboard['round_state']
    t['cut_line'] = leaderboard['cut_line']['cut_line_score']
    t['players'] = {}

    # player data
    players = leaderboard['players']
    for player in players:
        name = '{} {}'.format(player['player_bio']['first_name'], player['player_bio']['last_name'])
        t['players'][name] = {}
        t['players'][name]['status'] = player['status']
        t['players'][name]['current_round'] = player['current_round']
        t['players'][name]['thru'] = player['thru']
        t['players'][name]['today'] = player['today']
        t['players'][name]['total'] = player['total']
        t['players'][name]['total_strokes'] = player['total_strokes']
        t['players'][name]['rounds'] = []

        for round in player['rounds']:
            t['players'][name]['rounds'].append({})
            t['players'][name]['rounds'][round['round_number'] - 1]['strokes'] = round['strokes']
            t['players'][name]['rounds'][round['round_number'] - 1]['tee_time'] = round['tee_time']
#            t['players'][name]['rounds'][round['round_number'] - 1]['to_par'] = int(round['strokes']) - int(t['par'])

    return t

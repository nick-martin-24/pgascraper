import json
import urllib
import requests
import datetime
from bs4 import BeautifulSoup
from scrapeutils import utils


def scrape_leaderboard(json):
    setup = json['debug']
    leaderboard = json['leaderboard']
    t = {}

    # tournament data
    t['name'] = setup['tournament_in_schedule_file_name']
    t['id'] = leaderboard['tournament_id']
    t['setup_year'] = setup['setup_year']
    t['actual_year'] = datetime.datetime.now().year
    t['par'] = int(leaderboard['courses'][0]['par_total'])
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
        t['players'][name]['penalty'] = 0
        if player['status'] == 'cut':
            t['players'][name]['penalty'] = player['total'] - t['cut_line']
        t['players'][name]['current_round'] = player['current_round']
        t['players'][name]['thru'] = player['thru']
        t['players'][name]['today'] = player['today']
        t['players'][name]['real_total'] = player['total']
        t['players'][name]['total'] = (player['total'] or 0) + t['players'][name]['penalty']
        t['players'][name]['total_strokes'] = player['total_strokes']
        t['players'][name]['day1'] = 0
        t['players'][name]['day2'] = 0
        t['players'][name]['day3'] = 0
        t['players'][name]['day4'] = 0
        t['players'][name]['rounds'] = []

        for round in player['rounds']:
            t['players'][name]['rounds'].append({})
            t['players'][name]['rounds'][round['round_number'] - 1]['strokes'] = round['strokes']
            if round['tee_time'] is not None:
                t['players'][name]['rounds'][round['round_number'] - 1]['tee_time'] = datetime.datetime.strptime(round['tee_time'], '%Y-%m-%dT%H:%M:%S').time().strftime('%H:%M')
            else:
                t['players'][name]['rounds'][round['round_number'] - 1]['tee_time'] = '---'

        if t['current_round'] == 1:
            t['players'][name]['day1'] = t['players'][name]['today'] or 0
        elif t['current_round'] == 2:
            t['players'][name]['day1'] += t['players'][name]['rounds'][0]['strokes'] - t['par']
            if t['round_state'] != 'Official':
                t['players'][name]['day2'] += t['players'][name]['today'] or 0
            else:
                t['players'][name]['day2'] += t['players'][name]['rounds'][1]['strokes'] - t['par']
        elif t['current_round'] == 3:
            print(name)
            t['players'][name]['day1'] += t['players'][name]['rounds'][0]['strokes'] - t['par']
            t['players'][name]['day2'] += (t['players'][name]['rounds'][1]['strokes']or t['par']) - t['par']
            t['players'][name]['day3'] += t['players'][name]['today'] or 0
        else:
            t['players'][name]['day1'] += t['players'][name]['rounds'][0]['strokes'] - t['par']
            t['players'][name]['day2'] += (t['players'][name]['rounds'][1]['strokes'] or t['par']) - t['par']
            t['players'][name]['day3'] += (t['players'][name]['rounds'][2]['strokes'] or t['par']) - t['par']
            t['players'][name]['day4'] += t['players'][name]['today'] or 0


    return t


def scrape_field(id):
    field_url = 'https://statdata.pgatour.com/r/{}/field.json'.format(id)
    print(field_url)
    # set player names from field of current tournament
    f = requests.get(field_url)
    parsed_json = f.json()
    players = parsed_json['Tournament']['Players']
    player_names = []
    for item in players:
        name = item['PlayerName'].split(', ')
        player_names.append(' '.join((name[1], name[0])))

    # get players from owgr and set the top 60 who are in the field of current tournament
    # url = 'http://www.owgr.com/ranking?pageNo=1&pageSize=300$country=All'
    url = 'http://www.owgr.com/ranking?pageNo=1&pageSize=All&country=All'
    # url = 'http://www.owgr.com/ranking'
    h = urllib.request.urlopen(url)
    html = h.read()
    soup = BeautifulSoup(html, 'html.parser')

    tr = soup.find_all('tr')
    tr = tr[1:]
    owgr = []
    count = 0
    for item in tr:
        name = item.contents[9].contents[0].contents[0]
        if name[0:6] == 'Rafael':
            name = 'Rafa Cabrera Bello'
        if name == 'Peter Uihlein':
            continue
        if name in player_names and count < 60 and name != 'Scottie Scheffler':
            owgr.append(name)
            count += 1

    # define tiers
    field = {}
    field['a'] = owgr[0:10]
    field['b'] = owgr[10:25]
    field['c'] = owgr[25:40]
    field['d'] = owgr[40:]

    return field


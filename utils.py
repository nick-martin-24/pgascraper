import urls
import requests
import datetime
import collections
from scrapeutils import pgatour
from datetime import datetime as dt


def scrape():
    MAJOR_TOURNAMENT_NAMES = ['Masters Tournament',
                              'U.S. Open',
                              'The Open Championship',
                              'PGA Championship',
                              'THE PLAYERS Championship']

    tournament = get_current_tournament()
    tournament_urls = get_urls(tournament)
    tournament_data = parse_json(tournament_urls)

    t_name = tournament['trnName']['official']
    if 1>0:
        if len(tournament_data) != 0:
            t = pgatour.scrape_leaderboard(tournament_data[0])
        else:
            t = {}
            t['name'] = tournament['trnName']['official']
            t['id'] = tournament['permNum']
            t['setup_year'] = tournament['year']
            t['actual_year'] = datetime.datetime.now().year
            t['par'] = 72
            t['is_started'] = False
            t['is_finished'] = False
            t['current_round'] = 0
            t['round_state'] = 'Not Started'
            t['cut_line'] = None
            t['players'] = {}

            players_dict = pgatour.scrape_field(t['id'])
            players = players_dict['a'] + players_dict['b'] + players_dict['c'] + players_dict['d']
            for player in players:
                name = player
                t['players'][name] = {}
                t['players'][name]['status'] = 'active'
                t['players'][name]['penalty'] = 0
                t['players'][name]['current_round'] = 1
                t['players'][name]['thru'] = None
                t['players'][name]['today'] = None
                t['players'][name]['real_total'] = None
                t['players'][name]['total'] = 0
                t['players'][name]['total_strokes'] = None
                t['players'][name]['day1'] = 0
                t['players'][name]['day2'] = 0
                t['players'][name]['day3'] = 0
                t['players'][name]['day4'] = 0
                t['players'][name]['rounds'] = []

                for round in range(0,4):
                    t['players'][name]['rounds'].append({})
                    t['players'][name]['rounds'][round]['strokes'] = None
                    t['players'][name]['rounds'][round]['tee_time'] = '---'



    return t


def get_current_tournament():
    schedule_json = requests.get(urls.schedule_url()).json()

    current_week = schedule_json['thisWeek']['weekNumber']
    current_year = schedule_json['currentYears']['r']
    current_year_data = next(year for year in schedule_json['years']
                             if year['year'] == current_year)
    current_year_pga_tour = next(tour for tour in current_year_data['tours']
                                 if tour['tourCodeLc'] == 'r')

    current_week_verified = False
    while not current_week_verified:
        current_week_tournament = next(tournament for tournament in current_year_pga_tour['trns']
                                       if tournament['date']['weekNumber'] == current_week
                                       and tournament['primaryEvent'] == 'Y')
        if (dt.strptime(current_week_tournament['date']['end'], '%Y-%m-%d').date() >= dt.now().date()):
            current_week_verified = True
        else:
            current_week = str(int(current_week) + 1)

    return current_week_tournament

def parse_json(urls):
    data = []
    for url in urls:
        f = requests.get(url)
        if f.ok is True:
            data.append(f.json())

    return data


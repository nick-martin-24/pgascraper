import urls
import requests
import datetime
import collections
from scrapeutils import pgatour
from datetime import datetime as dt


def scrape():
    ''' Parse leaderboard url json and populate a dictionary
        with data required for golfpool processing. Currently
        only uses pgatour.com website

        TO DO: create scrapers for each major tournament website

    :returns: dictionary with parsed and organized tournament data
    :output t: dictionary with parsed and organized tournament data
        :field name: name of tournament as it will be found in leaderboard json
        :type name: str
        :field id: tournament id to be substituted into urls
        :type id: str
        :field setup_year: year in leaderboard json
        :type setup_year: str
        :field actual_year: real year at time of processing
        :type actual_year: str
        :field is_started:
        :type is_started: bool
        :field is_finished:
        :type is_finished: bool
        :field current_round: current round of tournament
        :type current_round: int
        :field round_state: 
        :type round_state: str
    
        :field players: dictionary of pga golfers in tournament indexed by name
        :type players: dict
            :field status: active/cut
            :type status: str
            :field penalty: strokes over cut line, if missed cut
            :type penalty: int
            :field current_round: current round for pga golfer
            :type current_round: int
            :field thru: holes completed in current round
            :type thru: int
            :field today: total w.r.t. par on current day
            :type today: int
            :field real_total: total w.r.t. par from json
            :type real_total: int
            :field total: total w.r.t. par + penalty, if applicable
            :type total: int
            :field total_strokes: cumulative number of strokes (TBC if it includes current day or up to latest completed round)
            :type total_strokes: int
            :field day<#>: total w.r.t. par on given day #
            :type day<#>: int
            
            :field rounds: list of round data for each pga golfer in players dict
            :type rounds: list
                :field strokes: number of strokes in given round (None until round finished?)
                :type strokes: int
                :field tee_time: tee time for given round (set to '---' until defined)
                :type tee_time: str
    '''

    MAJOR_TOURNAMENT_NAMES = ['Masters Tournament',
                              'U.S. Open',
                              'The Open Championship',
                              'PGA Championship',
                              'THE PLAYERS Championship']

    tournament = get_current_tournament()
    tournament_data = parse_json(urls.leaderboard(tournament))
    if 1>0:
        # if tournament json is initialized, parse it
        if len(tournament_data) != 0:
            t = pgatour.scrape_leaderboard(tournament_data[0])
        # if tournament json not initialized, set t to default
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

            players = generate_field(pgatour.scrape_field(t['id']))
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
    ''' Parse the pgatour.com schedule json for the tournament
        corresponding to the current week.

    :returns: Dictionary containing information for current week
              tournament.
    '''
    schedule_json = requests.get(urls.schedule()).json()

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
    ''' retrieve the json data that is present at the url
        returned by urls.leaderboard

    :param urls: url pointing to leaderboard json
    :type urls: str

    :returns: data variable containing json data for given tournament
    '''
    data = []
    for url in urls:
        f = requests.get(url)
        if f.ok is True:
            data.append(f.json())

    return data


def generate_field(player_names)
    ''' compare player names returned from field parsing for given tournament
        with the owgr. Take the top 60 and split into groups.

    :param player_names: player names returned from given tournament's scrape_field
    :type player_names: list

    :returns: dictionary with 4 keys corresponding to lists of golfers in given group
    '''
    h = urllib.request.urlopen(urls.owgr_url())
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

    return field['a'] + field['b'] + field['c'] + field['d']


import requests
import collections
from pgascraper.src.scrapeutils import pgatour
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


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
    if t_name == 'Masters Tournament':
        t = masters.scrape(leaderboard)

    elif t_name == 'U.S. Open':
        tee_times_url = 'https://gripapi-static-pd.usopen.com/gripapi/teetimes.json'
        tee_times = parse_json(tee_times_url)
        t = usopen.scrape(leaderboard, tee_times)

    elif t_name == 'The Open Championship':
        t = open.scrape(leaderboard)

    elif t_name == 'PGA Championship':
        t = pga.scrape(leaderboard)

    elif t_name == 'THE PLAYERS Championship':
        t = players.scrape(leaderboard)

    else:
        t = pgatour.scrape(tournament_data[0])

    return t


def get_current_tournament():
    schedule_url = 'https://statdata.pgatour.com/r/current/schedule-v2.json'
    schedule_json = requests.get(schedule_url).json()

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
        if (dt.strptime(current_week_tournament['date']['end'], '%Y-%m-%d') > dt.now()):
            current_week_verified = True
        else:
            current_week = str(int(current_week) + 1)

    return current_week_tournament


def get_urls(tournament):
    urls = []
    leaderboard_url = 'https://www.pgatour.com/leaderboard.html'
    tournament_name = tournament['trnName']['official']
    tournament_id = tournament['permNum']
    tournament_year = tournament['year']
    # tournament_name = 'U.S. Open'
    print('Processing json for {}\n'.format(tournament_name))
    if tournament_name == 'Masters Tournament':
        return
    elif tournament_name == 'U.S. Open':
        urls.append('https://gripapi-static-pd.usopen.com/gripapi/leaderboard.json')
        urls.append('https://gripapi-static-pd.usopen.com/gripapi/teetimes.json')
    elif tournament_name == 'The Open Championship':
        return
    elif tournament_name == 'PGA Championship':
        return
    elif tournament_name == 'THE PLAYERS Championship':
        return
    else:
        # init Chrome driver (Selenium)
        options = Options()
        options.headless = True
        cap = DesiredCapabilities.CHROME
        cap['goog:loggingPrefs'] = {'performance': 'ALL'}
        driver = webdriver.Chrome('/Users/nickmartin/projects/python/pgascraper/src/scrapeutils/chromedriver', desired_capabilities=cap, options=options)

        # record and parse performance log
        driver.get(leaderboard_url)
        performance_log = driver.get_log('performance')
        driver.quit()

        log = []
        base = 'https://statdata.pgatour.com/r'
        message = 'message.json'
        for item in performance_log:
            if base in item['message'] and message in item['message']:
                log.append(item['message'])


        id_str = 'userTrackingId=exp='
        id_idx = log[0].find(id_str)
        acl_str = '~acl=*~hmac='
        acl_idx = log[0].find(acl_str)
        end_acl_str = '"},"requestId'
        end_acl_idx = log[0].find(end_acl_str)
        user_id = log[0][id_idx + len(id_str) : acl_idx]
        acl = log[0][acl_idx + len(acl_str) : end_acl_idx]
        urls.append('{}/{}/{}/leaderboard-v2.json?{}{}{}{}'.format(base, tournament_id, tournament_year, id_str, user_id, acl_str, acl))

    return urls


def parse_json(urls):
    data = []
    for url in urls:
        f = requests.get(url)
        data.append(f.json())

    return data






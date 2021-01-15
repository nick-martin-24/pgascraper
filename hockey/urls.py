from datetime import datetime as d
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

def base():
    return 'http://statsapi.web.nhl.com/api/v1'

def schedule():
    date_i = d.now().strftime('%Y-%m-%d')
    date_f = date_i
    return '{}/schedule?startDate={}&endDate={}'.format(base(),date_i, date_f)

def game(game_id):
    return '{}/game/{}/feed/live'.format(base(),game_id)

def people(person_id):
    return '{}/people/{}'.format(base(),person_id)

def leaderboard(tournament):
    ''' create url for current tournament data. need to determine unique user and acl id
        for session created when accessing pga site.
    
    :param tournament: tournament dictionary retrieved from schedule()
    :type tournament: dict

    :returns: url string
    '''

    urls = []
    tournament_name = tournament['trnName']['official']
    tournament_id = tournament['permNum']
    tournament_year = tournament['year']

    # init Chrome driver (Selenium)
    options = Options()
    options.headless = True
    cap = DesiredCapabilities.CHROME
    cap['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome('/Users/nickmartin/projects/python/scrapeutils/chromedriver', desired_capabilities=cap, options=options)

    # record and parse performance log
    driver.get(basic_leaderboard())
    performance_log = driver.get_log('performance')
    driver.quit()

    log = []
    message = 'message.json'
    for item in performance_log:
        if base() in item['message'] and message in item['message']:
            log.append(item['message'])


    id_str = 'userTrackingId=exp='
    id_idx = log[0].find(id_str)
    acl_str = '~acl=*~hmac='
    acl_idx = log[0].find(acl_str)
    end_acl_str = '"},"requestId'
    end_acl_idx = log[0].find(end_acl_str)
    user_id = log[0][id_idx + len(id_str) : acl_idx]
    acl = log[0][acl_idx + len(acl_str) : end_acl_idx]
    urls.append('{}/{}/{}/leaderboard-v2.json?{}{}{}{}'.format(base(), tournament_id, tournament_year, id_str, user_id, acl_str, acl))

    return urls


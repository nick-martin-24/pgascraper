import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


def field(tournament_id):
    return 'https://statdata.pgatour.com/r/{}/field.json'.format(tournament_id)

def owgr():
    return 'http://www.owgr.com/ranking?pageNo=1&pageSize=All&country=All'

def schedule():
    return 'https://statdata.pgatour.com/r/current/schedule-v2.json'

def basic_leaderboard():
    return 'https://www.pgatour.com/leaderboard.html'

def base():
    return 'https://statdata.pgatour.com/r'

def masters_config_web():
    return 'https://www.masters.com/en_US/json/gen/config_web.json'

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
    driver = webdriver.Chrome('{}/projects/python/scrapeutils/chromedriver'.format(os.environ['HOME']), desired_capabilities=cap, options=options)

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


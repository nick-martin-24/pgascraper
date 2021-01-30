from datetime import datetime as d

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


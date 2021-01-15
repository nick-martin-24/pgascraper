import json
import utils
import requests


def scrape_leaderboard(json):
    '''
    urls:
        { "title": "Tee Times", "section":"tee","link": "/en_US/players/pairings/index.html"},
        { "title": "The Course", "section":"course","link": "/en_US/course/index.html"},
        { "title": "Schedule", "section":"schedule","link": "/en_US/tournament/schedule.html"},
        { "title": "Tournament Info", "section":"tourn", "link": "/en_US/tournament/index.html"},
        { "title": "Patron Info", "section":"patron", "link": "/en_US/patron/index.html" },
        { "title": "Tickets", "section":"tickets", "link": "/en_US/patron/index.html?tab=ticketing"},
        { "title": "Shop", "section":"shop", "link": "/en_US/info/shop/index.html"},
        { "title": "Women's Amateur", "section":"amateur", "link": "https://www.anwagolf.com" },
        { "title": "Newsletter", "section":"newsletter", "link": "/en_US/newsletter/index.html" },
        { "title": "Search", "section":"search", "link": "/en_US/search/index.html" }
        "link": "/en_US/scores/track/index.html"
        "link": "/en_US/players/invitees_2020.html"
        "link": "/en_US/live/index.html",
	"scheduleDays": "/en_US/scores/feeds/schedule/scheduleDays.json",
	"schedule": "/en_US/scores/feeds/schedule/schedule<day>.json",
	"stats": "/en_US/scores/feeds/stats/<id>.json",
	"track": {
		"version": "v1",
		"path": "/en_US/scores/feeds/track/<playerId>.json",
		"rateSec": 20
	"playerList": "/en_US/scores/feeds/players/players.json",
	"playerProfile": "/en_US/scores/feeds/players/<id>.json",
	"playerStats": {
			"path": "/en_US/scores/feeds/players/scores/<playerId>.json",
			"rateSec": 40
	},
	"pairings": "/en_US/scores/feeds/pairings.json",
	"teePin": "/en_US/scores/feeds/track/teepin.json"
        
                
    tournament:
        https://www.masters.com/en_US/json/gen/config_web.json
            tournamentYear: 2020

        name = masters
        year
        par = 72



    '''
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
        t['players'][name]['thru'] = ['thru']
        t['players'][name]['today'] = ['today']
        t['players'][name]['total'] = ['total']
        t['players'][name]['total_strokes'] = ['total_strokes']
        t['players'][name]['rounds'] = []

        for round in player['rounds']:
            t['players'][name]['rounds'].append({})
            t['players'][name]['rounds'][round['round_number'] - 1]['strokes'] = round['strokes']
            t['players'][name]['rounds'][round['round_number'] - 1]['tee_time'] = round['tee_time']
#            t['players'][name]['rounds'][round['round_number'] - 1]['to_par'] = int(round['strokes']) - int(t['par'])

    return t

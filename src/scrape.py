from scrapeutils import utils, pgatour


MAJOR_TOURNAMENT_NAMES = ['Masters Tournament',
                          'U.S. Open',
                          'The Open Championship',
                          'PGA Championship',
                          'THE PLAYERS Championship']


tournament = utils.get_current_tournament()
leaderboard_url = utils.get_urls(tournament)
leaderboard = utils.parse_json(leaderboard_url)

t_name = tournament['trnName']['official']
if t_name is 'Masters Tournament':
    t = masters.scrape(leaderboard)

elif t_name is 'U.S. Open':
    tee_times_url = 'https://gripapi-static-pd.usopen.com/gripapi/teetimes.json'
    tee_times = utils.parse_json(tee_times_url)
    t = usopen.scrape(leaderboard, tee_times)

elif t_name is 'The Open Championship':
    t = open.scrape(leaderboard)

elif t_name is 'PGA Championship':
    t = pga.scrape(leaderboard)

elif t_name is 'THE PLAYERS Championship':
    t = players.scrape(leaderboard)

else:
    t = pgatour.scrape(leaderboard)




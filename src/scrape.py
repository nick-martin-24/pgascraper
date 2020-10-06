from scrapeutils import utils, pgatour


MAJOR_TOURNAMENT_NAMES = ['Masters Tournament',
                          'U.S. Open',
                          'The Open Championship',
                          'PGA Championship',
                          'THE PLAYERS Championship']

tournament = utils.get_current_tournament()
tournament_urls = utils.get_urls(tournament)
tournament_data = utils.parse_json(tournament_urls)

t_name = tournament['trnName']['official']
if t_name == 'Masters Tournament':
    t = masters.scrape(leaderboard)

elif t_name == 'U.S. Open':
    tee_times_url = 'https://gripapi-static-pd.usopen.com/gripapi/teetimes.json'
    tee_times = utils.parse_json(tee_times_url)
    t = usopen.scrape(leaderboard, tee_times)

elif t_name == 'The Open Championship':
    t = open.scrape(leaderboard)

elif t_name == 'PGA Championship':
    t = pga.scrape(leaderboard)

elif t_name == 'THE PLAYERS Championship':
    t = players.scrape(leaderboard)

else:
    t = pgatour.scrape(tournament_data[0])




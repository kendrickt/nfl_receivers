from player import Player
from runningbacks.runningbacks import rbs_2015, rbs_2014, rbs_2013, rbs_2012


def get_players(startyear, endyear):
    years = range(startyear, endyear+1)
    players = {}
    for year in years:
        players_temp = get_players_from_one_year(year)
        for player in players_temp:
            if (player.name, player.team) in players.keys():
                players[(player.name, player.team)].combine(player)
                pass
            else:
                players[(player.name, player.team)] = player
    return players.values()


def get_players_from_one_year(year):
    f = file('stats_raw/receiver_stats_%d.csv' % year, 'r')
    players = []
    for line in f:
        data = line.split(',')
        player = Player(data[1], data[0])
        home_stats = [float(stat) for stat in data[3:11]]
        away_stats = [float(stat) for stat in data[11:]]
        player.change_home(home_stats)
        player.change_away(away_stats)
        players.append(player)
    f.close()
    return players


def remove_rbs(players, year):
    if year == 2015:
        rbs = rbs_2015
    elif year == 2014:
        rbs = rbs_2014
    elif year == 2013:
        rbs = rbs_2013
    elif year == 2012:
        rbs = rbs_2012
    else:
        raise ValueError('No running backs recorded for %d' % year)

    return filter(lambda x: (x.name, x.team) not in rbs, players)


def filter_by_playoffs(players):
    playoffteams = ['GB', 'ARI', 'CAR', 'SEA', 'KC', 'PIT', 'DEN', 'NE']
    return filter(lambda x: x.team in playoffteams, players)


def filter_players(players, func_key, min_val):
    return filter(lambda x: func_dict[func_key](x) > min_val, players)


func_dict = {
    'yds': lambda x: x.yds(),
    'comps': lambda x: x.comps(),
    'atts': lambda x: x.atts(),
    'compperc': lambda x: x.compperc(),
    'attspergame': lambda x: x.atts_per_game(),
    'ydspercomp': lambda x: x.yds_per_comp(),
    'compspergame': lambda x: x.comps_per_game(),
    'ydsperatt': lambda x: x.yds_per_att(),
    'tds': lambda x: x.tds(),
    'tdspergame': lambda x: x.tdspergame()
}


"""
    blog 1
    plot completion percentage vs number of attempts,
    but only the top 30 players wrt attepts
    plots yds per catch vs number of catches per game,
    only the top 30 players wrt catches per game

    filter by playoff teams
        then plot the same two things above.
"""

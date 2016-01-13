import sys
from player import Player
from matplotlib import pyplot as plt
import math
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
        raise ValueError('No running backs recorded for %d' % year )

    return filter(lambda x: (x.name, x.team) not in rbs, players)


def filter_by_playoffs(players):
    playoffteams = ['GB', 'ARI', 'CAR', 'SEA', 'KC', 'PIT', 'DEN', 'NE']
    return filter(lambda x: x.team in playoffteams, players)


def filter_players(players, func_key, min_val):
    return filter(lambda x: func_dict[func_key](x) > min_val, players)


def sort_players(players, func_key):
    func = func_dict[func_key]
    players.sort(key=func, reverse=True)


def write_2_file(players, filename, stat=None):
    f = file('stats_reordered/%s.csv' % filename, 'w')
    for player in players:
        if stat:
            f.write('%s,%s' % player.name, player.team)
            f.write(func_dict[stat](player))
            f.write('\n')
        else:
            f.write('%s\n' % str(player))


def plot_baldwin_year(year, stat, miny, maxy, playoffs=False):
    filename = 'plots/attspergame_vs_%s_%d' % (stat, year)
    players = get_players(year, year)
    players = remove_rbs(players, year)
    players = filter_players(players, 'atts', 20)
    teams = {'SEA':'g'} 
    plot_players(filename, players, 'attspergame', stat, 
            teams=teams, minx=1, miny=miny, maxx=13, maxy=maxy)

    if playoffs:
        players = filter_by_playoffs(players)
        filename = 'plots/attspergame_vs_%s_2015_playoffs' % stat
        teams = {'SEA':'g', 'CAR':'b'} 
        plot_players(
                filename, players, 'attspergame', stat, 
                teams=teams, minx=1, miny=miny, maxx=13, maxy=maxy, 
                plot_good=False
        )


def plot_players(
        filename, players, xaxis, yaxis,
        teams=None,
        minx=0, miny=0, maxx=0, maxy=0, plot_good=True):
    if minx:
        players = filter_players(players, xaxis, minx)
    if miny:
        players = filter_players(players, yaxis, miny)

    xfunc = func_dict[xaxis]
    yfunc = func_dict[yaxis]

    # Initialize min and max axes values
    x_min, x_max = sys.maxint, 0
    y_min, y_max = sys.maxint, 0

    plt.figure()
    for player in players:
        x_val, y_val = xfunc(player), yfunc(player)
        
        if player.team in teams.keys():
            color = teams[player.team]
            zorder = 2
            plt.text(
                    x_val, 
                    y_val, 
                    player.name, 
                    color='k', 
                    size='small', 
                    weight='heavy',
                    zorder=zorder)

        else:
            color = 'grey'
            zorder = 0
        plt.plot(
                x_val, y_val, 'o', 
                color=color,
                zorder=zorder,
                markersize=player.tds() + 3)

        # Label good players
        if plot_good and (player.name, player.team) in good_receivers:
            plt.text(
                    x_val, 
                    y_val, 
                    player.name, 
                    color='k', 
                    size='small', 
                    weight='heavy',
                    zorder=2)

        # determine min and max axes values
        x_min, x_max = min(x_val, x_min), max(x_val, x_max)
        y_min, y_max = min(y_val, y_min), max(y_val, y_max)

    # Set min and max axes values
    marginsize = 10.0
    if maxx:
        plt.xlim(minx, maxx)
    else:
        x_diff = x_max - x_min
        plt.xlim(x_min - x_diff/marginsize, x_max + x_diff/marginsize)

    if maxy:
        plt.ylim(miny, maxy)
    else:
        y_diff = y_max - y_min
        plt.ylim(y_min - y_diff/marginsize, y_max + y_diff/marginsize)

    plt.xlabel(xaxis, size='large')
    plt.ylabel(yaxis, size='large')
    plt.title(filename, size='large')
    plt.savefig('%s' % filename)

    plt.show()

    plt.close()

func_dict = {
    'yds': lambda x: x.yds(),
    'comps': lambda x: x.comps(),
    'atts': lambda x: x.atts(),
    'compperc': lambda x: x.compperc(),
    'attspergame': lambda x: x.atts_per_game(),
    'ydspercomp': lambda x: x.yds_per_comp(),
    'compspergame': lambda x: x.comps_per_game(),
    'ydsperatt': lambda x: x.yds_per_att()
}


good_receivers = [
    ('A.Brown', 'PIT'),
    ('J.Jones', 'ATL'),
    ('D.Thomas', 'DEN'),
    ('D.Hopkins', 'HOU'),
    ('B.Marshall', 'NYJ'),
    ('D.Bryant', 'DAL'),
    ('C.Johnson', 'DET'),
    ('T.Hilton', 'IND'),
    ('L.Fitzgerald', 'ARI'),
    ('A.Green', 'CIN')
]


if __name__ == "__main__":
    plot_baldwin_year(2015, 'compperc', 0, 1.1, playoffs=True)
    plot_baldwin_year(2014, 'compperc', 0, 1.1)
    plot_baldwin_year(2013, 'compperc', 0, 1.1)
    plot_baldwin_year(2012, 'compperc', 0, 1.1)


    plot_baldwin_year(2015, 'ydsperatt', 0, 15, playoffs=True)
    plot_baldwin_year(2014, 'ydsperatt', 0, 15)
    plot_baldwin_year(2013, 'ydsperatt', 0, 15)
    plot_baldwin_year(2012, 'ydsperatt', 0, 15)
"""
    blog 1
    plot completion percentage vs number of attempts,
    but only the top 30 players wrt attepts
    plots yds per catch vs number of catches per game,
    only the top 30 players wrt catches per game

    filter by playoff teams
        then plot the same two things above.
"""

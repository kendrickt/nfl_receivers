import sys
from player import Player
from matplotlib import pyplot as plt


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
        home_stats = [float(stat) for stat in data[3:10]]
        away_stats = [float(stat) for stat in data[10:]]
        player.change_home(home_stats)
        player.change_away(away_stats)
        players.append(player)
    f.close()
    return players


def filter_by_playoffs(players):
    playoffteams = ['GB', 'ARI', 'CAR', 'SEA', 'KC', 'PIT', 'DEN', 'NE']
    return filter(lambda x: x.team in playoffteams, players)


def filter_players(players, func_key, min_val):
    return filter(lambda x: func_dict[func_key](x) > min_val, players)


def sort_players(players, func_key):
    func = func_dict[func_key]
    players.sort(key=func, reverse=True)


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


def write_2_file(players, filename, stat=None):
    f = file('stats_reordered/%s.csv' % filename, 'w')
    for player in players:
        if stat:
            f.write('%s,%s' % player.name, player.team)
            f.write(func_dict[stat](player))
            f.write('\n')
        else:
            f.write('%s\n' % str(player))


def plot_players(players, xaxis, yaxis, minx=0, miny=0):
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
        if player.team == 'SEA':
            color = 'g'
        elif player.team == 'CAR':
            color = 'b'
        else:
            color = 'k'
        plt.text(x_val, y_val, player.name, color=color)

        # determine min and max axes values
        x_min, x_max = min(x_val, x_min), max(x_val, x_max)
        y_min, y_max = min(y_val, y_min), max(y_val, y_max)

    # Set min and max axes values
    x_diff, y_diff = x_max - x_min, y_max - y_min
    marginsize = 10.0
    plt.xlim(x_min - x_diff/marginsize, x_max + x_diff/marginsize)
    plt.ylim(y_min - y_diff/marginsize, y_max + y_diff/marginsize)

    plt.xlabel(xaxis, size='large')
    plt.ylabel(yaxis, size='large')
    plt.show()

    plt.close()


if __name__ == "__main__":
    players = get_players(2015, 2015)

    plot_players(players, 'atts', 'compperc', minx=50, miny=0.55)
    plot_players(players, 'attspergame', 'ydsperatt', minx=4)

    players = filter_by_playoffs(players)
    plot_players(players, 'atts', 'compperc', minx=10, miny=0.35)
    plot_players(players, 'attspergame', 'ydsperatt', minx=2)

"""
    blog 1
    plot completion percentage vs number of attempts,
    but only the top 30 players wrt attepts
    plots yds per catch vs number of catches per game,
    only the top 30 players wrt catches per game

    filter by playoff teams
        then plot the same two things above.
"""
"""
    filename = sys.argv[1]
    f = file(filename, 'r')
    players = []
    for line in f:
        data = line.split(',')
        player = Player(data[1], data[0], data[2])
        home_stats = [float(stat) for stat in data[3:10]]
        away_stats = [float(stat) for stat in data[10:]]
        player.change_home(home_stats)
        player.change_away(away_stats)
        players.append(player)
    f.close()

    # Filter by playoff teams
    playoffteams = ['GB', 'ARI', 'CAR', 'SEA', 'KC', 'PIT', 'DEN', 'NE']
    players = filter(lambda x: x.team in playoffteams, players)

    # Filter by completions
    players = filter(lambda x: x.comps() > 20, players)

    # Sort the set of players
    func_key = sys.argv[2]
    func = func_dict[func_key]
    players.sort(key=func, reverse=True)

    # Write the top N players
    N = int(sys.argv[3])
    f = file(filename + 'temp', 'w')
    for player in players[0:N]:
        f.write('%s\n' % str(player))
    f.close()
"""

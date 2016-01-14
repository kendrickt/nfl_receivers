import numpy as np
from matplotlib import pyplot as plt
from format_stats import func_dict, get_players, remove_rbs, filter_players, \
    filter_by_playoffs


def plot_baldwin_year(year, stat, zfunc, miny, maxy, playoffs=False):
    filename = 'plots/attspergame_vs_%s_%d' % (stat, year)
    players = get_players(year, year)
    players = remove_rbs(players, year)
    players = filter_players(players, 'tds', 1)
    players = filter_players(players, 'atts', 10)

    for player in players:
        if player.name == 'M.Lynch':
            print player

    teams = {'SEA': 'g'}
    plot_players(filename, players, 'attspergame', stat, zfunc,
                 teams=teams, minx=1, miny=miny, maxx=13, maxy=maxy)

    if playoffs:
        players = filter_by_playoffs(players)
        filename = 'plots/attspergame_vs_%s_2015_playoffs' % stat
        teams = {'SEA': 'g', 'CAR': 'b'}
        plot_players(
            filename, players, 'attspergame', stat, zfunc,
            teams=teams, minx=1, miny=miny, maxx=13, maxy=maxy,
            plot_good_receivers=False, best_fit=False
        )


def plot_players(
        filename, players, xaxis, yaxis, zfunc,
        teams=None,
        minx=0, miny=0, maxx=0, maxy=0,
        plot_good_receivers=True, best_fit=True):
    if minx:
        players = filter_players(players, xaxis, minx)
    if miny:
        players = filter_players(players, yaxis, miny)

    xfunc = func_dict[xaxis]
    yfunc = func_dict[yaxis]

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
                markersize=zfunc(player))

        # Label good players
        if plot_good_receivers and (player.name, player.team) in good_receivers:
            plt.text(
                    x_val,
                    y_val,
                    player.name,
                    color='k',
                    size='small',
                    weight='heavy',
                    zorder=2)

    # Set min and max axes values
    plt.xlim(minx, maxx)
    plt.ylim(miny, maxy)

    if best_fit:
        p = get_best_fit(players, xaxis, yaxis)
        xp = np.linspace(minx, maxx, 100)
        plt.plot(xp, p(xp), '-')

    plt.xlabel(xaxis, size='large')
    plt.ylabel(yaxis, size='large')
    plt.title(filename, size='large')

    plt.savefig('%s' % filename)
    plt.close()


def get_best_fit(players, xaxis, yaxis):
    x = []
    y = []
    for player in players:
        x.append(func_dict[xaxis](player))
        y.append(func_dict[yaxis](player))
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    return p


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
    plot_baldwin_year(2015, 'compperc', func_dict['tds'], 0, 1.1, playoffs=True)
    plot_baldwin_year(2014, 'compperc', func_dict['tds'], 0, 1.1)
    plot_baldwin_year(2013, 'compperc', func_dict['tds'], 0, 1.1)
    plot_baldwin_year(2012, 'compperc', func_dict['tds'], 0, 1.1)

    plot_baldwin_year(2015, 'ydsperatt', func_dict['tds'], 0, 15, playoffs=True)
    plot_baldwin_year(2014, 'ydsperatt', func_dict['tds'], 0, 15)
    plot_baldwin_year(2013, 'ydsperatt', func_dict['tds'], 0, 15)
    plot_baldwin_year(2012, 'ydsperatt', func_dict['tds'], 0, 15)

    plot_baldwin_year(
        2015, 'tdspergame', lambda x: 6, 0, 1.2, playoffs=True)
    plot_baldwin_year(
        2014, 'tdspergame', lambda x: 6, 0, 1.2)
    plot_baldwin_year(
        2013, 'tdspergame', lambda x: 6, 0, 1.2)
    plot_baldwin_year(
        2012, 'tdspergame', lambda x: 6, 0, 1.2)

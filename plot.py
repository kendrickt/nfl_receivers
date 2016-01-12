from matplotlib import pyplot as plt
import sys
from Player import Player


if __name__ == "__main__":
    print "hello"

    years = sys.argv[1:]
    for year in years:
        f = file("receiver_stats_" + year + ".csv", "r")
        players = []
        for line in f:
            data = line.split(',')
            player = Player(data[1], data[0], data[2])
            home_stats = [int(stat) for stat in data[3:10]]
            away_stats = [int(stat) for stat in data[10:]]
            player.change_home(home_stats)
            player.change_away(away_stats)
            players.append(player)
        f.close()

        """
        players.sort(key=lambda x: x.total_yds(), reverse=True)
        f = file("yds_" + year + ".csv", "w")
        for player in players:
            f.write(str(player) + "\n")
        f.close()

        players.sort(key=lambda x: x.total_atts(), reverse=True)
        f = file("atts_" + year + ".csv", "w")
        for player in players:
            f.write(str(player) + "\n")
        f.close()

        players.sort(key=lambda x: x.total_atts_per_game(), reverse=True)
        f = file("atts_per_game_" + year + ".csv", "w")
        for player in players:
            f.write(str(player) + "\n")
        f.close()
        """

        best_fit_x = []
        best_fit_y = []

        plt.figure()
        xmax = 0
        xmin = 700
        ymax = 0.0
        ymin = 1.0
        for player in players:
            if player.deep_comps() < 3 or not player.deep_atts():
                continue

            xmax = max(xmax, player.deep_atts())
            xmin = min(xmin, player.deep_atts())
            ymax = max(ymax, float(player.deep_comps())/player.deep_atts())
            ymin = min(ymin, float(player.deep_comps())/player.deep_atts())

            best_fit_x.append(player.deep_atts())
            best_fit_y.append(float(player.deep_comps())/player.deep_atts())

        """
        best_fit_coeff = np.polyfit(best_fit_x, best_fit_y, 2)
        print best_fit_coeff
        best_fit_line = [
            best_fit_coeff[0] + best_fit_coeff[1] * x + best_fit_coeff[2]*x**2
            for x in xrange(xmin, xmax)
        ]
        plt.show()
        """

        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        for player in players:
            if player.deep_comps() < 3 or not player.deep_atts():
                continue

            plt.text(
                player.deep_atts(),
                float(player.deep_comps())/player.deep_atts(),
                player.name)
        plt.xlabel("# of completions")
        plt.ylabel("% of completions")
        plt.show()

import sys
from Player import Player


if __name__ == "__main__":
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

        players.sort(key=lambda x: x.total_comps()/x.total_atts(), reverse=True)
        f = file("comp_perc_" + year + ".csv", "w")
        for player in players:
            if player.total_comps() < 20:
                continue
            f.write(str(player) + "\n")
        f.close()

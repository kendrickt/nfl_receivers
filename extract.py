import re
import nflgame
import sys
from player import Player


def preprocess_play(play, f_penalty):
    pattern_name = re.compile('[A-Z][a-z]*[\. ][A-Z][a-z]*')
    pattern_yds = re.compile('-*[0-9]+')
    pattern_team = re.compile('^\(([A-Z]+)')

    if "PENALTY" in play or "challenged" in play or "penalty" in play:
        f_penalty.write(play + '\n')

    """
    If "no-play" in play, return 0.
    if challenged, but play stands, then continue.
    if challenged and play reversed, get the second play.
    """

    if ("PENALTY" in play or "TWO-POINT" in play or "INTERCEPTED" in play or
            "sacked" in play or "challenged" in play):
        return 0
    if not ("short" in play or "deep" in play or "incomplete" in play):
        return 0

    team = pattern_team.findall(play)[0]
    play = re.sub('\([^)]*\)', '', play)
    play = re.sub('\[[^)]*\]', '', play)
    play = re.sub('no gain', '0', play)
    play = re.sub('[A-Z]\.[a-zA-Z]+ reported in as eligible.', '', play)
    matches_name = pattern_name.findall(play)
    matches_yds = pattern_yds.findall(play)

    if len(matches_name) == 1:
        return 0
    elif len(matches_name) < 2:
        raise StandardError("oops")
    name = matches_name[1]

    if "incomplete" in play:
        yds = 0
    elif "TOUCHDOWN" in play:
        yds = int(matches_yds[0])
    else:
        yds = int(matches_yds[1])

    return (team, name, yds)


def process_game(game, year, f_penalty):
    players = {}
    hometeam = game.home
    plays = nflgame.combine_plays([game])
    for play in plays:

        # Preprocess and then parse a play string
        play = str(play)
        parsed_play = preprocess_play(play, f_penalty)
        if not parsed_play:
            continue  # Something irrelevant happened, e.g. running play.
        team, name, yds = parsed_play[0], parsed_play[1], parsed_play[2]

        # Make or get a player from the player dictionary
        if (name, team, year) not in players.keys():
            player = Player(name, team, year)
            if team == hometeam:
                player.home.games = 1
            else:
                player.away.games = 1
            players[(name, team, year)] = player
        else:
            player = players[(name, team, year)]

        # Update a player's receiving stats
        player.update_player(play, hometeam, yds)

    return players


def combine_player_dicts(main_dict, aux_dict):
    for player in aux_dict:
        if player in main_dict.keys():
            main_dict[player].combine(aux_dict[player])
        else:
            main_dict[player] = aux_dict[player]


def write_player_stats(players, f):
    for player in players:
        f.write('%s\n' % str(players[player]))


if __name__ == "__main__":
    years = [int(year) for year in sys.argv[1:]]
    for year in years:
        f = file("stats_raw/receiver_stats_%s.csv" % year, "w")
        players = {}
        f_penalty = file("penalties/penalties_%s.txt" % year, 'w')

        games = nflgame.games(year)
        for game in games:
            curr_players = process_game(game, year, f_penalty)
            combine_player_dicts(players, curr_players)

        write_player_stats(players, f)
        f.close()
        f_penalty.close()

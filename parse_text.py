import re
import nflgame
import sys
from Player import Player


def preprocess_play(play, f_penalty):
    pattern_name = re.compile('[A-Z][a-z]*[\. ][A-Z][a-z]*')
    pattern_yds = re.compile('-*[0-9]+')
    pattern_team = re.compile('^\(([A-Z]+)')

    if "PENALTY" in play or "challenged" in play:
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


if __name__ == "__main__":
    f_penalty = file("penalties.txt", 'w')

    players = {}
    years = [int(year) for year in sys.argv[1:]]
    for year in years:
        f = file("receiver_stats_" + str(year) + ".csv", "w")

        games = nflgame.games(year)
        for game in games:
            this_games_players = {}
            hometeam = game.home
            plays = nflgame.combine_plays([game])
            for play in plays:

                # Preprocess and then parse a play string.
                play = str(play)
                parsed_play = preprocess_play(play, f_penalty)
                if not parsed_play:
                    continue
                team, name, yds = parsed_play[0], parsed_play[1], parsed_play[2]

                # Make a player if they don't already exist. Otherwise, get him.
                if (name, team, year) not in this_games_players:
                    this_games_players[(name, team, year)] = Player(
                        name, team, year)
                    print name, team, year
                player = this_games_players[(name, team, year)]

                # Update a player's receiving statistics
                player.update_player(play, hometeam, yds)

            # Combine this_games_players with players.
            for player in this_games_players:
                if player in players:
                    players[player].combine(this_games_players[player])
                else:
                    players[player] = this_games_players[player]

        # Output player statistics for each year.
        for player in players:
            f.write(str(players[player]) + '\n')
        f.close()

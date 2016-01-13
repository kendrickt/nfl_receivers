class Player(object):

    def __init__(self, name, team, year=None):
        self.name = name
        self.team = team
        self.year = year
        self.away = Passes()
        self.home = Passes()

    def completion(self, hometeam, short, yds):
        if hometeam == self.team:
            self.home.completion(short, yds)
        else:
            self.away.completion(short, yds)

    def incompletion(self, hometeam, short):
        if hometeam == self.team:
            self.home.incompletion(short)
        else:
            self.away.incompletion(short)

    def yds(self):
        return self.away.total_yds() + self.home.total_yds()

    def comps(self):
        return (self.away.total_comps() + self.home.total_comps())

    def atts(self):
        return (self.away.total_atts() + self.home.total_atts())

    def compperc(self):
        if self.comps():
            return float(self.comps()) / self.atts()
        return 0

    def games(self):
        return (self.away.games + self.home.games)

    def yds_per_att(self):
        if self.yds():
            return float(self.yds()) / self.atts()
        return 0

    def yds_per_comp(self):
        if self.yds():
            return float(self.yds()) / self.comps()
        return 0

    def yds_per_game(self):
        if self.yds():
            return float(self.yds()) / self.games()
        return 0

    def atts_per_game(self):
        if self.atts():
            return float(self.atts())/self.games()
        return 0

    def comps_per_game(self):
        if self.comps():
            return float(self.comps())/self.games()
        return 0

    def tds(self):
        return (self.home.tds + self.away.tds)

    def tdspergame(self):
        return float(self.tds()) / self.games()

    def tdsperatt(self):
        return float(self.tds()) / self.atts()

    def combine(self, other):
        self.home.combine(other.home)
        self.away.combine(other.away)

    def update_player(self, play, hometeam, yds):
        # Short or deep pass?
        if "short" in play:
            short = True
        elif "deep" in play:
            short = False
        else:
            short = True

        # This is an incomplete pass.
        if "incomplete" in play:
            self.incompletion(hometeam, short)

        # This is a complete pass
        else:
            self.completion(hometeam, short, yds)

        if 'TOUCHDOWN' in play:
            self.touchdown(hometeam)

    def touchdown(self, hometeam):
        if hometeam == self.team:
            self.home.tds += 1
        else:
            self.away.tds += 1

    def change_home(self, stats):
        self.home.change(stats)

    def change_away(self, stats):
        self.away.change(stats)

    def __repr__(self):
        return (self.team + ',' + self.name + ',' + str(self.year) + ',' +
                self.home.__repr__() + ',' + self.away.__repr__())


class Passes(object):

    def __init__(self):
        self.comp_short = 0.0
        self.att_short = 0.0
        self.yds_short = 0.0
        self.comp_deep = 0.0
        self.att_deep = 0.0
        self.yds_deep = 0.0
        self.tds = 0.0
        self.games = 0.0

    def completion(self, short, yds):
        if short:
            self.comp_short += 1
            self.att_short += 1
            self.yds_short += yds
        else:
            self.comp_deep += 1
            self.att_deep += 1
            self.yds_deep += yds

    def incompletion(self, short):
        if short:
            self.att_short += 1
        else:
            self.att_deep += 1

    def total_yds(self):
        return self.yds_short + self.yds_deep

    def total_comps(self):
        return self.comp_short + self.comp_deep

    def total_atts(self):
        return self.att_short + self.att_deep

    def combine(self, other):
        self.comp_short += other.comp_short
        self.comp_deep += other.comp_deep
        self.att_short += other.att_short
        self.att_deep += other.att_deep
        self.yds_short += other.yds_short
        self.yds_deep += other.yds_deep
        self.games += other.games
        self.tds += other.tds

    def change(self, stats):
        self.comp_short = stats[0]
        self.att_short = stats[1]
        self.yds_short = stats[2]
        self.comp_deep = stats[3]
        self.att_deep = stats[4]
        self.yds_deep = stats[5]
        self.games = stats[6]
        self.tds = stats[7]

    def __repr__(self):
        return (str(self.comp_short) + "," + str(self.att_short) + "," +
                str(self.yds_short) + "," + str(self.comp_deep) + "," +
                str(self.att_deep) + "," + str(self.yds_deep) + "," +
                str(self.games) + "," + str(self.tds))

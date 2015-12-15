class Player(object):

    def __init__(self, name, team, year):
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

    def total_yds(self):
        return self.away.total_yds() + self.home.total_yds()

    def total_comps(self):
        return (self.away.total_comps() + self.home.total_comps())

    def total_atts(self):
        return (self.away.total_atts() + self.home.total_atts())

    def total_atts_per_game(self):
        return (self.away.total_atts() + self.home.total_atts())/self.home.games

    def short_yds(self):
        return self.away.short_yds() + self.home.short_yds()

    def short_comps(self):
        return (self.away.short_comps() + self.home.short_comps())

    def short_atts(self):
        return (self.away.short_atts() + self.home.short_atts())

    def short_atts_per_game(self):
        return (self.away.short_atts() + self.home.short_atts())/self.home.games

    def deep_yds(self):
        return self.away.deep_yds() + self.home.deep_yds()

    def deep_comps(self):
        return (self.away.deep_comps() + self.home.deep_comps())

    def deep_atts(self):
        return (self.away.deep_atts() + self.home.deep_atts())

    def deep_atts_per_game(self):
        return (self.away.deep_atts() + self.home.deep_atts())/self.home.games

    def combine(self, other):
        self.away.combine(other.away)
        self.home.combine(other.home)

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
        self.games = 1.0

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

    def short_yds(self):
        return self.yds_short

    def short_comps(self):
        return self.comp_short

    def short_atts(self):
        return self.att_short

    def deep_yds(self):
        return self.yds_deep

    def deep_comps(self):
        return self.comp_deep

    def deep_atts(self):
        return self.att_deep

    def combine(self, other):
        self.comp_short += other.comp_short
        self.comp_deep += other.comp_deep
        self.att_short += other.att_short
        self.att_deep += other.att_deep
        self.yds_short += other.yds_short
        self.yds_deep += other.yds_deep
        self.games += other.games

    def change(self, stats):
        self.comp_short = stats[0]
        self.att_short = stats[1]
        self.yds_short = stats[2]
        self.comp_deep = stats[3]
        self.att_deep = stats[4]
        self.yds_deep = stats[5]
        self.games = stats[6]

    def __repr__(self):
        return (str(self.comp_short) + "," + str(self.att_short) + "," +
                str(self.yds_short) + "," + str(self.comp_deep) + "," +
                str(self.att_deep) + "," + str(self.yds_deep) + "," +
                str(self.games))

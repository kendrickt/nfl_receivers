import re


class JSON_Parser(object):

    def __init__(self):
        self.pat_name = re.compile('[a-zA-Z]+\.[a-zA-Z]+')
        self.pat_yds = re.compile('-*[0-9]+')
        self.pat_team = re.compile('^\(([A-Z]+)')

    def process_play(self, play):
        pass

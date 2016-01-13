import sys
try:
    from teamdict import team_dict
except Exception as e:
    print e
    print 'team_dict is not created yet. I hope you are using buildteams'

def build_team_dict():
    f = file('rbs_2015.txt', 'r')
    f_teamdict = file('teamdict.py', 'w')

    team_dict = {}

    for line in f:
        data = line.split('\t')
        if len(data) == 3 and data[0] != 'NAME':
            data_team = data[1]
            if data_team not in team_dict.keys():
                abbr = raw_input('%s abbreviation? ' % data_team)
                team_dict[data_team] = abbr

    f_teamdict.write('team_dict = {\n')
    for item in team_dict.items():
        f_teamdict.write('\t\'%s\': \'%s\',\n' % (item[0], item[1]))
    f_teamdict.write('}')

    f_teamdict.close()
    f.close()


def build_rbs():
    f = file('rbs_2015.txt', 'r')
    f_rb = file('runningbacks.py', 'w')

    f_rb.write('rbs_2015 = [\n')

    for line in f:
        data = line.split('\t')
        if len(data) != 3:
            continue

        if data[0] == 'NAME':
            continue

        data_name = data[0]
        data_name = data_name.split(', ')
        lastname = data_name[0]
        firstname = data_name[1]
        name = '%s.%s' % (firstname[0].capitalize(), lastname)

        data_team = data[1]
        team = team_dict[data_team]

        f_rb.write('\t(\'%s\',\'%s\'),\n' % (name, team))

    f_rb.write(']\n\n')

    f_rb.close()
    f.close()

if __name__ == '__main__':
    func = sys.argv[1]
    if func == 'buildteams':
        build_team_dict()
    elif func == 'buildrbs':
        build_rbs()

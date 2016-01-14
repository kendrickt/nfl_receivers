import re


if __name__ == '__main__':
    years = ['2012', '2013', '2014']
    f_rb = file('runningbacks.py', 'a')

    for year in years:
        f = file('rbs_%s.txt' % year, 'r')

        f_rb.write('rbs_%s = [\n' % year)
        for line in f:
            # Get name and team information
            data = line.split('\t')
            name_info = data[1]
            team_info = data[2]

            # if RB, format name and write to file
            name_info = re.split(', | ', name_info)
            if len(name_info) < 3:
                continue

            if name_info[2] == 'RB':
                name = '%s.%s' % (name_info[0][0], name_info[1])

                teams = team_info.split('/')
                for team in teams:
                    if team == 'JAX':
                        team = 'JAC'
                    elif team == 'WSH':
                        team = 'WAS'

                    f_rb.write('\t(\'%s\',\'%s\'),\n' % (name, team))

        f_rb.write(']\n\n')

import os
import pandas as pd
from pandas.plotting import parallel_coordinates
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import options
from cycler import cycler

data_dir = '../output_csv/gameProgressions'

#loading in the options file
teams_seasons = options.teams_seasons

#set rc params for matplotlib
plt.style.use('dark_background')
plt.rc('lines', linewidth=1)
plt.rc('lines', markersize=8)
plt.rc('axes', prop_cycle=(cycler('marker', ['.','*','+','x']))+ cycler('linestyle', ['-', ':', '--','-.']), axisbelow=True)


def plotGameProgressions():

    team_folders = os.listdir(data_dir)

    for team_folder in team_folders:
        seasons = os.listdir(f'{data_dir}/{team_folder}')

        for season in seasons:
            print(f'\n\nPlotting game progressions for team {team_folder}, season {season}')
            games = os.listdir(f'{data_dir}/{team_folder}/{season}')

            for game in games:
                df, home, away, date = convert_stats(data_dir, team_folder, season, game)
                print(df.head(50))

                plotDF(df, team_folder, season,home, away, date)





def convert_stats(data_dir, team_folder, season, game):

    time = []
    score = []
    cols = []
    with open(f'{data_dir}/{team_folder}/{season}/{game}', 'r') as infile:
        lines = infile.readlines()
        n = 0
        for line in lines:
            # line = line.decode('utf-8')
            if n == 0:
                line = line[:-1]
                cols.extend(line.split(','))
                n += 1
            else:
                line = line.split(',')
                time.append(str(line[0]))
                score.append(str(line[1][:-1]))
                n += 1

        data = reversed(list(zip(time, score)))

        df = pd.DataFrame(data, columns=cols)

        # check which team was home or away, adjust goal diff accordingly
        homeAway = 1000
        ha = game[9:].split('_')
        home = ha[0]
        away = ha[1][:-4]
        date = game[:9]
        us = ['lakeside', 'wacker', 'steffisburg']
        if any(us in home.lower() for us in us):
            homeAway = 0
        else:
            homeAway = 1

        # calculate new columns
        df['GDoT'] = df['score'].apply(lambda x: convert_score(x, homeAway))
        df['time'] = df['timestamp'].apply(lambda t: convert_time(t))

        return df, home, away, date


def convert_score(x, homeAway):
    try:
        if homeAway == 0:
            string = str(x).split(':')
            diff = round(int(string[0])-int(string[1]),1)
            return diff
        else:
            string = str(x).split(':')
            diff = round(int(string[1]) - int(string[0]), 1)
            return diff

    except (ValueError, IndexError) as e:
        return x


def convert_time(t):

    try:
        minutes = int(t.split(':')[0])
        seconds = int(t.split(':')[1])/60
        return round(minutes + seconds, 1)

    except (ValueError, IndexError) as e:
        return t


def plotDF(df, team_folder, season, home, away, date):

    league = team_folder.split(' ')[-1]
    d = date.split("_")
    date = "/".join(d)[:-1]

    # plotting stuff
    fontP = FontProperties()
    fontP.set_size('small')

    plot = df.plot.area(x = 'time', y = 'GDoT', stacked=False, colormap='viridis_r', zorder=1000)
    plt.grid(linestyle='-', linewidth='0.5', color='white', alpha=0.1, zorder=1)
    gridlines = plot.xaxis.get_gridlines()
    gridlines[4].set_linewidth(2)
    gridlines[4].set_alpha(0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)
    plt.title(f'Goal Differential over Time:\n {date} {home} vs. {away} ({league})')
    plt.ylabel('Goal Differential')
    plt.xlabel('Game Time [min]')
    plt.tight_layout()

    plt.savefig(f'../output_png/gameProgressions/{team_folder}/{season}/{date.replace("/", "-")}_{home.strip(" ")}_{away.strip(" ")}_goalDifferential')

if __name__ == '__main__':
    plotGameProgressions()
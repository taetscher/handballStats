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
plt.rc('lines', markersize=6)
plt.rc('axes', prop_cycle=(cycler('marker', ['.','*','+','x']))+ cycler('linestyle', ['-', ':', '--','-.']), axisbelow=True)


def plotGameProgressions():

    team_folders = os.listdir(data_dir)

    for team_folder in team_folders:
        seasons = os.listdir(f'{data_dir}/{team_folder}')

        for season in seasons:
            print(f'\n\nPlotting game progressions for team {team_folder}, season {season}')
            games = os.listdir(f'{data_dir}/{team_folder}/{season}')

            plt.close('all')
            for game in games:
                df, home, away, date = convert_stats(data_dir, team_folder, season, game)
                plotDF(0, df, team_folder, season,home, away, date)
                print('..')

            plt.close('all')
            for game in games:
                df, home, away, date = convert_stats(data_dir, team_folder, season, game)
                plotDF(1, df, team_folder, season,home, away, date)
                print('..')






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
        df['Rolling'] = df['GDoT'].rolling(10).mean()

        df['cum_sum'] = df['GDoT'].cumsum()
        df['count'] = range(1, len(df['GDoT']) + 1)
        df['Moving Average'] = df['cum_sum'] / df['count']

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


def plotDF(mode, df, team_folder, season, home, away, date):

    league = team_folder.split(' ')[-1]
    d = date.split("_")
    date = "/".join(d)[:-1]

    # plotting stuff
    fontP = FontProperties()
    fontP.set_size('small')

    #to plot multiple lines in the same plot, re-use the ax object
    ax = plt.gca()

    if mode == 0:
        plot1 = df.plot.area(x='time', y='GDoT', stacked=False, colormap='viridis_r', zorder=1000, ax=ax)
        plot2 = df.plot.line(x='time', y='Moving Average', stacked=False, linestyle='-', linewidth=0.8, marker='',
                             color='orange', zorder=1001, ax=ax)
        plt.grid(linestyle='-', linewidth='0.5', color='white', alpha=0.1, zorder=1)
        gridlines = plot1.xaxis.get_gridlines()
        gridlines[4].set_linewidth(2)
        gridlines[4].set_alpha(0.3)
        plt.ylabel('Goal Differential')
        plt.xlabel('Game Time [min]')
        plt.title(f'Goal Differential over Time:\n {date} {home} vs. {away} ({league})')
        plt.legend(loc='lower center', prop=fontP, facecolor='black', framealpha=0.8).set_zorder(1010)
        plt.tight_layout()
        plt.savefig(f'../output_png/gameProgressions/{team_folder}/{season}/{date.replace("/", "-")}_{home.strip(" ")}_{away.strip(" ")}_goalDifferential')
        plt.close()

    else:
        plot1 = df.plot.area(x='time', y='GDoT', stacked=False, colormap='viridis_r', zorder=1000, ax=ax, alpha=0.1)
        plot2 = df.plot.line(x='time', y='Moving Average', stacked=False, linestyle='-', linewidth=0.8, marker='',
                             color='orange', zorder=1001, ax=ax)
        plt.grid(linestyle='-', linewidth='0.5', color='white', alpha=0.1, zorder=1)
        gridlines = plot1.xaxis.get_gridlines()
        gridlines[4].set_linewidth(2)
        gridlines[4].set_alpha(0.3)
        plt.ylabel('Goal Differential')
        plt.xlabel('Game Time [min]')
        plt.title(f'Goal Differential over Time:\n All Games of {team_folder}, {season}')

        handles, labels = ax.get_legend_handles_labels()
        handle_list, label_list = [], []
        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        plt.legend(handle_list, label_list, loc='lower center', prop=fontP, facecolor='black', framealpha=0.8).set_zorder(1010)

        ax.set_ylim(-15,15)
        plt.tight_layout()
        plt.savefig(f'../output_png/gameProgressions/{team_folder}/{season}/All_Games_goalDifferential')


if __name__ == '__main__':
    plotGameProgressions()
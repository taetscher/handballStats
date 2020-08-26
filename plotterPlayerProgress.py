import os
import pandas as pd
from pandas.plotting import parallel_coordinates
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import options
from cycler import cycler

data_dir = 'playerProgress_data'

#loading in the options file
teams_seasons = options.teams_seasons

#set rc params for matplotlib
plt.style.use('dark_background')
plt.rc('lines', linewidth=1)
plt.rc('lines', markersize=8)
plt.rc('axes', prop_cycle=(cycler('marker', ['.','*','+','x']))+ cycler('linestyle', ['-', ':', '--','-.']), axisbelow=True)
plt.rc('grid', c='white', ls=':', lw=0.4)


def main():
    team_folders = os.listdir(data_dir)

    for team_folder in team_folders:
        seasons = os.listdir(f'{data_dir}/{team_folder}')

        for season in seasons:
            print(f'\n\nanalyzing team {team_folder}, season {season}')
            #get all files in folder
            files = []
            files.extend(os.listdir(f'{data_dir}/{team_folder}/{season}/raw_data'))

            #convert csv files to account for player info and goalie info
            for file in files:
                print('converting file {}...'.format(file))
                csvConverter(file,team_folder,season)

            #read in newly generated, split csvs
            inputs = []
            outfield = []
            goalies = []

            inputs.extend(os.listdir(f'{data_dir}/{team_folder}/{season}'))

            #create list of files for outfield/goalie players
            for file in inputs:
                if str(file).split('_')[-1] == 'outfield.csv':
                    outfield.append(file)
                elif str(file).split('_')[-1] == 'goalies.csv':
                    goalies.append(file)
                else:
                    pass

            #first, generate a list of all players who have played over the course of the whole season
            outfield_players = []
            for file in outfield:
                temp_df = pd.read_csv(f'{data_dir}/{team_folder}/{season}/{file}', encoding='utf-8').fillna(0)
                for player in temp_df['SPIELER']:
                    outfield_players.append(player)
            outfield_players = set(outfield_players)

            stats = ['%', 'TF', 'V', "2'", 'D']

            for stat in stats:
                merged_outfield = mergeStatsOutfield(outfield,outfield_players,stat,team_folder,season)

                #plot time series data of each outfield player to see his/her progress over time
                plotOutfield(merged_outfield,stat,team_folder,season)
                plotOutfieldIndividuals(outfield_players,merged_outfield,stat,team_folder,season)
                write(merged_outfield,team_folder,season,stat)

            # second, generate a list of all goalies who have played over the course of the whole season
            goalie_players = []
            for file in goalies:
                temp_df = pd.read_csv(f'{data_dir}/{team_folder}/{season}/{file}', encoding='utf-8').fillna(0)
                for player in temp_df['TORHÜTER']:
                    goalie_players.append(player)
            goalie_players = set(goalie_players)

            stats = ['P/W','7M','%']

            for stat in stats:
                merged_goalies = mergeStatsGoalie(goalies, goalie_players, stat, team_folder, season)

                # plot time series data of each goalie to see his/her progress over time
                try:
                    try:
                        plotGoalie(merged_goalies, stat,team_folder, season)
                        plotGoalieIndividuals(goalie_players, merged_goalies, stat,team_folder, season)
                    except TypeError:
                        # print('cannot plot data in x/y format (from goalie P/W & 7M, would need to convert to float. '
                        # 'but then the information would get lost because it would be identical to %-stat')
                        pass
                except ValueError:
                    #print('cannot plot data in x/y format (from goalie P/W & 7M, would need to convert to float. '
                          #'but then the information would get lost because it would be identical to %-stat')
                    pass

                write(merged_goalies,team_folder, season, str(stat).replace('/','-')+'_goalie')

    print('\n\nplotting complete')

def csvConverter(infile,team_folder,season):
    """ takes in messy raw data and turns it into readable csv format.
    writes one output file for outfield players and one file for goalies"""
    game_number = infile[4:-4]

    data = []
    with open(f'{data_dir}/{team_folder}/{season}/raw_data/{infile}', 'rb') as infile:

        for line in infile.readlines():
            line = line.decode('utf-8')
            line = line[:-2]
            data.append(line.split(' '))



    date = cleanUp(data[0]).split(' ')[1].replace('.','_')
    date = date[-2:] + '_' + date[3:5] + '_' + date[:2]
    group = cleanUp(data[1])
    team = cleanUp(data[2]) + cleanUp(data[1])
    header_players = str(data[3]).strip('["').strip('"]')

    goalie_index = float('NaN')
    staff_index = float('NaN')

    #find where to slice the data to get player stats
    for entry in data:
        if "'TORHÜTER,P/W,7M,%'" in str(entry):
            index = data.index(entry)
            goalie_index = index + 1
        else:
            pass

    # find where to slice the data to get goalie stats
    for entry in data:
        if "STAFF,V,2',D" in str(entry):
            index = data.index(entry)
            staff_index = index + 1
        else:
            pass
    try:
        #this try/except statement is here because there can be faulty raw_.csv files, avoid those and skip
        #Champions League games, for instance, can trigger these exceptions because of bad stats

        player_data = data[4:goalie_index - 2]
        goalie_data = data[goalie_index:staff_index - 2]
        header_goalies = cleanUp(data[goalie_index - 1]).replace(' ', ',')

        # write the cleaned data into two seperate files
        # outfield players
        with open(f'{data_dir}/{team_folder}/{season}/{date}_{game_number}_outfield.csv', 'w',
                  encoding='utf-8') as outfile:
            outfile.write(header_players + '\n')
            for element in player_data:
                element = element[0].split(',')
                element = str(element[1:]).strip("[").strip("]")

                player_names = eval(element)[:-7]
                player_name = ''
                for segment in player_names:
                    player_name = player_name.strip() + ' ' + segment

                player_stats_in = eval(element)[-7:]
                player_stats = []
                for stat in player_stats_in:
                    player_stats.append(str(stat))

                element = str(player_name) + ',' + str(player_stats).strip('[').strip(']').replace("'", '').replace(' ',
                                                                                                                    '')
                outfile.write(element + '\n')
            outfile.close()

        # goalies
        with open(f'{data_dir}/{team_folder}/{season}/{date}_{game_number}_goalies.csv', 'w',
                  encoding='utf-8') as outfile:
            outfile.write(header_goalies + '\n')
            for element in goalie_data:
                element = element[0].split(',')
                element = str(element[1:]).strip("[").strip("]")

                goalie_names = eval(element)[:-3]
                goalie_name = ''
                for segment in goalie_names:
                    goalie_name = goalie_name.strip() + ' ' + segment

                goalie_stats_in = eval(element)[-3:]
                goalie_stats = []
                for stat in goalie_stats_in:
                    goalie_stats.append(str(stat))

                element = str(goalie_name) + ',' + str(goalie_stats).strip('[').strip(']').replace("'", '').replace(' ',
                                                                                                                    '')
                outfile.write(element + '\n')
            outfile.close()
    except TypeError:
        print('raw_file has errors, skipping this one...')

def cleanUp(inlist):
    return str(inlist).strip("['").strip("']").replace(',',' ')

def pdToInt(dframe,inlist):
    for column in inlist:
        pd.eval(dframe[column],parser='python')

def mergeStatsOutfield(games_list,player_list,stat,team_folder,season):
    """merging stats across the season (stats per game per player)"""

    # create a base dataframe of all players
    join_df = pd.DataFrame(player_list, columns=['SPIELER'])

    header = ['TORE', '7M', '%', 'TF', 'V', "2'", 'D']
    header.remove(stat)

    # merge stats to the base dataframe using the date as column name
    for file in games_list:
        temp_df = pd.read_csv(f'{data_dir}/{team_folder}/{season}/{file}', encoding='utf-8').fillna(0)
        merged = pd.merge(join_df, temp_df, left_on='SPIELER', right_on='SPIELER', how='outer')#.fillna(-1)
        merged = merged.drop(header, axis=1)
        merged.rename(columns={stat : str(file[:8])}, inplace=True)
        join_df = merged

    # sort columns: first is SPIELER, then sort according to date
    join_df = join_df.reindex(sorted(join_df.columns), axis=1)
    col = join_df.pop("SPIELER")
    join_df.insert(0, col.name, col)
    return join_df

def mergeStatsGoalie(games_list,player_list,stat,team_folder,season):
    """merging stats across the season (stats per game per player)"""

    # create a base dataframe of all players
    join_df = pd.DataFrame(player_list, columns=['TORHÜTER'])

    header = ['P/W','7M','%']
    header.remove(stat)

    # merge stats to the base dataframe using the date as column name
    for file in games_list:
        temp_df = pd.read_csv(f'{data_dir}/{team_folder}/{season}/{file}', encoding='utf-8').fillna(0)
        merged = pd.merge(join_df, temp_df, left_on='TORHÜTER', right_on='TORHÜTER', how='outer')#.fillna(-1)
        merged = merged.drop(header, axis=1)
        merged.rename(columns={stat : str(file[:8])}, inplace=True)
        join_df = merged

    # sort columns: first is SPIELER, then sort according to date
    join_df = join_df.reindex(sorted(join_df.columns), axis=1)
    col = join_df.pop("TORHÜTER")
    join_df.insert(0, col.name, col)

    return join_df

def plotOutfield(input_dataframe,stat,team_folder,season):
    """plots multivariate time series and saves .pngs of them"""
    print(f'plotting stat {stat} for team {team_folder}, {season}')


    fontP = FontProperties()
    fontP.set_size('small')

    plt.figure(figsize=(15, 7))
    input_dataframe = input_dataframe.sort_values(by = 'SPIELER')
    output = parallel_coordinates(input_dataframe,'SPIELER', colormap='viridis',zorder=1000)
    plt.title(f'outfield player, statistic [{stat}], of team {team_folder}, {season}')
    plt.legend(title='Player Name', bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)
    plt.xticks(rotation=90)
    plt.tight_layout()

    if stat == '%':
        #save all players scoring % at higher dpi for better zoomability
        plt.savefig(f'output_png/progress_plots/{team_folder}/{season}/{stat}', dpi=300)
    else:
        plt.savefig(f'output_png/progress_plots/{team_folder}/{season}/{stat}')

    plt.close()

def plotOutfieldIndividuals(player_list, input_dataframe, stat, team_folder, season):
    """plots individual entries of multivariate time series and saves .pngs of them"""

    for player in player_list:
        print(f'plotting stat {stat} for player {player}, {season}')

        #set up directory for player
        try:
            os.makedirs(f'output_png/progress_plots/{team_folder}/{season}/{player}', exist_ok=False)
        except FileExistsError:
            pass

        #plotting stuff
        fontP = FontProperties()
        fontP.set_size('small')

        plt.figure(figsize=(10, 7))

        output = parallel_coordinates(input_dataframe.loc[input_dataframe['SPIELER'] == player], 'SPIELER', colormap='viridis_r', zorder=1000)

        plt.title(f'outfield player, statistic [{stat}] of team {team_folder}, {season}')
        plt.legend(title='Player Name', bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)
        plt.xticks(rotation=90)
        plt.tight_layout()

        plt.savefig(f'output_png/progress_plots/{team_folder}/{season}/{player}/{stat}')
        plt.close()

def plotGoalie(input_dataframe,stat,team_folder,season):
    """plots multivariate time series and saves .pngs of them"""
    print(f'plotting stat {stat} for goalies of team {team_folder}, {season}')

    fontP = FontProperties()
    fontP.set_size('small')

    plt.figure(figsize=(10, 5))
    input_dataframe = input_dataframe.sort_values(by='TORHÜTER')
    output = parallel_coordinates(input_dataframe, 'TORHÜTER', colormap='viridis', zorder=1000)
    plt.title(f'goalie save{stat} of team {team_folder}, {season}')
    plt.legend(title='Player Name', bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.savefig(f'output_png/progress_plots/{team_folder}/{season}/{stat}_goalies')
    print('saving goalie stats...')
    plt.close()

def plotGoalieIndividuals(player_list, input_dataframe, stat, team_folder, season):
    """plots individual entries of multivariate time series and saves .pngs of them"""

    for player in player_list:
        print(f'plotting stat {stat} for goalie {player}, {season}')

        # set up directory for player
        try:
            os.makedirs(f'output_png/progress_plots/{team_folder}/{season}/{player}', exist_ok=False)
        except FileExistsError:
            pass

        # plotting stuff
        fontP = FontProperties()
        fontP.set_size('small')

        plt.figure(figsize=(10, 7))

        output = parallel_coordinates(input_dataframe.loc[input_dataframe['TORHÜTER'] == player], 'TORHÜTER', colormap='viridis_r', zorder=1000)

        plt.title(f'goalie save{stat} of team {team_folder}, {season}')
        plt.legend(title='Player Name', bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)
        plt.xticks(rotation=90)
        plt.tight_layout()

        plt.savefig(f'output_png/progress_plots/{team_folder}/{season}/{player}/{stat}_goalie')
        plt.close()

def write(input_dataframe,team_folder,season,stat):
    input_dataframe.to_csv(f'output_csv/progress_data/{team_folder}/{season}/{stat}', index=False)

def get_team(val):
    """returns the key to a value in a dictionary within the options.py dictionary"""
    for entry in teams_seasons.items():
        for season, number in entry[1].items():
            for element in number:
                if val == element:
                    return entry[0]
    return "team not found"

def get_season(val):
    """returns the season of a value in a dictionary within the options.py dictionary"""
    for entry in teams_seasons.items():
        for season, number in entry[1].items():
            for element in number:
                if val == element:
                    return season
    return "season not found"


if __name__ == '__main__':
    main()
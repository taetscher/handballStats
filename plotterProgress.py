import os
import pandas as pd
import matplotlib.pyplot as plt

data_dir = 'playerProgress_data'

def main():
    folders = os.listdir(data_dir)

    for folder in folders:
        print(f'analyzing team number {folder}')
        #get all files in folder
        files = []
        files.extend(os.listdir('{}/{}/raw_data'.format(data_dir, folder)))

        #convert csv files to account for player info and goalie info
        for file in files:
            print('converting file {}...'.format(file))
            csvConverter(file,folder)

        #read in newly generated, split csvs
        inputs = []
        outfield = []
        goalies = []

        inputs.extend(os.listdir('{}/{}'.format(data_dir,folder)))

        #create list of files for outfield/goalie players
        for file in inputs:
            if str(file).split('_')[-1] == 'outfield.csv':
                outfield.append(file)
            elif str(file).split('_')[-1] == 'goalies.csv':
                goalies.append(file)
            else:
                pass

        #do pandas calculations/joins to be able to have each game as a column, each player as a row
        #create empty dataframe to which to join all of the information of each file

        #first, generate a list of all players who have played over the course of the whole season
        outfield_players = []
        for file in outfield:
            temp_df = pd.read_csv('{}/{}/{}'.format(data_dir, folder, file), encoding='utf-8').fillna(0)
            for player in temp_df['SPIELER']:
                outfield_players.append(player)
        outfield_players = set(outfield_players)

        stats = ['%', 'TF', 'V', "2'", 'D']

        for stat in stats:
            merged = mergeStats(outfield,outfield_players,stat,folder)

            #plot time series data of each player to see his/her progress over time
            plot(merged)

def csvConverter(infile,folder):
    """ takes in messy raw data and turns it into readable csv format

    writes one output file for outfield players and one file for goalies"""
    game_number = infile[4:-4]

    data = []
    with open('{}/{}/raw_data/{}'.format(data_dir,folder,infile), 'rb') as infile:

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

    player_data = data[4:goalie_index-2]
    goalie_data = data[goalie_index:staff_index-2]
    header_goalies = cleanUp(data[goalie_index-1]).replace(' ',',')


    #write the cleaned data into two seperate files
    #outfield players
    with open('playerProgress_data/{}/{}_game{}_outfield.csv'.format(folder,date,game_number),'w',encoding='utf-8') as outfile:
        outfile.write(header_players +'\n')
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

            element = str(player_name) + ',' + str(player_stats).strip('[').strip(']').replace("'",'').replace(' ','')
            outfile.write(element +'\n')
        outfile.close()

    #goalies
    with open('playerProgress_data/{}/{}_game{}_goalies.csv'.format(folder,date,game_number),'w',encoding='utf-8') as outfile:
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

            element = str(goalie_name) + ',' + str(goalie_stats).strip('[').strip(']').replace("'", '').replace(' ', '')
            outfile.write(element + '\n')
        outfile.close()

def cleanUp(inlist):
    return str(inlist).strip("['").strip("']").replace(',',' ')

def pdToInt(dframe,inlist):
    for column in inlist:
        pd.eval(dframe[column],parser='python')

def mergeStats(games_list,player_list,stat,folder):
    # create a base dataframe of all players
    join_df = pd.DataFrame(player_list, columns=['SPIELER'])

    header = ['TORE', '7M', '%', 'TF', 'V', "2'", 'D']
    header.remove(stat)

    # merge stats to the base dataframe using the date as column name
    for file in games_list:
        temp_df = pd.read_csv('{}/{}/{}'.format(data_dir, folder, file), encoding='utf-8').fillna(0)
        merged = pd.merge(join_df, temp_df, left_on='SPIELER', right_on='SPIELER', how='outer')#.fillna(-1)
        merged = merged.drop(header, axis=1)
        merged.rename(columns={stat : str(file[:8])}, inplace=True)
        join_df = merged

    # sort columns: first is SPIELER, then sort according to date
    join_df = join_df.reindex(sorted(join_df.columns), axis=1)
    col = join_df.pop("SPIELER")
    join_df.insert(0, col.name, col)

    return join_df

def plot(input_dataframe):

    input_dataframe.plot()




if __name__ == '__main__':
    main()
import os

data_dir = 'playerProgress_data'

def main():
    folders = os.listdir(data_dir)

    for folder in folders:
        #get all files in folder
        files = []
        files.extend(os.listdir('{}/{}'.format(data_dir, folder)))

        #convert to readable csv
        for file in files:
            print('\nreading file {}...\n'.format(file))
            csvConverter(file,folder)

        #do pandas calculations/joins to be able to have each game as a column, each player as a row

        #plot time series data of each player to see his/her progress over time

def csvConverter(infile,folder):
    """ takes in messy raw data and turns it into readable csv format

    writes one output file for outfield players and one file for goalies"""

    with open('{}/{}/{}'.format(data_dir,folder,infile), 'r') as infile:
        lines = infile.readlines()
        date = lines[0].split(' ')[1]
        header = lines[2]

        print(lines)
        print(date,header)

if __name__ == '__main__':
    main()
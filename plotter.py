import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.groupby.groupby import DataError
import os

def plot():
    indir = os.listdir('scraped_data')

    for file in indir:
        infile = file[:-4]
        group = infile.split('_')[1:]
        s = '_'
        group = s.join(group)
        print('\n\n\n')
        print('reading in... ' + infile
              )

        df = pd.read_csv('scraped_data/' + infile + '.csv')
        # df = df.drop(['yellowCards','2mins','redCards'], axis=1 )

        try:
            goalsPerGame = df.groupby(['team'])['goalsPerGame'].mean().sort_values(ascending=False)
            suspensions = df.groupby(['team'])['2mins'].mean().sort_values(ascending=False)
            yellows = df.groupby(['team'])['yellowCards'].mean().sort_values(ascending=False)
            reds = df.groupby(['team'])['redCards'].sum().sort_values(ascending=False)

            # print(goalsPerGame.head(10))
            print(suspensions.head(20))
            print(yellows.head(20))
            print(reds.head(20))

            goalsPerGame.plot(x='teams', y='goalsPerGame', kind='bar')
            plt.title('Mean amount of Goals per Player per Team per Game\n{}'.format(group))
            plt.tight_layout()
            plt.savefig('output_png/{}_meanGoalsPerPlayerPerTeamPerGame.png'.format(group))
            plt.close('all')

            suspensions.plot(x='teams', y='2mins', kind='bar')
            plt.title('Mean amount of Suspensions per Player per Team\n{}'.format(group))
            plt.tight_layout()
            plt.savefig('output_png/{}_meanSuspensionsPerPlayerPerTeam.png'.format(group))
            plt.close('all')

            yellows.plot(x='teams', y='yellowCards', kind='bar')
            plt.title('Mean amount of Yellow Cards per Player per Team\n{}'.format(group))
            plt.tight_layout()
            plt.savefig('output_png/{}_meanYellowCardsPerPlayerPerTeam.png'.format(group))
            plt.close('all')

            reds.plot(x='teams', y='redCards', kind='bar')
            plt.title('Sum of Red Cards per Team\n{}'.format(group))
            plt.tight_layout()
            plt.savefig('output_png/{}_redCardsPerTeam.png'.format(group))
            plt.close('all')

        except DataError as e:
            print('ERROR: {}'.format(e))
            print('The season you are looking at probably does not have player stats (yet/anymore)')
            print('Looked specifically at group {}'.format(group))
            print('\n\n\n')
            continue

if __name__ == '__main__':
    plot()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('scraped_data.csv')
#df = df.drop(['yellowCards','redCards'], axis=1 )


goalsPerGame = df.groupby(['team'])['goalsPerGame'].aggregate(np.mean).sort_values(ascending=False)
suspensions = df.groupby(['team'])['2mins'].mean().sort_values(ascending=False)
yellows = df.groupby(['team'])['yellowCards'].mean().sort_values(ascending=False)
reds = df.groupby(['team'])['redCards'].sum().sort_values(ascending=False)

#print(goalsPerGame.head(10))
print(suspensions.head(20))
print(yellows.head(20))
print(reds.head(20))

#TODO: avoid overlap of all these plots
goalsPerGame.plot(x='teams',y='goalsPerGame',kind='bar')
plt.title('Mean amount of Goals per Player per Team per Game')
plt.tight_layout()
plt.savefig('output_png/meanGoalsPerPlayerPerTeamPerGame.png')
plt.close('all')

suspensions.plot(x='teams',y='2mins',kind='bar')
plt.title('Mean amount of Suspensions per Player per Team')
plt.tight_layout()
plt.savefig('output_png/meanSuspensionsPerPlayerPerTeam.png')
plt.close('all')

yellows.plot(x='teams',y='yellowCards',kind='bar')
plt.title('Mean amount of Yellow Cards per Player per Team')
plt.tight_layout()
plt.savefig('output_png/meanYellowCardsPerPlayerPerTeam.png')
plt.close('all')

reds.plot(x='teams',y='redCards',kind='bar')
plt.title('Sum of Red Cards per Team')
plt.tight_layout()
plt.savefig('output_png/redCardsPerTeam.png')
plt.close('all')
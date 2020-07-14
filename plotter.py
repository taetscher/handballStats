import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('scraped_data.csv')
df = df.drop(['yellowCards','2mins','redCards'], axis=1 )

grouped = df.groupby(['team'])['goalsPerGame'].mean().sort_values(ascending=False)

print(grouped.head(20))


fig = plt.figure()
ax = fig.add_subplot(111)
plot = grouped.plot(x='team',y='goalsPerGame',kind='bar')
plt.title('Mean amount of Goals per Player per Team per Game')
plt.tight_layout()

#plt.show()
plt.savefig('meanGoalsPerPlayerPerTeamPerGame.png')
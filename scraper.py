from lib.plotterPlayerProgress import plotPlayerProgress
from lib.plotterPlayerStats import plotPlayerStats
from lib.scraperPlayerProgress import scrapePlayerProgress
from lib.scraperPlayerStats import scrapePlayerStats
from lib.scraperGameProgression import scrapeGameProgression
from lib.plotterGameProgression import plotGameProgressions
from datetime import datetime


start = datetime.now()

#--------------------------------
#unfinished stuff

#print("\n", "-"*30, "\n", "Scraping Player Stats", "\n", "-"*30, "\n")
#scrapePlayerStats()

#print("\n", "-"*30, "\n", "Plotting Player Stats", "\n", "-"*30, "\n")
#plotPlayerStats()
#--------------------------------

print("\n", "-"*30, "\n", "Scraping Player Progress", "\n", "-"*30, "\n")
scrapePlayerProgress()

print("\n", "-"*30, "\n", "Plotting Player Progress", "\n", "-"*30, "\n")
plotPlayerProgress()

print("\n", "-"*30, "\n", "Scraping Game Progression", "\n", "-"*30, "\n")
scrapeGameProgression()

print("\n", "-"*30, "\n", "Plotting Game Progression", "\n", "-"*30, "\n")
plotGameProgressions()

end = datetime.now()
print(f'done. elapsed time: {end-start}')
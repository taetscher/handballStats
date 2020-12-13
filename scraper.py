from lib.plotterPlayerProgress import *
from lib.plotterPlayerStats import *
from lib.scraperPlayerProgress import *
from lib.scraperPlayerStats import *
from lib.scraperGameProgression import *
from lib.plotterGameProgression import *

print("\n", "-"*30, "\n", "Scraping Player Stats", "\n", "-"*30, "\n")
scrapePlayerStats()

print("\n", "-"*30, "\n", "Plotting Player Stats", "\n", "-"*30, "\n")
plotPlayerStats()

print("\n", "-"*30, "\n", "Scraping Player Progress", "\n", "-"*30, "\n")
scrapePlayerProgress()

print("\n", "-"*30, "\n", "Plotting Player Progress", "\n", "-"*30, "\n")
plotPlayerProgress()

print("\n", "-"*30, "\n", "Scraping Game Progression", "\n", "-"*30, "\n")
scrapeGameProgression()

print("\n", "-"*30, "\n", "Plotting Game Progression", "\n", "-"*30, "\n")
#plot spielverlauf
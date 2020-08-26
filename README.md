# handballStats
This repository was created for me to learn about web scraping and git/github flow.
If you have any comments, ideas for improvement, let me know!

This repository allows you to scrape data from <a href="https://www.handball.ch/de/matchcenter/" target="blank">handball.ch</a>.
scraperPlayerStats.py scrapes overall (league-wide) player statistics of pre-defined groups (corresponding to leagues/years). plotterPlayerStats plots and analyzes some of that data (rudimentary statistics only currently). You can find these analyses within the folder output_png.

scraperPlayerProgress scrapes statistics of each individual game (liveticker-stats). plotterPlayerProgress plots (per stat available) a multivariate time series of each team as well as time series data (progression over the season) of each player of each team. These plots can be found in the corresponding team folder under output_png/progress_plots/{team_name}/{season}.

At this point, only the performance-oriented teams of <a href="https://wackerthun.ch/de/" target="blank">Wacker Thun</a> are analyzed, however through adjustment of options.py, any team playing under the <a href="https://www.handball.ch/de/matchcenter/" target="blank">Swiss Handball Federation</a> may be analyzed.


![Example Statistic](https://github.com/taetscher/handballStats/blob/master/output_png/progress_plots/Wacker%20Thun%20NLA/Saison%2019_20/%25_goalies.png "Example of Multivariate Time Series Plot")
![Example Statistic](https://github.com/taetscher/handballStats/blob/master/output_png/U15_Elite_201920_meanGoalsPerPlayerPerTeamPerGame.png "Example Statistic")



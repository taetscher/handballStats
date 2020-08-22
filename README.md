# handballStats
This repository was created for me to learn about web scraping and git/github flow.
If you have any comments, ideas for improvement, let me know!

This repository allows you to scrape data from <a href="https://www.handball.ch/de/matchcenter/" target="blank">handball.ch</a>.
It gets overall player statistics of pre-defined groups (corresponding to leagues/years).
Furthermore, the program gets statistics of each individual game (liveticker-stats) and plots (per stat available) multivariate time series of each team as well as time series data (progression over the season) of each player of each team.

At this point, only the performance-oriented teams of <a href="https://wackerthun.ch/de/" target="blank">Wacker Thun</a> are analyzed, however through adjustment of options.py, any team playing under the <a href="https://www.handball.ch/de/matchcenter/" target="blank">Swiss Handball Federation</a> may be analyzed.

Then, it currently calculates rudimentary statistics from that.
Like how many goals were scored per player per team per game on average.
I would like to expand on this in the future.

### Use the options.py file to navigate the output_png directory more swiftly!
In there you can see what number corresponds to which team - as the Swiss Handball Federation assigns each team a unique number per season.

![Example Statistic](https://github.com/taetscher/handballStats/blob/master/output_png/progress_plots/30644/%25_goalies.png "Example Statistic")
![Example Statistic](https://github.com/taetscher/handballStats/blob/master/output_png/U15_Elite_201920_meanGoalsPerPlayerPerTeamPerGame.png "Example Statistic")



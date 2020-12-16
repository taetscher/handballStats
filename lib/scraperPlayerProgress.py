from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import unicodecsv as csv
import options

#loading in the options file
teams_seasons = options.teams_seasons
teams = []

def scrapePlayerProgress():

    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(
        #on pc
        executable_path=r'C:\Users\Benjamin Schüpbach\Desktop\Coding\geckodriver-v0.27.0-win64\geckodriver.exe')

        #on mac
        #executable_path = r'/Users/benischuepbach/Desktop/Coding/sources/geckodriver')

    #get team ids from options.py
    for season in teams_seasons.values():
        for id in season.values():
            teams.extend(id)

    # check if output directory already exists, create new one if not
    for team in teams:
        try:
            print(f'creating new directories for team {get_team(team)} and season {get_season(team)}...')
            os.makedirs(f"playerProgress_data/{get_team(team)}/{get_season(team)}/raw_data", exist_ok=False)
            os.makedirs(f'output_png/progress_plots/{get_team(team)}/{get_season(team)}',exist_ok=False)
            os.makedirs(f'output_csv/progress_data/{get_team(team)}/{get_season(team)}', exist_ok=False)
        except OSError:
            print(f'directories for team {get_team(team)} and season {get_season(team)} already exist, skipping...\n')

    for team in teams:
        season = get_season(team)
        year_start = season.split(' ')[1].split('_')[0]
        year_finish = season.split(' ')[1].split('_')[1]

        team_name, games = findGamesPage(driver, team,year_start,year_finish)

        for game in games:
            time.sleep(0.5)
            link = 'https://www.handball.ch/de/matchcenter/spiele/{}'.format(game)
            time.sleep(0.5)
            try:
                game_stats, date, league = scrapeGame(link, team_name, driver)
                writer(game_stats, game, date, team, league)
                print(date, team, league)
            except TypeError:
                print(f'error. most likely the game ({game}) you are trying to download does not have stats available\nskipping...')

    print('\n', '-'*10)
    print('scraping successfully terminated, closing firefox...')
    driver.quit()

def findGamesPage(driver,team,year_start,year_finish):
    """finds all games played by specified team

    returns a list of game ids"""

    # specify url
    urlpage = 'https://www.handball.ch/de/matchcenter/teams/{}#/games'.format(team)
    print('\n\nscraping... ', urlpage)

    driver.get(urlpage)
    time.sleep(1)

    team_name = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div/div[2]/div/div[2]/h1').text
    print(f'\nscraping games of team: {team_name}, season {year_start}/{year_finish}')

    games_button = driver.find_element_by_xpath('//*[@id="games-tab"]')
    games_button.click()

    time.sleep(1)
    first_date = driver.find_element_by_xpath('//*[@id="dateFromGames_1"]')
    first_date.send_keys(Keys.CONTROL + "a")
    first_date.send_keys('01.07.20'+year_start)

    second_date = driver.find_element_by_xpath('//*[@id="dateToGames_1"]')
    second_date.send_keys(Keys.CONTROL + "a")
    second_date.send_keys('01.05.20'+year_finish)

    click_away = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div[2]/div/div/div[2]/div/div[1]/h2')
    click_away.click()

    games = getAllGames(driver)
    return team_name, games

def getAllGames(driver):
    """helper function, retrieves and cleans up a list of all games played by specified team"""
    games = []
    time.sleep(1)
    table_rows = driver.find_elements_by_tag_name('tr')
    for row in table_rows:
        games.append(row.get_attribute('id'))

    while ("" in games):
        games.remove("")

    return games

def scrapeGame(link,team,driver):
    """helper function. retrieves game statistics of input game-id

    returns only statistics for specified team and input game"""

    driver.get(link)
    time.sleep(1)
    stats_tab = driver.find_element_by_xpath('//*[@id="stats-tab"]')
    stats_tab.click()
    time.sleep(1)
    date = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/span[1]').text
    left_table = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[1]/div/table')
    right_table = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[2]')

    left_content = left_table.get_attribute('innerText')
    left_team = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[1]/div/table/thead[1]/tr/td/span').text
    time.sleep(3)

    right_content = right_table.get_attribute('innerText')
    right_team = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[2]/div/table/thead[1]/tr/td/span').text
    time.sleep(3)

    league = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div/div/div[6]/p').text
    try:
        league = league.split('-')[1]
    except IndexError:
        pass

    #get only stats for specified team
    if left_team.upper() == team:
        return left_content, date, league
    elif right_team.upper() == team:
        return right_content, date, league
    else:
        print('\n\nsomething went wrong, skipping or shutting down...')
        pass

def writer(game_stats,game,date,team, league):
    """helper function. writes statistics of input game-id into csv file"""

    with open(f'playerProgress_data/{get_team(team)}/{get_season(team)}/raw_data/raw_{game}.csv','wb') as outfile:
        #write in bytes mode ('wb') to avoid characters being saved wrongly
        print(f'\nwriting stats for game {game}...')
        writeR = csv.writer(outfile)
        date = date.split(' ')
        league = league.split(' ')[1:]
        writeR.writerow(date)
        writeR.writerow(league)

        cSv = game_stats.split('\n')

        for element in cSv:
            # remove whitespace at beginning of strings
            try:
                element = element.strip().replace('\t',' ')
            except:
                pass

            element = element.split(' ')
            writeR.writerow(element)

        outfile.close()

def get_team(val):
    """returns the key to a value in a dictionary within the options.py dictionary"""
    for entry in teams_seasons.items():
        for season, number in entry[1].items():
            for element in number:
                if val == element:
                    return entry[0]
    return "season not found"

def get_season(val):
    """returns the season of a value in a dictionary within the options.py dictionary"""
    for entry in teams_seasons.items():
        for season, number in entry[1].items():
            for element in number:
                if val == element:
                    return season
    return "season not found"


if __name__ == '__main__':
    scrapePlayerProgress()

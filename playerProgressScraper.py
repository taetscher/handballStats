from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import unicodecsv as csv
import options


#be aware, the team id changes once per season!
teams_seasons = options.teams_seasons
teams = []

def main():

    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(
        #on pc
        #executable_path=r'C:\Users\Benjamin Schüpbach\Desktop\Coding\geckodriver-v0.27.0-win64\geckodriver.exe')

        #on mac
        executable_path = r'/Users/benischuepbach/Desktop/Coding/sources/geckodriver')

    for value in teams_seasons.values():
        teams.extend(value)

    # check if output directory already exists, create new one if not
    for team in teams:
        try:
            print(f'creating new directories for team {team}...')
            os.makedirs(f"playerProgress_data/{team}/raw_data", exist_ok=False)
            os.makedirs(f'output_png/progress_plots/{team}',exist_ok=False)
            os.makedirs(f'output_csv/progress_data/{team}', exist_ok=False)
        except OSError:
            print('directories for team {} already exist, skipping...'.format(team))

    for team in teams:
        team_name, games = findGamesPage(driver, team)

        for game in games:
            link = 'https://www.handball.ch/de/matchcenter/spiele/{}'.format(game)
            game_stats, date, league = scrapeGame(link, team_name, driver)
            writer(game_stats, game, date, team, league)
            print(date, team, league, game_stats)

    print('scraping successfully terminated, closing firefox...')
    driver.quit()

def findGamesPage(driver,team):
    """finds all games played by specified team

    returns a list of game ids"""

    # specify url
    urlpage = 'https://www.handball.ch/de/matchcenter/teams/{}'.format(team)
    print('scraping... ', urlpage)

    driver.get(urlpage)
    time.sleep(2)

    team_name = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div/div[2]/div/div[2]/h1').text
    print('scraping games of team: {}'.format(team_name))

    games_button = driver.find_element_by_xpath('//*[@id="games-tab"]')
    games_button.click()

    time.sleep(0.5)
    first_date = driver.find_element_by_xpath('//*[@id="dateFromGames_1"]')
    first_date.send_keys(Keys.CONTROL + "a")
    first_date.send_keys('01.07.2019')

    second_date = driver.find_element_by_xpath('//*[@id="dateToGames_1"]')
    second_date.send_keys(Keys.CONTROL + "a")
    second_date.send_keys('01.05.2020')

    click_away = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div[2]/div/div/div[2]/div/div[1]/h2')
    click_away.click()

    games = getAllGames(driver)
    return team_name, games

def getAllGames(driver):
    """helper function, retrieves and cleans up a list of all games played by specified team"""
    games = []
    time.sleep(2)
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
    time.sleep(0.5)
    stats_tab = driver.find_element_by_xpath('//*[@id="stats-tab"]')
    stats_tab.click()
    time.sleep(2)
    date = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/span[1]').text
    left_table = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[1]/div/table')
    right_table = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[2]')

    left_content = left_table.get_attribute('innerText')
    left_team = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[1]/div/table/thead[1]/tr/td/span').text
    time.sleep(0.5)

    right_content = right_table.get_attribute('innerText')
    right_team = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[2]/div/table/thead[1]/tr/td/span').text
    time.sleep(0.5)

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
        print('\n\nsomething went wrong, shutting down...')
        pass

def writer(game_stats,game,date,team, league):
    """helper function. writes statistics of input game-id into csv file"""

    with open('playerProgress_data/{}/raw_data/raw_{}.csv'.format(team,game),'wb') as outfile:
        #write in bytes mode ('wb') to avoid characters being saved wrongly
        print('\n\nwriting stats for game {}...'.format(game))
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

if __name__ == '__main__':
    main()

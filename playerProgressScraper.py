from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

#be aware, the team id changes once per season!
teams = {'U15Elite':['30639'],'U17Elite':['30635'],'U19Elite':['30371']}

def main():

    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(
        executable_path=r'C:\Users\Benjamin Schüpbach\Desktop\Coding\geckodriver-v0.27.0-win64\geckodriver.exe')

    #TODO: Find some way of being able to assign each output folder(or file) a season tag to generate stats for multiple seasons

    # check if output directory already exists, create new one if not
    for team in teams:
        try:
            print('creating new directory for team {}...'.format(team))
            os.makedirs("playerProgress_data/{}".format(team), exist_ok=False)
        except OSError:
            print('directory for team {} already exists, skipping...'.format(team))

    for team in teams:
        team_name, games = findGamesPage(driver, team)

        for game in games:
            link = 'https://www.handball.ch/de/matchcenter/spiele/{}'.format(game)
            game_stats, date = scrapeGame(link, team_name, driver)
            # TODO: save date of game as well as number and all the other stuff!
            writer(game_stats, game, date, team)
            print(game_stats)

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

    left_content = left_table.text
    left_team = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[1]/div/table/thead[1]/tr/td/span').text
    time.sleep(0.5)

    right_content = right_table.text
    right_team = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[2]/div/table/thead[1]/tr/td/span').text
    time.sleep(0.5)

    if left_team.upper() == team:
        return left_content, date
    elif right_team.upper() == team:
        return right_content, date
    else:
        print('\n\nsomething went wrong, shutting down...')
        pass

def writer(game_stats,game,date,team):
    """helper function. writes statistics of input game-id into csv file"""

    with open('playerProgress_data/{}/{}.csv'.format(team,game),'w') as outfile:
        #encode/decode to avoid characters being saved wrongly
        outfile.write(date+'\n')
        csv = game_stats.replace(' ', ',').encode().decode('cp1252')
        outfile.write(csv)
        outfile.close()

if __name__ == '__main__':
    main()

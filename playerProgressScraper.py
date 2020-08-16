from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def scrape():
    findGamesPage()

def findGamesPage():
    # specify url
    urlpage = 'https://www.handball.ch/de/matchcenter/teams/30639'
    print('scraping... ', urlpage)

    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(
        executable_path=r'C:\Users\Benjamin Schüpbach\Desktop\Coding\geckodriver-v0.27.0-win64\geckodriver.exe')

    driver.get(urlpage)

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

    for game in games:
        link = 'https://www.handball.ch/de/matchcenter/spiele/{}'.format(game)
        scrapeGame(link,driver)

    driver.quit()


def getAllGames(driver):
    games = []
    time.sleep(1)
    table_rows = driver.find_elements_by_tag_name('tr')
    for row in table_rows:
        games.append(row.get_attribute('id'))

    while ("" in games):
        games.remove("")

    return games

def scrapeGame(link,driver):
    driver.get(link)
    stats_tab = driver.find_element_by_xpath('//*[@id="stats-tab"]')
    stats_tab.click()
    time.sleep(1)
    left_table = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[1]/div/table')
    right_table = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[3]/div[2]')
    print(left_table.text)
    print(right_table)

if __name__ == '__main__':
    scrape()

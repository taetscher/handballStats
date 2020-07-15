from selenium import webdriver
import time

#set groups (2019/2020, groups were 12135 (u19), 12136 (u17), 12137 (u15)
seasons = {'LakeSide_Elite_1920':[12135,12136,12137],'LakeSide_Elite_2021':[12954,12955,12956],'TVS_3_1920':[12147]}
groups = []

def scrape():
    for value in seasons.values():
        groups.extend(value)

    print('scraping from groups...', groups)

    for group in groups:
        # specify url
        urlpage = 'https://www.handball.ch/de/matchcenter/gruppen/{}#/stats'.format(group)
        print('scraping... ', urlpage)

        # run firefox webdriver from executable path of your choice
        driver = webdriver.Firefox(executable_path='/Users/benischuepbach/Desktop/Coding/sources/geckodriver')

        driver.get(urlpage)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(5)

        results = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[2]/table')
        group = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div/div[2]/p').text.replace(' ', '_')
        season = driver.find_element_by_xpath('//*[@id="menu-breadcrumb-season-trigger"]/span').text.replace('/', '')

        teams = []

        data = results.text.replace('\n', '\n').replace(' ', ',')

        with open('scraped_data/{}_{}.csv'.format(group, season), 'w') as outfile:
            outfile.write('playerName,team,games,goalsPerGame,yellowCards,2mins,redCards\n')
            outfile.close()

        for n in range(1, len(data.split('\n'))):
            player_name = driver.find_element_by_xpath(
                '//*[@id="stats"]/div[2]/div[2]/table/tbody/tr[{}]/td[2]'.format(n))
            player_team = driver.find_element_by_xpath(
                '//*[@id="stats"]/div[2]/div[2]/table/tbody/tr[{}]/td[3]'.format(n))
            player_games = driver.find_element_by_xpath(
                '//*[@id="stats"]/div[2]/div[2]/table/tbody/tr[{}]/td[6]'.format(n))
            player_gpg = driver.find_element_by_xpath(
                '//*[@id="stats"]/div[2]/div[2]/table/tbody/tr[{}]/td[7]'.format(n))
            player_yellow = driver.find_element_by_xpath(
                '//*[@id="stats"]/div[2]/div[2]/table/tbody/tr[{}]/td[8]'.format(n))
            player_2min = driver.find_element_by_xpath(
                '//*[@id="stats"]/div[2]/div[2]/table/tbody/tr[{}]/td[9]'.format(n))
            player_red = driver.find_element_by_xpath(
                '//*[@id="stats"]/div[2]/div[2]/table/tbody/tr[{}]/td[10]'.format(n))

            teams.append(player_team.text)

            with open('scraped_data/{}_{}.csv'.format(group, season), 'ab') as outfile:
                outfile.write(player_name.text.encode('utf-8'))
                outfile.write(str.encode(',', 'utf-8'))
                outfile.write(player_team.text.encode('utf-8'))
                outfile.write(str.encode(',', 'utf-8'))
                outfile.write(player_games.text.encode('utf-8'))
                outfile.write(str.encode(',', 'utf-8'))
                outfile.write(player_gpg.text.encode('utf-8'))
                outfile.write(str.encode(',', 'utf-8'))
                outfile.write(player_yellow.text.encode('utf-8'))
                outfile.write(str.encode(',', 'utf-8'))
                outfile.write(player_2min.text.encode('utf-8'))
                outfile.write(str.encode(',', 'utf-8'))
                outfile.write(player_red.text.encode('utf-8'))
                outfile.write(str.encode('\n', 'utf-8'))
                outfile.close()

        driver.quit()
    driver.quit()

if __name__ == '__main__':
    scrape()

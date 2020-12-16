from lib.scraperPlayerProgress import *

#loading in the options file
teams_seasons = options.teams_seasons
teams = []

def scrapeGameProgression():
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
            os.makedirs(f'././output_csv/gameProgressions/{get_team(team)}/{get_season(team)}', exist_ok=False)
            os.makedirs(f'././output_png/gameProgressions/{get_team(team)}/{get_season(team)}', exist_ok=False)

        except OSError:
            print(f'directories for team {get_team(team)} and season {get_season(team)} already exist, skipping...\n')

    for team in teams:
        season = get_season(team)
        year_start = season.split(' ')[1].split('_')[0]
        year_finish = season.split(' ')[1].split('_')[1]

        team_name, games = findGamesPage(driver, team,year_start,year_finish)

        for game in games:
            time.sleep(0.1)
            link = 'https://www.handball.ch/de/matchcenter/spiele/{}'.format(game)
            print(link)
            time.sleep(0.1)
            try:
                try:
                    progression, date = getGameProgression(link, driver)
                    writeProgression(progression, team, season, date)
                except IndexError:
                    #TODO: fix issue where index is out of range for home or away team
                    print("IndexError occured, skipping...")

            except:
                print(f'error. most likely the game ({game}) you are trying to download does not have stats available\nskipping...')

    print('\n', '-'*10)
    print('scraping successfully terminated, closing firefox...')
    driver.quit()


def getGameProgression(link, driver):
    driver.get(link)
    time.sleep(0.5)
    tab = driver.find_element_by_xpath('//*[@id="live-tab"]')
    tab.click()
    time.sleep(1.5)
    table = driver.find_element_by_xpath('//*[@id="live"]/div[2]/div[3]')
    table_content = table.get_attribute('innerText')
    date = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/span[1]').get_attribute('innerText')
    date = date.split(' ')[1][:-6]
    date = date.split('.')
    date = "_".join(reversed(date))

    return table_content, date


def writeProgression(progression, team, season, date):

    entries = progression.split('\n')
    team_home = entries[0]
    team_away = entries[1]
    course = entries[2:]
    rows = list(divide_chunks(course,4))
    time_score = []

    for row in rows:
        for entry in row:
            if ':' in entry:
                time_score.append(entry)

    time_score = list(divide_chunks(time_score, 2))

    try:
        with open(f'././output_csv/gameProgressions/{get_team(team)}/{season}/{date}_{team_home.replace(".", "")}_{team_away.replace(".", "")}.csv',
                  'wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['timestamp', 'score'])
            for row in time_score:
                writer.writerow(row)
            outfile.close()

    except OSError:
        #handle games that werent played (yet)
        pass


def divide_chunks(l, n):
    """takes a list and segments it into evenly sized chunks of length n"""

    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__ == "__main__":
    scrapeGameProgression()
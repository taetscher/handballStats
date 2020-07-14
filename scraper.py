from selenium import webdriver
import time


# specify url
urlpage = 'https://www.handball.ch/de/matchcenter/gruppen/12137#/stats'
print('scraping... ', urlpage)

# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox(executable_path = '/Users/benischuepbach/Desktop/Coding/sources/geckodriver')


driver.get(urlpage)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
time.sleep(5)

results = driver.find_element_by_xpath('//*[@id="stats"]/div[2]/div[2]/table')
data = results.text.replace('\n',';').replace(' ',',')

with open('scraped_data.csv', 'w') as outfile:
    outfile.write(data)
    outfile.close()

print(data)

driver.quit()

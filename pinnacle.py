from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv

from bs4 import BeautifulSoup

# List of sports and their links

# sports = {
#     "basketball" : {
#         "nba", 
#         "ncaa"
#     },
#     "esports/games" : {
#         "csgo",
#         "league-of-legends",
#         "dota-2"
#     },
#     "football" : {
#         "nfl",
#         "ncaa"
#     },
#     "hockey" : {
#         "nhl"
#     },
#     "soccer" : {
#         "germany-bundesliga",
#         "uefa-champions-league",
#         "uefa-europa-league",
#         "spain-la-liga",
#         "france-ligue-1",
#         "england-premier-league",
#         "italy-serie-a"
#     },
#     "tennis" : None,
#     "mixed-martial-arts" : {
#         "ufc"
#     },
#     "baseball" : {
#         "mlb"
#     }
# }

sports = {
    "basketball" : {
        "nba", 
    }
}


web = 'https://www.pinnacle.com/en/' 
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("user-agent={}".format(user_agent))
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)


#browser.get(web)
#browser.implicitly_wait(20)
#browser.get_screenshot_as_file('main-page.png')

#content = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.XPATH, "/html/body/pre"))
#content_json = json.loads(content.text)
PINNACLE_MATCH_XPATH = "/html/body/div[2]/div/div[2]/main/div/div[4]/div[2]/div/div"

# loop through each sport above and get the player props
wait = WebDriverWait(browser, 10)
for sport in sports:
    leagues = sports[sport]
    if leagues is not None:
        for league in leagues:
            site = web + "{}/{}/matchups".format(sport, league)

            browser.get(site)
            browser.implicitly_wait(15)
            browser.get_screenshot_as_file('{}-{}.png'.format(sport, league))

            div = 3


            #match = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/main/div/div[4]/div[2]/div/div[3]/div[1]/div/a")))
            #         
            #match = browser.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/main/div/div[4]/div[2]/div/div[3]/div[1]/div/a")

            
            while True:
                try:
                    match = browser.find_element(By.XPATH, "{}[{}]/div[1]/div/a".format(PINNACLE_MATCH_XPATH, div))
                    #match = wait.until(EC.presence_of_element_located((By.XPATH, "{}[{}]/div[1]/div/a".format(PINNACLE_MATCH_XPATH, div))))
                    # get link from match and open a new browser window
                    match_link = match.get_attribute("href")
                    print(match_link)
                    browser.get(match_link)
                    browser.implicitly_wait(10)
                    browser.get_screenshot_as_file('{}-forward.png'.format(sport))
                    browser.close()
                    browser.get_screenshot_as_file('{}-back.png'.format(sport))
                    
                    div+=1
                except Exception as e:
                    print(e)
                    break
            
            


            
            #matches = wait.until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "{}/{}/".format(sport,league))))
            #print(matches)

    else:
        site = web + "{}/matchups".format(sport)
        
        browser.get(site)
        browser.implicitly_wait(15)
        browser.get_screenshot_as_file('{}.png'.format(sport))

    # go to each individual match in the league 

    
#     wait = WebDriverWait(browser, 10)
    
    
#     #matches = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "style_row__3q4g_ style_row__3hCMX")))
    

# #     for match in matches:
# #         element = wait.until(EC.element_to_be_clickable(element))
# #         element.click()

# #         # brings to a new page
# #         browser.implicitly_wait(15)
# #         browser.get_screenshot_as_file('{}.png'.format(sport))
# #         exit()

    browser.quit()

# # //*[@id="main"]/div/div[4]/div[2]/div/div[3]
# # //*[@id="main"]/div/div[4]/div[2]/div/div[4]
    
# # #main > div > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(3)
# # #main > div > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(4)

# # document.querySelector("#main > div > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(3)")
    
# # //*[@id="main"]/div/div[4]/div[2]/div/div[2]
# # /html/body/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[2]/div/div[3]
# # /html/body/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[2]/div/div[7]
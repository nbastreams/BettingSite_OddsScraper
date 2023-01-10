from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import json
import csv

# List of tags that prizepicks uses in their projections - that we want to keep
attribute_tags = ['description', 'line_score', 'stat_type',
    'flash_sale_line_score', 'is_promo', 'start_time',  'updated_at']
relationship_tags = ['league', 'name', 'position', 'team']

#projection_tags = ['id'] + relationship_tags + attribute_tags
projection_tags = relationship_tags + attribute_tags

web = 'https://api.prizepicks.com/projections' 
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("user-agent={}".format(user_agent))
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)


browser.get(web)
browser.implicitly_wait(10)
#browser.get_screenshot_as_file('main-page.png')

content = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.XPATH, "/html/body/pre"))
content_json = json.loads(content.text)

player_info = content_json['included']
data = content_json['data']


with open('projections.csv', mode='w', encoding='utf-8-sig') as csv_file:

    writer = csv.DictWriter(csv_file, fieldnames=projection_tags, extrasaction='ignore', dialect='excel')
    writer.writeheader()

    #print(csv.list_dialects())

    # For each projection get the player name + info and store it all in a csv
    for projection in data:
        if projection['type'] == 'projection':
            id = projection['relationships']['new_player']['data']['id']
            for player in player_info:
                if player['type'] == 'new_player':
                    if player['id'] == id:
                        #print(player['attributes'])
                        projection['relationships']['new_player']['data'] = player['attributes']
                        del projection['relationships']['stat_type']
                        del projection['relationships']['projection_type']
                        row = {
                            'id': projection['id']
                        }
                        for attribute in projection['attributes']:
                            row[attribute] = projection['attributes'][attribute]
                        
                        for relationship in projection['relationships']:
                            if relationship == 'new_player':
                                for key in projection['relationships']['new_player']['data']:
                                    row[key] = projection['relationships']['new_player']['data'][key]
                            else:
                                row[relationship] = projection['relationships'][relationship]

                        writer.writerow(row)


from requests_html import HTMLSession
import csv

url = 'https://www.pinnacle.com' 

GAME_TIME_TAG = '/html/body/div[2]/div/div[2]/main/div[1]/div[2]/div[2]/div/span'
PROP_TAG = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[1]/span[1]'
PROP_OVER_TAG = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[2]/div/div/div[1]/button/span[1]'
ODDS_OVER_TAG = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[2]/div/div/div[1]/button/span[2]'
#prop_under_tag = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[2]/div/div/div[2]/button/span[1]'
ODDS_UNDER_TAG = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[2]/div/div/div[2]/button/span[2]'


PROJECTION_TAGS = ['player_name', 'game_time', 'prop_type', 'prop_line', 'odds_over', 'odds_under']

SPORTS = {
    "basketball" : {
        "nba", 
        "ncaa"
    },
    "esports/games" : {
        "csgo",
        "league-of-legends",
        "dota-2"
    },
    "football" : {
        "nfl",
        "ncaa"
    },
    "hockey" : {
        "nhl"
    },
    "soccer" : {
        "germany-bundesliga",
        "uefa-champions-league",
        "uefa-europa-league",
        "spain-la-liga",
        "france-ligue-1",
        "england-premier-league",
        "italy-serie-a"
    },
    "baseball" : {
        "mlb"
    }
}



session = HTMLSession()

# create a list of all links
league_urls = []
match_urls = []
for sport in SPORTS:
    leagues = SPORTS[sport]
    if leagues is not None:
        for league in leagues:
            league_url = url + "/en/{}/{}/matchups/".format(sport, league)
            league_urls.append(league_url)

            r = session.get(league_url)
            r.html.render(sleep = 5)
            possible_match_urls = r.html.links

            for possible_match_url in possible_match_urls:
                #print(match_url)
                if possible_match_url.startswith("{}{}/{}".format("/en/", sport, league)):
                    #print(possible_match_url)
                    match_urls.append(possible_match_url)


    else:
        league_url = url + "/en/{}/matchups".format(sport)
        league_urls.append(league_url)

        r = session.get(league_url)
        r.html.render(sleep = 5)
        possible_match_urls = r.html.links

        for possible_match_url in possible_match_urls:
            #print(match_url)
            if possible_match_url.startswith("{}{}".format("/en/", sport)):
                #print(possible_match_url)
                match_urls.append(possible_match_url)

# open csv and write heard
with open('pinnacle_player_props.csv', mode='w', encoding='utf-8-sig') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=PROJECTION_TAGS, extrasaction='ignore', dialect='excel')
    writer.writeheader()


for match_url in match_urls:
    try:
        match_prop_url = "{}{}{}".format(url, match_url, "/#player-props")
        r = session.get(match_prop_url)
        r.html.render(wait = 1.0, sleep = 5)

        prop_id = 1
        props = []
        game_time = r.html.xpath(GAME_TIME_TAG)[0].text
        #print(game_time)
        while True:
            
            try:
                prop_title = r.html.xpath(PROP_TAG.format(prop_id))[0].text

                try:
                    prop_over = r.html.xpath(PROP_OVER_TAG.format(prop_id))[0].text
                    odds_over = r.html.xpath(ODDS_OVER_TAG.format(prop_id))[0].text
                    odds_under = r.html.xpath(ODDS_UNDER_TAG.format(prop_id))[0].text

                    player_name = prop_title.split('(')[0].rstrip()
                    prop_type = prop_title.split('(')[1].split(')')[0].strip()
                    prop_line = prop_over.split()[1]

                    prop = {'player_name': player_name, 'game_time': game_time, 'prop_type': prop_type, 'prop_line': prop_line, 'odds_over': odds_over, 'odds_under': odds_under}
                    props.append(prop)
                except Exception as e:
                    #print(e)
                    pass
                

                prop_id+=1
            except Exception as e:
                break
        
        with open('pinnacle_player_props.csv', mode='a', encoding='utf-8-sig') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=PROJECTION_TAGS, extrasaction='ignore', dialect='excel')

            for prop in props:
                writer.writerow(prop)

    except Exception as e:
        #print(e)
        pass

session.close()
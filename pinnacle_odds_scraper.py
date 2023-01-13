from requests_html import HTMLSession
import csv

url = 'https://www.pinnacle.com' 

game_time_tag = '/html/body/div[2]/div/div[2]/main/div[1]/div[2]/div[2]/div/span'
prop_tag = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[1]/span[1]'
prop_over_tag = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[2]/div/div/div[1]/button/span[1]'
odds_over_tag = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[2]/div/div/div[1]/button/span[2]'
#prop_under_tag = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[2]/div/div/div[2]/button/span[1]'
odds_under_tag = '/html/body/div[2]/div/div[2]/main/div[3]/div[{}]/div[2]/div/div/div[2]/button/span[2]'


projection_tags = ['player_name', 'game_time', 'prop_type', 'prop_line', 'odds_over', 'odds_under']
file_name = 'pinnacle.csv'

sports = {
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
    # "soccer" : {
    #     "germany-bundesliga",
    #     "uefa-champions-league",
    #     "uefa-europa-league",
    #     "spain-la-liga",
    #     "france-ligue-1",
    #     "england-premier-league",
    #     "italy-serie-a"
    # },
    # "baseball" : {
    #     "mlb"
    # }
}



session = HTMLSession()

# create a list of all links
league_urls = []
match_urls = []

# loop through all sports and leagues and find all the match urls
for sport in sports:
    leagues = sports[sport]
    if leagues is not None:
        for league in leagues:
            league_url = url + "/en/{}/{}/matchups/".format(sport, league)
            league_urls.append(league_url)

            # find all the urls on the page
            r = session.get(league_url)
            r.html.render(sleep = 5)
            possible_match_urls = r.html.links

            # check which urls are an actual match (and not a random url)
            for possible_match_url in possible_match_urls:
                if possible_match_url.startswith("{}{}/{}".format("/en/", sport, league)):
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

# create empty csv then write header
with open(file_name, mode='w', encoding='utf-8-sig') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=projection_tags, extrasaction='ignore', dialect='excel')
    writer.writeheader()

# loop through all the match urls (for every sport/league)
for match_url in match_urls:
    try:
        # load the player props page
        match_prop_url = "{}{}{}".format(url, match_url, "/#player-props")
        r = session.get(match_prop_url)
        r.html.render(wait = 1.0, sleep = 5)

        prop_id = 1
        props = []

        # get the game time data and all the player props
        game_time = r.html.xpath(game_time_tag)[0].text
        while True:
            
            try:
                prop_title = r.html.xpath(prop_tag.format(prop_id))[0].text

                try:
                    prop_over = r.html.xpath(prop_over_tag.format(prop_id))[0].text
                    odds_over = r.html.xpath(odds_over_tag.format(prop_id))[0].text
                    odds_under = r.html.xpath(odds_under_tag.format(prop_id))[0].text

                    player_name = prop_title.split('(')[0].rstrip()
                    prop_type = prop_title.split('(')[1].split(')')[0].strip()
                    prop_line = prop_over.split()[1]

                    prop = {'player_name': player_name, 'game_time': game_time, 'prop_type': prop_type, 'prop_line': prop_line, 'odds_over': odds_over, 'odds_under': odds_under}
                    props.append(prop)
                except Exception as e:
                    print(e)
                    pass
                
                prop_id+=1

            except Exception as e:
                print(e)
                break
        
        # for each match_url append the player props (if not empty)
        if len(props) > 0:
            with open(file_name, mode='a', encoding='utf-8-sig') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=projection_tags, extrasaction='ignore', dialect='excel')

                for prop in props:
                    writer.writerow(prop)

    except Exception as e:
        print(e)
        pass

session.close()
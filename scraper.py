from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

web = 'https://app.prizepicks.com/' 
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


try:
    close = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div[1]')
    close.click()
    del(close)
    time.sleep(1)
except:
    pass


login = browser.find_element_by_xpath('//*[@id="header"]/div/div[2]/button[1]')
login.click()
time.sleep(1)
del(login)

email = browser.find_element_by_xpath('//*[@id="email-input"]')
password = browser.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div[1]/div[2]/form/div[3]/input')

myEmail = ''
email.send_keys('kwiskel@gmail.com')
time.sleep(1)

myPassword = ''
password.send_keys('23WCGazStNvmVMp@')
time.sleep(1)

submit = browser.find_element_by_xpath('//*[@id="submit-btn"]')
submit.click()
time.sleep(1)

my_entries = browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[1]/div/div[1]/div/div[1]/div/ul/li[2]/a')
my_entries.click()
time.sleep(1)


entries = browser.find_elements_by_class_name('entry')
for entry in entries:
    names = entry.find_elements_by_class_name('name')
    types = entry.find_elements_by_class_name('type')
    scores = entry.find_elements_by_class_name('score')
    stat_types = entry.find_elements_by_class_name('stat-type')
    for i in range(len(names)):
        print("{}: {} {} {}".format(names[i].text, types[i].text, scores[i].text, stat_types[i].text))

browser.close()

'''
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "nav-user-account"))).click() ##drop down menu
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sign-btn"))).click() ##sign in button
emailElement = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "fm-login-id")))
emailElement.click()
'''

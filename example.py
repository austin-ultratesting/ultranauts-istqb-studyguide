# import packages
import os.path
import pickle
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from jupytercards import md2json, display_flashcards

def save_cookies():
    print("Saving cookies in " + istqb_cookies_file)
    pickle.dump(driver.get_cookies(), open(istqb_cookies_file, "wb"))

def load_cookies():
    print("Loading cookies from " + istqb_cookies_file)
    cookies = pickle.load(open(istqb_cookies_file, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("All cookies loaded!")

istqb_cookies_file = "istqb_cookies.pkl"
page_url = "https://glossary.istqb.org/en_US/search?term=&exact_matches_first=true&page=30"
delay = 15 # seconds
key_terms = ''''''
# create webdriver object and go to page URL
driver = webdriver.Chrome()
driver.get(page_url)

if os.path.exists(istqb_cookies_file) and os.path.isfile(istqb_cookies_file):
    try:
        load_cookies()
        WebDriverWait(driver, delay).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.MuiBox-root.muiltr-6lyagu")))
    except TimeoutException:
        print("Loading took too much time!")
    except:
        print("Cookies Failed to Load")
else:
    try:
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "div.cc-nb-main-container button.cc-nb-okagree"))).click()
        WebDriverWait(driver, delay).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.MuiBox-root.muiltr-6lyagu")))
        save_cookies()
    except TimeoutException:
        print("Loading took too much time!")

print("Page is ready!")

istqb_glossary_key_terms = driver.find_elements(By.CSS_SELECTOR, "div.MuiBox-root.muiltr-6lyagu")

for key_term in istqb_glossary_key_terms:
    key_term_header = key_term.find_element(By.TAG_NAME, "h3")
    key_term_definition = key_term.find_element(By.TAG_NAME, "p")
    key_terms += '''## ''' + key_term_header.text + '''\n''' + key_term_definition.text + '''\n'''

driver.close()

markdown = open("key_terms.md", "w")
markdown.write(key_terms)

myjson=md2json(key_terms, "glossary_terms_cards.json")
print(myjson)

display_flashcards(myjson)

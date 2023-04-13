import datetime
import time
from random import randrange
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd

import filename_safe
import user


def main():
    listings = {
        "keyword": [],
        "title": [],
        "price": [],
        "url": [],
        "location": [],
    }

    for key in range(len(user.user["facebook.marketplace.keywords"])):
        print("Searching for " + user.user["facebook.marketplace.keywords"][key])
        search = driver.find_element("xpath", "//*[@aria-label='Search Marketplace']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        search.send_keys(user.user["facebook.marketplace.keywords"][key])
        search.send_keys(Keys.RETURN)
        time.sleep(randrange(1,8))
        for title in driver.find_elements("xpath", "//*[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6'][@style='-webkit-box-orient: vertical; -webkit-line-clamp: 2; display: -webkit-box;']"):
            listings["keyword"].append(user.user["facebook.marketplace.keywords"][key])
            listings["title"].append(str(title.text))
        for price in driver.find_elements("xpath", './/*[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u"][@dir="auto"]'):
            listings["price"].append(str(price.text))
        for url in driver.find_elements("xpath", './/a[contains(@href,"/marketplace/item")][@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv"]'):
            listings["url"].append(url.get_attribute("href"))
        for location in driver.find_elements("xpath", ".//*[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84'][string-length(text()) > 0]"):
            listings["location"].append(str(location.text))
        # driver.quit()
    print(str(listings))
    print(str(len(listings["keyword"])))
    print(str(len(listings["title"])))
    print(str(len(listings["price"])))
    print(str(len(listings["url"])))
    print(str(len(listings["location"])))
    df = pd.DataFrame(
        data=[listings["keyword"], listings["title"], listings["price"], listings["url"], listings["location"]],
        index=["keyword", "title", "price", "url", "location"])
    df = (df.T)
    df.to_excel(filename_safe.clean_filename(str(datetime.datetime.now())) + ".xlsx")
    driver.quit()


def signin():
    print("Signing in")
    email_box = driver.find_element("name", "email")
    email_box.send_keys(user.user["facebook.email"])
    password_box = driver.find_element("name", "pass")
    password_box.send_keys(user.user["facebook.password"])
    password_box.send_keys(Keys.RETURN)
    time.sleep(randrange(3, 6))
    driver.get("https://www.facebook.com/marketplace")
    main()
    print("Signed in")


if __name__ == "__main__":
    print("!!! Due to the nature of how Facebook handles web scraping, the sleep times between pages randomly changes to throw off Facebook.")
    PATH = "chromedriver.exe"
    options = Options()
 #   options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(PATH, options=options)
    driver.get("https://www.facebook.com")
    print("Connected to Facebook Marketplace")
    signin()

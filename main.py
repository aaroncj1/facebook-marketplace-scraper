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
        search = driver.find_element_by_xpath("//*[@aria-label='Search Marketplace']")
        search.send_keys(user.user["facebook.marketplace.keywords"][key])
        search.send_keys(Keys.RETURN)
        time.sleep(randrange(1,8))
        for title in driver.find_elements_by_xpath("//*[@class='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7'][@style='-webkit-box-orient: vertical; -webkit-line-clamp: 2; display: -webkit-box;']"):
            listings["keyword"].append(user.user["facebook.marketplace.keywords"][key])
            listings["title"].append(str(title.text))
        for price in driver.find_elements_by_xpath(".//*[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id'][@dir='auto']"):
            listings["price"].append(str(price.text))
        for url in driver.find_elements_by_xpath('.//a[contains(@href,"/marketplace/item")][@class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 p8dawk7l"]'):
            listings["url"].append(url.get_attribute("href"))
        for location in driver.find_elements_by_xpath(".//*[@class='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5 ojkyduve'][string-length(text()) > 0]"):
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
    email_box = driver.find_element_by_name("email")
    email_box.send_keys(user.user["facebook.email"])
    password_box = driver.find_element_by_name("pass")
    password_box.send_keys(user.user["facebook.password"])
    password_box.send_keys(Keys.RETURN)
    time.sleep(randrange(3, 6))
    main()
    print("Signed in")


if __name__ == "__main__":
    print("!!! Due to the nature of how Facebook handles web scraping, the sleep times between pages randomly changes to throw off Facebook.")
    PATH = "chromedriver.exe"
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(PATH, options=options)
    driver.get("https://www.facebook.com/marketplace/")
    print("Connected to Facebook Marketplace")
    signin()

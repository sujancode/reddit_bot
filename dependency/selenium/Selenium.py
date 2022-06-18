from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def getSeleniumBrowserAutomation():
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-notifications')
    option.add_argument("--mute-audio")
    # option.add_argument('--headless')
    # option.add_argument('--disable-gpu') 
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    return driver
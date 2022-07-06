from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from webdriver_manager.core.utils import ChromeType

def getSeleniumBrowserAutomation():
    
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-notifications')
    option.add_argument("--mute-audio")
    option.add_argument('--headless')
    option.add_argument('--disable-gpu') 
    option.add_argument('--no-sandbox')
    option.add_argument("--disable-dev-shm-usage") 

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    return driver
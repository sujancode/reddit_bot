from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from webdriver_manager.core.utils import ChromeType
import random
def getSeleniumBrowserAutomation():
    
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-notifications')
    option.add_argument("--mute-audio")
    option.add_argument('--headless')
    option.add_argument('--disable-gpu') 
    option.add_argument("enable-automation")
    option.add_argument("--disable-infobars")

    option.add_argument('--no-sandbox')
    option.add_argument("--disable-dev-shm-usage") 
    option.add_argument(f"window-size={random.randint(1000,2000)},{random.randint(1000,2000)}")


    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    return driver
import time
from dependency.captchaResolver.index import getTextToSpeechCaptchaResolver
from dependency.selenium.Selenium import getSeleniumBrowserAutomation

from dependency.reddit.index import getRedditWrapperInstance
from dependency.database.index import getDatabaseWrapperInstance

from entities.RedditUser import RedditUser
from dependency.logger.index import getLoggerInstance

from datetime import datetime
import os


DEFAULT_DELAY=2
BASE_URL="https://old.reddit.com"
ACCOUNT_REGISTER=f"{BASE_URL}/register"
APP_REGISTER_URL=f"{BASE_URL}/prefs/apps/"

def handle_account_creation(browser,reddit_user):
    browser.get(ACCOUNT_REGISTER)

    #user Input Text
    username_input=browser.find_element_by_id("user_reg")
    username_input.send_keys(reddit_user.username)

    time.sleep(DEFAULT_DELAY)

    #password Input Text
    password_input=browser.find_element_by_id("passwd_reg")
    password_input.send_keys(reddit_user.password)

    time.sleep(DEFAULT_DELAY)
    
    #verify password Input Text
    verify_password_input = browser.find_element_by_id("passwd2_reg")
    verify_password_input.send_keys(reddit_user.password)

    time.sleep(DEFAULT_DELAY)


    #Resolving Captcha
    captchaSolver=getTextToSpeechCaptchaResolver(browserWrapper=browser)
    captchaSolver.resolve()

    time.sleep(DEFAULT_DELAY)
    
    browser.switch_to.parent_frame()   


    sign_up_btn=browser.find_element_by_css_selector("#register-form .c-submit-group .c-btn")
    sign_up_btn.click()
    time.sleep(DEFAULT_DELAY)



def handle_developer_app_creation(browser):
    
    browser.get(APP_REGISTER_URL)
    time.sleep(DEFAULT_DELAY)

    edit_app_button=browser.find_elements_by_css_selector(".edit-app-button")
    if len(edit_app_button)>0:
        edit_app_button[0].click()
    else:
        time.sleep(DEFAULT_DELAY)    
        #Create APP Button
        browser.find_element_by_id("create-app-button").click()
    

        #Select Script Input Select Type
        browser.find_element_by_css_selector("[value='script']").click()

        #input name box
        browser.find_element_by_css_selector("form input[name='name']").send_keys("good application")
    
        #description input
        browser.find_element_by_css_selector("form textarea[name='description']").send_keys("good application")

        #redirect url 

        browser.find_element_by_css_selector("form input[name='redirect_uri']").send_keys("http://127.0.0.1:8000")

        #submit button
        browser.find_element_by_css_selector("form button[type='submit']").click()

    #getting client Secret and client id
    time.sleep(DEFAULT_DELAY)

    client_id=browser.find_element_by_css_selector("#developed-apps ul li:first-child .app-details h3:nth-child(3)").text
    client_secret=browser.find_element_by_css_selector(".edit-app-form table tbody:first-child td").text
    

    
    return {
        "client_id":client_id,
        "client_secret":client_secret
    }
    


def handle_login(browser,reddit_user):
    browser.get(ACCOUNT_REGISTER)
    time.sleep(DEFAULT_DELAY)

    #user Input Text
    username_input=browser.find_element_by_id("user_login")
    username_input.send_keys(reddit_user.username)

    #password Input Text
    password_input=browser.find_element_by_id("passwd_login")
    password_input.send_keys(reddit_user.password)

    sign_in_btn=browser.find_element_by_css_selector("#login-form .c-submit-group .c-btn")
    sign_in_btn.click()

    time.sleep(DEFAULT_DELAY)    

def stop_instance():
    os.system("sudo shutdown now -h")

def run():
    browser=None
    log_data={
        "account":"",
        "date":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "message":[]
    }
    logger=getLoggerInstance("account_logger")

    try:
    
        password="Earning$$"

        browser=getSeleniumBrowserAutomation()
        reddit=getRedditWrapperInstance()
        db=getDatabaseWrapperInstance()

        username=reddit.get_random_name(browser=getSeleniumBrowserAutomation())
        log_data["username"]=username

        reddit_user=RedditUser(username,password)

        print(f"Creating User with username{username}")

        log_data["message"].append("Creating User with username{username}")
        logger.dispatchLog(log_data)
        
        handle_account_creation(browser=browser,reddit_user=reddit_user)
        
        print("Creating reddit application: Getting->Client Id and Client Secret")
        log_data["message"].append("Creating reddit application: Getting->Client Id and Client Secret")
        logger.dispatchLog(log_data)

        client_info=handle_developer_app_creation(browser=browser)
        
        reddit_user.client_id=client_info["client_id"]
        reddit_user.client_secret=client_info["client_secret"]

        db.insert("accounts",{
            "username":reddit_user.username,
            "password":reddit_user.password,
            "client_id":reddit_user.client_id,
            "client_secret":reddit_user.client_secret,
            "isBanned":False
        })
        log_data["message"].append("Success")
        logger.dispatchLog(log_data)

    except Exception as e:
        print(e)
        log_data["message"].append(str(e))
        logger.dispatchLog(log_data)

    finally:
        if browser:
            browser.close()
        stop_instance()
            


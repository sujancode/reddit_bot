import os
import time
from selenium.webdriver.common.by import By

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

class CaptchaSolver:
    def __init__(self,browserWrapper,requests):
        self.browserWrapper=browserWrapper
        self.requests=requests

    def audioToText(self,mp3Path,driver):
        print("1")
        driver.execute_script('''window.open("","_blank");''')
        driver.switch_to.window(driver.window_handles[1])
        print("2")
        driver.get("https://speech-to-text-demo.ng.bluemix.net/")
        delayTime = 10
        # Upload file
        time.sleep(1)
        print("3")
        # Upload file
        time.sleep(1)
        root = driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
        btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
        btn.send_keys(mp3Path)
        # Audio to text is processing
        time.sleep(delayTime)
        #btn.send_keys(path)
        print("4")
        # Audio to text is processing
        time.sleep(10)

        print("5")
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements_by_tag_name('span')
        print("5.1")
        result = " ".join( [ each.text for each in text ] )
        print("6")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("7")
        return result

    def find_audio_btn(self,driver,allIframes):
        for index in range(len(allIframes)):
            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[index]
            driver.switch_to.frame(iframe)
            driver.implicitly_wait(1)
            try:
                audioBtn = driver.find_element_by_id('recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
                audioBtn.click()
                return index
            except Exception as e:
                pass
        return False

    def download_audio_file(self,driver,filename):
        filepath=f"{BASE_DIR}/{filename}"
        href = driver.find_element_by_id('audio-source').get_attribute('src')
        response = self.requests.get(href, stream=True)
        
        with open(filepath, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)
        return filepath

    def resolve(self):        
        driver=self.browserWrapper
        googleClass=None
        while not googleClass:
            try:
                print("Pressing Captcha")
                googleClass=driver.find_element_by_css_selector("[title=reCAPTCHA]")
                print(googleClass)
            
            except:
                print("Error")

        time.sleep(2)
        
        googleClass.click()


        allIframes=driver.find_elements_by_tag_name("iframe")
        
        audioBtnIndex=self.find_audio_btn(driver=driver,allIframes=allIframes)
        
        if audioBtnIndex:
            try:
                while True:
                    audio_path=self.download_audio_file(driver,f"1.mp3")
                    print(audio_path)
                    response = self.audioToText(mp3Path=audio_path,driver=driver)
                    
                    driver.switch_to.default_content()
                    iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
                    driver.switch_to.frame(iframe)
                    inputbtn = driver.find_element_by_id('audio-response')
                    inputbtn.send_keys(response)
                    inputbtn.send_keys("\ue007")                    
                    time.sleep(2)
                    errorMsg = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
                    if errorMsg.text == "" or errorMsg.value_of_css_property('display') == 'none':
                        print("Success")
                        return True
            except Exception as e:
                print(e)
                print("Most Probably Change Proxies or Use Proxies")
        return False            

        
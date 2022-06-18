import os
import time
from .speechToText import get_large_audio_transcription

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

class CaptchaSolver:
    def __init__(self,browserWrapper,requests):
        self.browserWrapper=browserWrapper
        self.requests=requests

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
                    response = get_large_audio_transcription(audio_path)
                    
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

        
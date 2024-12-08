
from datetime import timezone, datetime, time, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys



def meet_on_telemost(meet):

    opt = Options()
    opt.add_argument('--disable-blink-features=AutomationControlled')
    opt.add_argument('--start-maximized')
    opt.add_experimental_option("prefs", {

        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 0,
        "profile.default_content_setting_values.notifications": 1
    })

    driver = webdriver.Chrome(options=opt)
    driver.implicitly_wait(20)
    driver.get('https://telemost.yandex.ru/connect-to-meeting-by-id')
    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/form/span/input').send_keys(meet.room_uri)
    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/form/button').click()
    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div[1]/div/div/button').click()




    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[1]/button').click()
    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[2]/div/button').click()

    el = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div[1]/span/input')

    for i in range(1,6):
        el.send_keys(Keys.BACKSPACE)

    el.send_keys('MinutesBot')

    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/button').click()

    if meet.end_meet_date >= datetime.now(timezone.utc):
        driver.quit()



def meet_on_skype(url):
    #https://join.skype.com/EuIzxDQmR6Xh
    opt = Options()
    opt.add_argument('--disable-blink-features=AutomationControlled')
    opt.add_argument('--start-maximized')
    opt.add_experimental_option("prefs", {

        "profile.default_content_setting_values.media_stream_mic": 2,
        "profile.default_content_setting_values.media_stream_camera": 2,
        "profile.default_content_setting_values.geolocation": 0,
        "profile.default_content_setting_values.notifications": 1
    })
    driver = webdriver.Chrome(options=opt)
    driver.implicitly_wait(10)

    driver.get(url)

    driver.find_element(By.XPATH,'//*[@id="meetNowContainer"]/div/div/div/div[2]/div[2]/label/a').click()
    driver.find_element(By.XPATH,'//*[@id="meetingJoinLink"]').send_keys('https://join.skype.com/Indru144DV0u')
    driver.find_element(By.XPATH,'//*[@id="meetNowContainer"]/div/div/div/div[2]/button').click()
    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/button').click()
    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[1]/div/d'
                                 'iv/div/div/div[2]/div/div[4]/div[3]/div/div/div/div/input').send_keys('MinutesBot')

    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[5]/div[2]/button').click()


    leave = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div['
                                 '1]/div/div[1]/div/div/div/div[11]/div/div[2]/div[2]/button')
    leave.click()








meet_on_telemost()









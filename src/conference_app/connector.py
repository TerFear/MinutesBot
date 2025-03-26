
from datetime import *
from fastapi import FastAPI
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys


app = FastAPI()


@app.get("/connect/{meet_url}")
def connection(meet_url):
    opt = Options()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--headless')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--start-maximized')
    opt.add_experimental_option("prefs", {

        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 0,
        "profile.default_content_setting_values.notifications": 1
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)



    driver.implicitly_wait(30)
    driver.get("https://telemost.yandex.ru/connect-to-meeting-by-id")

    try:

        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div/form/span/input').send_keys(
            meet_url)
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div/form/button').click()
        time.sleep(2)
        time.sleep(2)
        time.sleep(2)
        driver.find_element(By.XPATH,
                            '//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[1]/button').click()
        time.sleep(2)
        driver.find_element(By.XPATH,
                            '//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[2]/div/button').click()

        time.sleep(2)

        el = driver.find_element(By.XPATH,
                                 '//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div[1]/span/input')
        time.sleep(2)

        for i in range(1, 6):
            el.send_keys(Keys.BACKSPACE)


        el.send_keys('MinutesBot')
        time.sleep(2)
        driver.find_element(By.XPATH,
                            '//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/button').click()
        print("Подключение к конференции было успешно завершенно ...")
        time.sleep(30)
        return {'success': True, "block_status": False, 'current.url': driver.current_url}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'success':False,"block_status": True,'current.url': driver.current_url}
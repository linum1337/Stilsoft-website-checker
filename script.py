import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


def website_scrap():
    print("Started")
    global results
    results = open("results.txt", 'w') #Инит тхт для вывода
    # Красиво что бы браузер не доставал
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

    url = "https://stilsoft.ru/products/kitsoz-synerget"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                              options=options)
    try:

        driver.get(url=url)
        driver.set_window_size(1439, 818)
        time.sleep(3)
        elems = driver.find_elements(By.CLASS_NAME, "product_anker  ") #Достаю все href под этим классом
        for i in range(0, len(elems), 2):  # Извлекаю ссылки
            img_and_warranty(elems[i].get_attribute('href'))  # Отправляю на проверку

    except:
        print("Stopped")
        return 0

    finally:
        driver.close()
        driver.quit()
        results.close()
        print("Successfully!")


def img_and_warranty(cur_url):
    req = requests.get(cur_url)
    bs_meal = BeautifulSoup(req.text, 'lxml')
    warranty = str(bs_meal.find('li', string=re.compile('срок службы'))).split()[-2]
    img = str(bs_meal.find(class_='imgCont')).split()[-1]
    if int(warranty) <= 7:
        results.write(f"URL: {cur_url} | WARRANTY: {warranty} | Срок службы менее 7 лет! \n")
    if img == "None":
        results.write(f"URL: {cur_url} | IMAGE: {img} | Нет изображения! \n")


website_scrap()

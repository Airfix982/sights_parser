import tkinter as tk
import requests
import re
import selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tkinter import messagebox

def parse_extraguide(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        countries = soup.find_all('h2', class_="all-sights-h2")
        with open('texts/countries_1.txt', 'w', encoding='utf-8') as file:
            for i, country in enumerate(countries):
                if i > 0:
                    file.write("\n")
                file.write(country.get_text(strip=True))
    else:
        print(f"Ошибка при доступе к странице: {response.status_code}")


def parse_turizm(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Находим все элементы li с определенным классом
        list_items = soup.find_all('li', class_='infolist_alfa__item')

        with open('texts/countries_2.txt', 'w', encoding='utf-8') as file:
            for i, item in enumerate(list_items):
                hidden_div = item.find('div', class_="hidden-xs")
                if hidden_div:
                    country_div = hidden_div.find_next_sibling('div')
                    if country_div:
                        country_name = country_div.get_text(strip=True)
                        if i > 0:
                            file.write("\n")
                        file.write(country_name)
    else:
        print(f"Ошибка при доступе к странице: {response.status_code}")


    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # driver.get(url)
    # #wait = WebDriverWait(driver, 10)  # Ожидание до 10 секунд
    # #wait.until(EC.presence_of_element_located((By.ID, "content")))  # Ждать, пока элемент с id='content' не появится
    # html = driver.page_source
    # driver.quit()

    # soup = BeautifulSoup(html, 'html.parser')
    # pattern = re.compile('cs-.*')
    # li_elements = soup.find_all('li', class_=pattern)

    # for li in li_elements:
    #     print(li)
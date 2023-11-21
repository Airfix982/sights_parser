import tkinter as tk
import requests
import re
import selenium
import os

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
    countries = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        countries_elements = soup.find_all('h2', class_="all-sights-h2")
        for country in countries_elements:
            countries.append(country.get_text(strip=True))
        return countries
    else:
        print(f"Ошибка при доступе к странице: {response.status_code}")

def parse_turizm(url):
    countries = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        list_items = soup.find_all('li', class_='infolist_alfa__item')
        for item in list_items:
            hidden_div = item.find('div', class_="hidden-xs")
            if hidden_div:
                country_div = hidden_div.find_next_sibling('div')
                if country_div:
                    countries.append(country_div.get_text(strip=True))
        return countries
    else:
        print(f"Ошибка при доступе к странице: {response.status_code}")

def parse_tourister(url):
    countries = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        country_divs = soup.find_all('div', class_='sitemap_country_links')
        for div in country_divs:
            h2_tag = div.find_previous_sibling('h2')
            if h2_tag:
                countries.append(h2_tag.get_text(strip=True))
        return countries
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
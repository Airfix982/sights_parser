import json
import os
import requests
import re
from bs4 import BeautifulSoup

def init_parse_extraguide(url_info):
    base_url = url_info["url"]
    countries_cities = {}
    countries_cities_simple = {}  # Для возвращения без ссылок

    response = requests.get(base_url, cookies=url_info["cookies"], headers=url_info["headers"])
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        countries_elements = soup.find_all('h2', class_="all-sights-h2")

        for country_element in countries_elements:
            country_name = country_element.get_text(strip=True)
            next_ul = country_element.find_next_sibling('ul')
            cities = []
            cities_simple = []  # Только названия городов

            if next_ul:
                for city_element in next_ul.find_all('a'):
                    city_name = city_element.get_text(strip=True)
                    city_url = base_url.rstrip('/sights/') + city_element['href']
                    cities.append({"name": city_name, "url": city_url})
                    cities_simple.append(city_name)  # Добавляем только название города

            countries_cities[country_name] = cities
            countries_cities_simple[country_name] = cities_simple
    else:
        print(f"Ошибка при доступе к странице: {response.status_code}")
        return {}

    # Сохранение полной информации в файл JSON
    os.makedirs('configs', exist_ok=True)
    with open('configs/extraguide.json', 'w', encoding='utf-8') as file:
        json.dump(countries_cities, file, indent=4, ensure_ascii=False)

    # Возвращаем упрощенный список стран и городов без ссылок
    return countries_cities_simple

def init_parse_wikiway(url_info):
    base_url = url_info["url"].rstrip('/')
    countries_cities = {}  # Для сохранения полной информации
    countries_cities_simple = {}  # Для возврата упрощенной информации

    response = requests.get(base_url, cookies=url_info["cookies"], headers=url_info["headers"])
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        countries_elements = soup.find_all('li', class_=re.compile(r'cs-\w+'))

        for country_element in countries_elements:
            link_element = country_element.find('a')
            if link_element:
                country_name = link_element.find('span').get_text(strip=True)
                country_href = link_element['href']
                country_url = base_url + country_href
                city_url = country_url + 'goroda/'
                countries_cities[country_name] = {"url": country_url, "cities": []}
                countries_cities_simple[country_name] = []

                country_response = requests.get(city_url, cookies=url_info["cookies"], headers=url_info["headers"])
                if country_response.status_code == 200:
                    country_soup = BeautifulSoup(country_response.content, 'html.parser')
                    city_elements = country_soup.find_all('div', class_='ob-block')

                    for city_element in city_elements:
                        city_link = city_element.find('a', class_='ob-href')
                        if city_link:
                            city_name = city_element.find('div', class_='ob-tz').get_text(strip=True)
                            full_city_url = base_url + city_link['href']
                            countries_cities[country_name]["cities"].append({"name": city_name, "url": full_city_url})
                            countries_cities_simple[country_name].append(city_name)

    else:
        print(f"Ошибка при доступе к странице: {response.status_code}")
        return {}

    # Сохранение полной информации в файл JSON
    os.makedirs('configs', exist_ok=True)
    with open('configs/wikiway.json', 'w', encoding='utf-8') as file:
        json.dump(countries_cities, file, indent=4, ensure_ascii=False)

    # Возвращаем упрощенный список стран и городов без ссылок
    return countries_cities_simple



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


#     {
#     "country1_name": ["city1_name", "city2_name", ...],
#     "country2_name": ["city3_name", "city4_name", ...],
#     ...
# }

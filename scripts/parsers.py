import json
import ijson
import os
import requests
import hashlib
import re
from bs4 import BeautifulSoup
from classes import Sight

def save_to_json(path, data):
    os.makedirs(path.split('/')[0], exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def init_parse_extraguide(url_info, settings):
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
    
    save_to_json(settings["extraguide_data"], countries_cities)
    return countries_cities_simple

def init_parse_wikiway(url_info, settings):
    base_url = url_info["url"].rstrip('/')
    countries_sights = {}
    countries_cities = {}

    response = requests.get(base_url, cookies=url_info["cookies"], headers=url_info["headers"])
    if response.status_code != 200:
        print(f"Ошибка при доступе к странице: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    countries_elements = soup.find_all('li', class_=re.compile(r'cs-\w+'))

    for country_element in countries_elements:
        link_element = country_element.find('a')
        if not link_element:
            continue

        country_name = link_element.find('span').get_text(strip=True)
        country_href = link_element['href']
        country_url = base_url + country_href
        cities = set()

        # Запрос страницы достопримечательностей страны
        sights_response = requests.get(country_url + "dostoprimechatelnosti/", cookies=url_info["cookies"], headers=url_info["headers"])
        if sights_response.status_code == 200:
            sights_soup = BeautifulSoup(sights_response.content, 'html.parser')
            sights_elements = sights_soup.find_all('div', class_='ob-block')

            for sight_element in sights_elements:
                sight_link = sight_element.find('a', class_='ob-href')
                if sight_link:
                    sight_name = sight_element.find('div', class_='ob-tz').get_text(strip=True)
                    sight_url = base_url + sight_link['href']
                    city_element = sight_element.find('a', class_='city-href')
                    city_name = city_element.get_text(strip=True) if city_element else "Не указан"
                    if city_name != "Не указан":
                        cities.add(city_name)
                    countries_sights.setdefault(country_name, {})[sight_url] = city_name
        countries_cities[country_name] = list(cities)

    # Сохранение данных о достопримечательностях в файл
    save_to_json(settings["wikiway_data"], countries_sights)

    return countries_cities

def save_to_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)








def load_hashes(hash_path):
    try:
        with open(hash_path, 'r', encoding='utf-8') as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON из файла {hash_path}.")
        return set()

def update_hashes(hash_path, new_hashes):
    hashes = load_hashes(hash_path)
    hashes.update(new_hashes)  # Объединение множеств
    with open(hash_path, 'w', encoding='utf-8') as file:
        json.dump(list(hashes), file, indent=4)


    
def load_sights_for_country_wikiway(country_name, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return list(data.get(country_name, {}).items())
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return []
    
def parse_sight_page_wikiway(url, headers, cookies, base_url, settings):
    response = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1').get_text(strip=True)
    description = soup.find('div', class_='txt-body').get_text(strip=True)

    image_url = soup.find('div', class_='obj-info')['style'].split('url(')[-1].split(')')[0]
    image_url = base_url + image_url
    image_name = str(hash(description))[:10] + '.jpg'
    download_image_wikiway(image_url, image_name, headers, cookies, settings)

    return title, description, image_name, url

def download_image_wikiway(image_url, image_name, headers, cookies, settings):
    response = requests.get(image_url, headers=headers, cookies=cookies)
    path = settings["img_path"]
    with open(f"{path}{image_name}", 'wb') as file:
        file.write(response.content)





def load_sights_for_country_extraguide(country_name, path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            country_key = country_name.capitalize()
            country_data = data.get(country_key, [])
            return [(sight["url"], sight["name"]) for sight in country_data]
    except FileNotFoundError:
        print(f"Файл {path} не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON из файла {path}.")
        return []
    
def parse_sight_page_extraguide(city_url, headers, cookies, base_url, settings, count, num_sights):
    response = requests.get(city_url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    sights = []
    sight_containers = soup.find('div', class_='row rows sight-center').find_all('div', class_='mobimg')
    for container in sight_containers:
        if count == num_sights:
            break
        count += 1
        title_block = container.find_previous_sibling('h2')
        title = title_block.get_text(strip=True) if title_block else ""
        description_block = container.find_next_sibling('p')
        description = description_block.get_text(strip=True) if description_block else ""
        image_block = container.find('a')
        img_url = image_block['href'] if image_block else ""
        image_url = base_url.split("/sights")[0] + img_url
        image_name = str(hash(description))[:10] + '.jpg'
        download_image_extraguide(image_url, image_name, headers, cookies, settings)

        sights.append((title, description, image_name, city_url))

    return sights

def download_image_extraguide(image_url, image_name, headers, cookies, settings):
    response = requests.get(image_url, headers=headers, cookies=cookies)
    path = settings["img_path"]
    with open(f"{path}{image_name}", 'wb') as file:
        file.write(response.content)




def parse_country(settings, num_sights, *args):
    country_name = args[0].capitalize()
    sights = []
    new_hashes = load_hashes(settings["hash_path"])

    # Загрузка и добавление данных с сайта Wikiway
    sights_data_wikiway = load_sights_for_country_wikiway(country_name, settings["wikiway_data"])
    web_settings_wikiway = json.load(open(settings["web_urls"]))["urls"]["wikiway"]
    headers_wikiway = web_settings_wikiway["headers"]
    cookies_wikiway = web_settings_wikiway["cookies"]
    base_url_wikiway = web_settings_wikiway["url"].rstrip('/')

    for sight_url, city_name in sights_data_wikiway:
        if len(sights) >= num_sights:
            break
        title, description, image_name, url = parse_sight_page_wikiway(sight_url, headers_wikiway, cookies_wikiway, base_url_wikiway, settings)
        sight_hash = image_name.split('.')[0]
        if sight_hash not in new_hashes:
            sight_object = Sight(country_name, city_name if city_name != "Не указан" else "", title, description, f"img/{image_name}", url, sight_hash)
            sights.append(sight_object)
            new_hashes.add(sight_hash)

    # Проверка, нужно ли загружать данные с сайта Extraguide
    if len(sights) < num_sights:
        sights_data_extraguide = load_sights_for_country_extraguide(country_name, settings["extraguide_data"])
        web_settings_extraguide = json.load(open(settings["web_urls"]))["urls"]["extraguide"]
        headers_extraguide = web_settings_extraguide["headers"]
        cookies_extraguide = web_settings_extraguide["cookies"]
        base_url_extraguide = web_settings_extraguide["url"].rstrip('/')

        for city_url, city_name in sights_data_extraguide:
            if len(sights) >= num_sights:
                break
            sights_ex = parse_sight_page_extraguide(city_url, headers_extraguide, cookies_extraguide, base_url_extraguide, settings, 0, num_sights - len(sights))

            for title, description, image_name, url in sights_ex:
                sight_hash = image_name.split('.')[0]
                if sight_hash not in new_hashes:
                    sight_object = Sight(country_name, city_name, title, description, f"img/{image_name}", url, sight_hash)
                    sights.append(sight_object)
                    new_hashes.add(sight_hash)
                    if len(sights) >= num_sights:
                        break

    update_hashes(settings["hash_path"], new_hashes)
    return sights







    






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

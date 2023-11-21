import json
import os

from parsers import parse_extraguide, parse_tourister, parse_turizm

def get_urls(urls_path):
    with open(urls_path, 'r') as file:
        config = json.load(file)
        return list(config["urls"].values())
    

def get_countries(*urls):
    all_countries = []
    for url in urls:
        if url:
            all_countries.extend(url())
    return list(set(all_countries))


def get_countries_list(countries_path, urls):
    if os.path.exists(countries_path):
        with open(countries_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        countries = get_countries(
            lambda: parse_extraguide(urls[0]),
            lambda: parse_turizm(urls[1]),
            lambda: parse_tourister(urls[2])
        )
        with open(countries_path, 'w', encoding='utf-8') as file:
            json.dump(countries, file)
        return countries
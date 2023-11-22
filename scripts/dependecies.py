import json
import os
from parsers import init_parse_extraguide, init_parse_wikiway

def get_settings():
    with open("configs/settings.json", "r", encoding="utf-8") as file:
        return json.load(file)

def get_urls():
    urls_path = get_settings()["web_urls"]
    with open(urls_path, 'r') as file:
        config = json.load(file)
        return config["urls"]

def merge_country_data(existing_data, new_data):
    for country, cities in new_data.items():
        if country in existing_data:
            existing_data[country] = list(set(existing_data[country] + cities))
        else:
            existing_data[country] = cities
    return existing_data

def get_init_data(*parsers):
    all_data = {}
    for parse in parsers:
        parsed_data = parse()
        all_data = merge_country_data(all_data, parsed_data)
    return all_data

def get_parse_data():
    settings = get_settings()
    urls = get_urls()

    parse_data_path = settings["parse_data"]

    if os.path.exists(parse_data_path):
        with open(parse_data_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        init_data = get_init_data(
            lambda: init_parse_extraguide(urls["extraguide"]),
            lambda: init_parse_wikiway(urls["wikiway"])
        )
        with open(parse_data_path, 'w', encoding='utf-8') as file:
            json.dump(init_data, file, indent=4)
        return init_data
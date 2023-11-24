class Sight:
    def __init__(self, country_name, city_name, sight_name, description, photo_path, url, hash):
        self.country_name = country_name
        self.city_name = city_name
        self.sight_name = sight_name
        self.description = description
        self.photo_path = photo_path
        self.hash = hash
        self.url = url

    def __repr__(self):
        return f"Sight(country_name={self.country_name}, city_name={self.city_name}, sight_name={self.sight_name}, url={self.url}, hash={self.hash})"

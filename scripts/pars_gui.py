import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import shutil
from dependecies import get_parse_data, get_settings, start_parsing
from classes import Sight


class DataApp:
    def __init__(self, root):
        self.root = root
        self.settings = get_settings()
        self.country_city_data = self.load_country_city_data()
        self.sights = []

        self.root.title("Сбор данных о городах и странах")
        self.root.geometry("1000x500")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Создание виджета Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Создание вкладки "Сбор"
        self.collect_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.collect_frame, text="Сбор")

        # Создание вкладки "Галерея"
        self.gallery_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.gallery_frame, text="Галерея")

        # Добавление интерфейса на вкладку "Сбор"
        self.create_collect_interface()
        self.get_sights()
        # Добавление интерфейса на вкладку "Галерея"
        # self.create_gallery_interface()

    def get_sights(self):
        if os.path.exists(self.settings["sights_path"]):
            with open(self.settings["sights_path"], "r", encoding="utf-8") as file:
                sights_from_json = json.load(file)
                for sight in sights_from_json:
                    sight_object = Sight(sight["country_name"], sight["city_name"], sight["sight_name"], sight["description"], sight["photo_path"], sight["url"], sight["hash"])
                    self.sights.append(sight_object)

    def load_country_city_data(self):
        country_city_data = get_parse_data()
        formatted_data = {}
        for country, cities in country_city_data.items():
            formatted_data[country.lower()] = [city.lower() for city in cities.keys()]
        return formatted_data


    def create_collect_interface(self):
        ttk.Label(self.collect_frame, text="Выберите страну:").pack()
        self.country_var = tk.StringVar()
        self.country_var.trace("w", self.update_city_list)
        self.country_combobox = ttk.Combobox(self.collect_frame, textvariable=self.country_var)
        self.country_combobox['values'] = [self.format_string(country) for country in sorted(self.country_city_data.keys())]
        self.country_combobox.pack()

        ttk.Label(self.collect_frame, text="Выберите город:").pack()
        self.city_var = tk.StringVar()
        self.city_combobox = ttk.Combobox(self.collect_frame, textvariable=self.city_var)
        self.city_combobox.pack()

        ttk.Label(self.collect_frame, text="Выберите макс. количество:").pack()
        self.num_sights_var = tk.StringVar()
        self.num_sights_entry = ttk.Entry(self.collect_frame, textvariable=self.num_sights_var)
        self.num_sights_entry.pack()

        start_button = tk.Button(self.collect_frame, text="Начать сбор данных", bg="#004158", fg="white", 
                                 command=lambda: self.on_start_button_click())
        start_button.pack(pady=10)

        clear_button = tk.Button(self.collect_frame, text="Удалить все данные", bg="#3f3f3f", fg="white", 
                                 command=lambda: self.discard_data(close=False))
        clear_button.pack(pady=10)

    def format_string(self, s):
        """Форматирование строки с заглавной первой буквой."""
        return s.capitalize()

    def update_city_list(self, *args):
        """Обновление списка городов на основе введенной страны."""
        selected_country = self.country_var.get().lower()
        cities = self.country_city_data.get(selected_country, [])
        self.city_combobox['values'] = [self.format_string(city) for city in sorted(cities)]

    def on_start_button_click(self):
        country = self.country_var.get().lower()
        city = self.city_var.get().capitalize()
        try:
            num_sights = int(self.num_sights_var.get())
            if num_sights <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите корректное число достопримечательностей.")
            return

        if country not in self.country_city_data or (city and city not in [c.capitalize() for c in self.country_city_data[country]]):
            messagebox.showerror("Ошибка ввода", "Выбранная страна или город не найдены. Пожалуйста, выберите из списка.")
            return

        if not city:
            self.sights = start_parsing(self.sights, num_sights, country)
        else:
            self.sights = start_parsing(self.sights, num_sights, country, city)
        

    def discard_data(self, close=True):
        if not close:
            if messagebox.askyesno("Подтверждение", "Удалить скачанные данные?"):
                pass
            else:
                return
        try:
            shutil.rmtree(self.settings["img_path"])
            print(f"Папка {self.settings['img_path']} удалена.")
        except OSError as e:
            print(f"Ошибка при удалении папки {self.settings['img_path']}: {e.strerror}")

        try:
            os.remove(self.settings['hash_path'])
            print(f"Файл {self.settings['hash_path']} удален.")
        except OSError as e:
            print(f"Ошибка при удалении файла {self.settings['hash_path']}: {e.strerror}")
        try:
            os.remove(self.settings['sights_path'])
            print(f"Файл {self.settings['sights_path']} удален.")
        except OSError as e:
            print(f"Ошибка при удалении файла {self.settings['sights_path']}: {e.strerror}")
        with open(self.settings["parse_data"], 'r', encoding='utf-8') as file:
            data = json.load(file)
        for country in data:
            for city in data[country]:
                data[country][city] = 0
        with open(self.settings["parse_data"], "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        
        print("Данные не сохранены")
    
    def save_data(self):
        sights_data = [sight.to_dict() for sight in self.sights]
        with open(self.settings["sights_path"], "w", encoding="utf-8") as file:
            json.dump(sights_data, file, indent=4, ensure_ascii=False)

    def on_close(self):
        """Функция, вызываемая при закрытии приложения."""
        if messagebox.askyesno("Подтверждение", "Сохранить скачанные данные?"):
            self.save_data()
        else:
            self.discard_data()
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
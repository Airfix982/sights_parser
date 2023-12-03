import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk, PhotoImage
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
        self.root.geometry("1040x500")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Создание виджета Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Создание вкладки "Сбор"
        self.collect_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.collect_frame, text="Сбор")

        # Создание вкладки "Галерея"
        self.gallery_frame = ttk.Frame(self.notebook)
        self.scrollable_frame = tk.Frame(self.gallery_frame)
        self.canvas = tk.Canvas(self.scrollable_frame)

        self.gallery_row = 0
        self.gallery_column = 0

        self.scrollable_gallery = tk.Frame(self.canvas)
        self.notebook.add(self.gallery_frame, text="Галерея")

        # Добавление интерфейса на вкладку "Сбор"
        self.create_collect_interface()
        self.get_sights()
        # Добавление интерфейса на вкладку "Галерея"
        self.create_gallery_interface()

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
    
    def create_gallery_interface(self):
        self.scrollable_frame = tk.Frame(self.gallery_frame)
        self.canvas = tk.Canvas(self.scrollable_frame)
        
        self.scrollable_gallery = tk.Frame(self.canvas)
        self.notebook.add(self.gallery_frame, text="Галерея")

        scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)

        self.scrollable_gallery.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_gallery, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Создание первого вложенного фрейма для элементов галереи
        self.current_gallery_row = tk.Frame(self.scrollable_gallery)
        self.current_gallery_row.pack(fill="both", expand=True)

        for sight in self.sights:
            self.create_sight_widget(sight, self.current_gallery_row)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.scrollable_frame.pack(fill="both", expand=True)

    def on_tab_changed(self, event):
        selected_tab = event.widget.select()
        selected_tab_title = event.widget.tab(selected_tab, "text")
        if selected_tab_title == "Галерея":
            self.update_gallery()

    def update_gallery(self):
    # Удаление всех существующих виджетов
        for widget in self.scrollable_gallery.winfo_children():
            widget.destroy()

        # Пересоздание первого вложенного фрейма для элементов галереи
        self.current_gallery_row = tk.Frame(self.scrollable_gallery)
        self.current_gallery_row.pack(fill="both", expand=True)

        # Добавление элементов в галерею
        for sight in self.sights:
            self.create_sight_widget(sight, self.current_gallery_row)

    def create_sight_widget(self, sight, parent_frame):
        max_size = (300, 300)
        container = tk.Frame(parent_frame, borderwidth=2, relief="groove")

        container.pack(side="left", padx=10, pady=10)  # Добавление отступов вокруг контейнера

        # Проверка, нужно ли создать новый ряд
        if len(self.current_gallery_row.winfo_children()) >= 3:
            self.current_gallery_row = tk.Frame(self.scrollable_gallery)
            self.current_gallery_row.pack(fill="both", expand=True)

        if os.path.exists(sight.photo_path):
            img = Image.open(sight.photo_path)
            img.thumbnail(max_size)  # Resize image
            photo = ImageTk.PhotoImage(img)
        else:
            # Load default image if file not found
            default_img = Image.open('path/to/default/image')  # Specify path to default image
            default_img.thumbnail(max_size)
            photo = ImageTk.PhotoImage(default_img)

        image_label = tk.Label(container, image=photo)
        image_label.image = photo
        image_label.pack(padx=5, pady=5)  # Add padding around the image

        if sight.city_name:
            text = f"{sight.sight_name} ({(sight.city_name).capitalize()}, {(sight.country_name).capitalize()})"
        else:
            text = f"{sight.sight_name} ({(sight.country_name).capitalize()})"
        text_label = tk.Label(container, text=text, cursor="hand2")
        text_label.pack(padx=5, pady=5)  # Add padding around the text
        text_label.bind("<Button-1>", lambda event: self.show_sight_description(sight))


    def show_sight_description(self, sight):
        messagebox.showinfo(sight.sight_name, sight.description)


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

        self.update_gallery()
        self.root.update_idletasks()
        print(len(self.sights))
        

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
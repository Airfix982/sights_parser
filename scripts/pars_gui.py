import tkinter as tk
from tkinter import messagebox, ttk
from dependecies import get_parse_data

def format_string(s):
    """Форматирование строки с заглавной первой буквой."""
    return s.capitalize()

def update_city_list(*args):
    """Обновление списка городов на основе введенной страны."""
    selected_country = country_var.get().lower()
    cities = country_city_data.get(selected_country, [])
    city_combobox['values'] = [format_string(city) for city in sorted(cities)]

def on_start_button_click(country_city_data):
    country = country_var.get().lower()
    city = city_var.get().capitalize()
    if country not in country_city_data or (city and city not in [c.capitalize() for c in country_city_data[country]]):
        messagebox.showerror("Ошибка ввода", "Выбранная страна или город не найдены. Пожалуйста, выберите из списка.")
        return
    # Здесь код для начала сбора данных

if __name__ == "__main__":
    country_city_data = {key.lower(): [city.lower() for city in cities] for key, cities in get_parse_data().items()}
    root = tk.Tk()
    root.title("Сбор данных о городах и странах")
    root.geometry("400x200")

    ttk.Label(root, text="Выберите страну:").pack()
    country_var = tk.StringVar()
    country_var.trace("w", update_city_list)
    country_combobox = ttk.Combobox(root, textvariable=country_var)
    country_combobox['values'] = [format_string(country) for country in sorted(country_city_data.keys())]
    country_combobox.pack()

    ttk.Label(root, text="Выберите город:").pack()
    city_var = tk.StringVar()
    city_combobox = ttk.Combobox(root, textvariable=city_var)
    city_combobox.pack()

    start_button = tk.Button(root, text="Начать сбор данных", bg="#004158", fg="white", command=lambda: on_start_button_click(country_city_data))
    start_button.pack(pady=10)

    root.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk
from dependecies import get_parse_data

def on_country_select(event):
    selected_country = country_var.get()
    cities = country_city_data.get(selected_country, [])
    city_combobox['values'] = sorted(cities)
    city_combobox.set('')

def on_start_button_click(country_city_data):
    country = country_var.get()
    city = city_var.get()
    if country not in country_city_data or (city and city not in country_city_data[country]):
        messagebox.showerror("Ошибка ввода", "Выбранная страна или город не найдены. Пожалуйста, выберите из списка.")
        return
    # Здесь код для начала сбора данных

if __name__ == "__main__":
    country_city_data = get_parse_data()
    root = tk.Tk()
    root.title("Сбор данных о городах и странах")
    root.geometry("400x200")

    ttk.Label(root, text="Выберите страну:").pack()
    country_var = tk.StringVar()
    country_combobox = ttk.Combobox(root, textvariable=country_var)
    country_combobox['values'] = sorted(country_city_data.keys())
    country_combobox.bind('<<ComboboxSelected>>', on_country_select)
    country_combobox.pack()

    ttk.Label(root, text="Выберите город:").pack()
    city_var = tk.StringVar()
    city_combobox = ttk.Combobox(root, textvariable=city_var)
    city_combobox.pack()

    start_button = tk.Button(root, text="Начать сбор данных", bg="#004158", fg="white", command=lambda:on_start_button_click(country_city_data))
    start_button.pack(pady=10)

    root.mainloop()
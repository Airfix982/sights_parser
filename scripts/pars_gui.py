import tkinter as tk
from tkinter import messagebox

def start_scraping():
    url = url_entry.get()
    messagebox.showinfo("Info", f"Начат сбор данных с {url}")

def show_page_one():
    page_one.pack(fill="both", expand=True)
    page_two.pack_forget()

def show_page_two():
    page_two.pack(fill="both", expand=True)
    page_one.pack_forget()

# Создание главного окна
root = tk.Tk()
root.title("Сбор данных из Интернета")
root.geometry("600x400") 

# Создание бокового меню
side_panel = tk.Frame(root, bg="#A9A9A9")
side_panel.pack(side="left", fill="y")

# Кнопки на боковом меню
button1 = tk.Button(side_panel, text="Страница 1", command=show_page_one)
button1.pack(fill="x")

button2 = tk.Button(side_panel, text="Страница 2", command=show_page_two)
button2.pack(fill="x")

# Создание двух страниц
page_one = tk.Frame(root, bg="#f7f7f7")
page_two = tk.Frame(root, bg="#f7f7f7")

# Элементы на странице 1
label_one = tk.Label(page_one, text="Введите корневой URL:", bg="#f7f7f7")
label_one.pack(pady=10)

url_entry = tk.Entry(page_one, width=30)
url_entry.pack(pady=10)

start_button = tk.Button(page_one, text="Начать сбор данных", command=start_scraping, bg="#004851", fg="white")
start_button.pack(pady=20)

# Элементы на странице 2 (пример)
label_two = tk.Label(page_two, text="Страница 2", bg="#f7f7f7")
label_two.pack(pady=10)

# Показать первую страницу по умолчанию
show_page_one()

# Запуск главного цикла Tkinter
root.mainloop()

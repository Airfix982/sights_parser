import tkinter as tk
from tkinter import messagebox

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="Подсказка", color='grey', highlight_color='red'):
        super().__init__(master, highlightthickness=1, highlightbackground=highlight_color)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _add_placeholder(self, event=None):
        if not self.get():
            self.configure(fg=self.placeholder_color)
            self.insert(0, self.placeholder)

    def _clear_placeholder(self, event=None):
        if self['fg'] == self.placeholder_color:
            self.delete(0, "end")
            self['fg'] = self.default_fg_color

def start_scraping():
    country = country_entry.get()
    city = city_entry.get()
    messagebox.showinfo("Info", f"Начат сбор данных для страны: {country}, города: {city}")

def show_page_one():
    page_one.pack(fill="both", expand=True)
    page_two.pack_forget()

def show_page_two():
    page_two.pack(fill="both", expand=True)
    page_one.pack_forget()

if __name__ == "__main__":
    # Создание главного окна
    root = tk.Tk()
    root.title("Сбор данных из Интернета")
    root.geometry("600x400") 

    # Создание бокового меню
    side_panel = tk.Frame(root, bg="#004158")
    side_panel.pack(side="left", fill="y")

    # Кнопки на боковом меню
    button1 = tk.Button(side_panel, text="Сбор данных", command=show_page_one)
    button1.pack(fill="x")

    button2 = tk.Button(side_panel, text="Галерея", command=show_page_two)
    button2.pack(fill="x")

    # Создание двух страниц
    page_one = tk.Frame(root, bg="#f7f7f7")
    page_two = tk.Frame(root, bg="#f7f7f7")

    # Элементы на странице 1
    country_label = tk.Label(page_one, text="Введите страну:", bg="#f7f7f7")
    country_label.pack(pady=10)

    country_entry = PlaceholderEntry(page_one, "Страна", color='grey', highlight_color='red')
    country_entry.pack(pady=10)

    city_label = tk.Label(page_one, text="Введите город: -не обязательно", bg="#f7f7f7")
    city_label.pack(pady=10)

    city_entry = PlaceholderEntry(page_one, "Город", color='grey', highlight_color='#343434')
    city_entry.pack(pady=10)

    start_button = tk.Button(page_one, text="Начать сбор данных", command=start_scraping, bg="#004851", fg="white")
    start_button.pack(pady=10)

    # Элементы на странице 2 (пример)
    label_two = tk.Label(page_two, text="Страница 2", bg="#f7f7f7")
    label_two.pack(pady=10)

    # Показать первую страницу по умолчанию
    show_page_one()

    # Запуск главного цикла Tkinter
    root.mainloop()

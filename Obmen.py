from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests

def update_base_currency_label(event):
    # Получаем полное название базовой валюты из словаря и обновляем метку
    code = base_combobox.get()
    name = currencies[code]
    base_currency_label.config(text=name)

def update_target_currency_label(event):
    # Получаем полное название целевой валюты из словаря и обновляем метку
    code = target_combobox.get()
    name = currencies[code]
    target_currency_label.config(text=name)

def exchange():
    target_code = target_combobox.get()
    base_code = base_combobox.get()

    if target_code and base_code:
        try:
            # Делаем запрос к API ЦБ РФ
            response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
            response.raise_for_status()
            data = response.json()

            # Получаем курсы обеих валют к рублю
            if base_code == "RUB":
                base_rate = 1.0
            elif 'Valute' in data and base_code in data['Valute']:
                base_rate = data['Valute'][base_code]['Value']
            else:
                mb.showerror("Ошибка", f"Базовая валюта {base_code} не найдена")
                return

            if target_code == "RUB":
                target_rate = 1.0
            elif 'Valute' in data and target_code in data['Valute']:
                target_rate = data['Valute'][target_code]['Value']
            else:
                mb.showerror("Ошибка", f"Целевая валюта {target_code} не найдена")
                return

            # Рассчитываем курс между выбранными валютами
            exchange_rate = target_rate / base_rate
            mb.showinfo("Курс обмена", f"1 {base_code} = {exchange_rate:.4f} {target_code}")

        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning("Внимание", "Выберите коды валют")


# Словарь кодов валют и их полных названий
currencies = {
    "USD": "Американский доллар",
    "EUR": "Евро",
    "JPY": "Японская йена",
    "GBP": "Британский фунт стерлингов",
    "AUD": "Австралийский доллар",
    "CAD": "Канадский доллар",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "RUB": "Российский рубль",
    "KZT": "Казахстанский тенге",
    "UZS": "Узбекский сум"
}

# Создание графического интерфейса
window = Tk()
window.title("Курс обмена валюты")
window.geometry("400x250")

Label(text="Базовая валюта:").pack(padx=10, pady=5)
base_combobox = ttk.Combobox(values=list(currencies.keys()))
base_combobox.pack(padx=10, pady=5)
base_combobox.bind("<<ComboboxSelected>>", update_base_currency_label)

base_currency_label = ttk.Label(text="Выберите валюту")
base_currency_label.pack(padx=10, pady=2)

Label(text="Целевая валюта:").pack(padx=10, pady=5)
target_combobox = ttk.Combobox(values=list(currencies.keys()))
target_combobox.pack(padx=10, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_target_currency_label)

target_currency_label = ttk.Label(text="Выберите валюту")
target_currency_label.pack(padx=10, pady=2)

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)

window.mainloop()






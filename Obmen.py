from tkinter import *
from tkinter import messagebox as mb
import requests
import json
from tkinter import ttk

def exchange():
    code = combobox.get()
    if not code:
        mb.showwarning("Внимание", "Введите код валюты (например, USD, EUR)")
        return

    try:
        # Делаем запрос к API ЦБ РФ
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        response.raise_for_status()
        data = response.json()

        # Проверяем наличие валюты в ответе
        if 'Valute' in data and code in data['Valute']:
            exchange_rate = data['Valute'][code]['Value']
            mb.showinfo("Курс обмена", f"Курс {code} к рублю: {exchange_rate:.2f} руб. за 1 {code}")
        else:
            mb.showerror("Ошибка", f"Валюта с кодом '{code}' не найдена.\nПроверьте правильность кода (например, USD, EUR).")

    except requests.exceptions.RequestException as e:
        mb.showerror("Ошибка сети", f"Не удалось получить данные: {e}")
    except json.JSONDecodeError:
        mb.showerror("Ошибка", "Ошибка обработки данных от сервера.")
    except Exception as e:
        mb.showerror("Ошибка", f"Неизвестная ошибка: {e}")

# Создаем главное окно
window = Tk()
window.title("Курсы обмена валют")
window.geometry("400x200")


# Список 10 популярных валют

cur = ["EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "RUB", "KZT", "UZS"]

combobox=ttk.Combobox(values=cur)
combobox.pack(padx=10, pady=10)

entry = Entry()
entry.pack(padx=10, pady=10)
Button(text="Получить курс обмена к рублю", command=exchange).pack(padx=10, pady=10)

window.mainloop()




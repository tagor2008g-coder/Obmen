from tkinter import *
from tkinter import messagebox as mb
import requests
import json

def exchange():
    code = entry.get().upper()
    if code:
        try:
            response = requests.get(f'https://www.cbr-xml-daily.ru/daily_json.js')
            response.raise_for_status()
            data = response.json()

            if code in data['rates']:
                exchange_rate = data['rates'][code]

                mb.showinfo("Курс обмена", f"Курс к доллару: {exchange_rate:.1f} {code} за 1 доллар")
            else:
                mb.showerror("Ошибка", f"Валюта {code} не найдена")
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
        else:
            mb.showwarning("Внимание", "Введите код валюты")


window=Tk()
window.title("Курсы обмена валют")
window.geometry("360x180")

Label(text="Введите код валюты:").pack(padx=10, pady=10) #добавили отступы

entry = Entry()
entry.pack(padx=10, pady=10)

Button(text="Получить курс обмена к доллару", command=exchange).pack(padx=10, pady=10)

window.mainloop()




import tkinter as tk
import pandas as pd
from datetime import date
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu")
        self.master.geometry("400x400")
        self.master.config(bg="white")  # set background color
        self.menu = {"Cucina": {"Pizza": 10, "Pasta": 12, "Salad": 8},
                     "Santa Maria": {"Burger": 9, "Fries": 4, "Soda": 2},
                     "Preti": {"Steak": 20, "Fish": 18, "Soup": 6}}
        self.order = []
        self.today = date.today().strftime("%Y-%m-%d")
        self.df = pd.DataFrame(columns=["Order", "Price", "Category", "Date"])
        self.create_widgets()

    def create_widgets(self):
        self.category_labels = []
        self.category_buttons = []
        for i, category in enumerate(self.menu.keys()):
            self.category_labels.append(tk.Label(self.master, text=category, fg="white"))  # set label color
            self.category_labels[i].grid(row=i, column=0, padx=10, pady=10, sticky="w")
            self.category_buttons.append([])
            for j, item in enumerate(self.menu[category].keys()):
                name = item
                price = self.menu[category][item]
                self.category_buttons[i].append(tk.Button(self.master, text=f"{name} - ${price}",
                                                           command=lambda name=name, price=price: self.add_to_order(name, price)))
                self.category_buttons[i][j].grid(row=i, column=j+1, padx=10, pady=10)
        self.print_order_button = tk.Button(self.master, text="Print Order", command=self.print_order)
        self.print_order_button.grid(row=len(self.menu.keys())+1, column=0, padx=10, pady=10)

    def add_to_order(self, name, price):
        self.order.append((name, price))


    def print_order(self):
        print(f"Order length: {len(self.order)}")
        data = []
        for item in self.order:
            name, price = item
            category = ""
            for c in self.menu.keys():
                if name in self.menu[c].keys():
                    category = c
                    break
            data.append({"Order": name, "Price": price, "Category": category, "Date": self.today})
        print(f"Data length: {len(data)}")
        df = pd.DataFrame(data=data, columns=["Order", "Price", "Category", "Date"])
        self.df = pd.concat([self.df, df], ignore_index=True)
        self.df.to_excel(f"{self.today}_order.xlsx", index=False)
        self.order = []
        self.df = pd.DataFrame(columns=["Order", "Price", "Category", "Date"])

root = tk.Tk()
app = App(root)
root.mainloop()
import tkinter as tk
import pandas as pd
from datetime import date
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu")
        self.master.geometry("400x400")
        self.master.config(bg="white")  # set background color
        self.menu = {"Cucina": {"Pizza": {"Margherita": 10, "Pepperoni": 12, "Vegetarian": 8},
                        "Pasta": {"Spaghetti": 12, "Lasagna": 14, "Fettuccine Alfredo": 10},
                        "Salad": {"Caesar": 8, "Greek": 10, "Caprese": 9}},
             "Santa Maria": {"Burger": {"Cheeseburger": 9, "Bacon Burger": 11, "Veggie Burger": 8},
                             "Fries": {"Regular": 4, "Curly": 5, "Sweet Potato": 6},
                             "Soda": {"Coke": 2, "Sprite": 2, "Fanta": 2}},
             "Preti": {"Steak": {"Ribeye": 20, "Filet Mignon": 25, "New York Strip": 22},
                       "Fish": {"Salmon": 18, "Tilapia": 16, "Cod": 20},
                       "Soup": {"Minestrone": 6, "Tomato": 5, "Chicken Noodle": 7}}}
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
            j = 1
            for subcategory, items in self.menu[category].items():
                self.category_labels.append(tk.Label(self.master, text=subcategory, fg="white"))  # set label color
                self.category_labels[-1].grid(row=i, column=j, padx=10, pady=10, sticky="w")
                j += 1
                for k, (item, price) in enumerate(items.items()):
                    self.category_buttons.append(tk.Button(self.master, text=f"{item} - ${price}",
                                                            command=lambda item=item, price=price: self.add_to_order(item, price)))
                    self.category_buttons[-1].grid(row=i, column=j+k, padx=10, pady=10)
            i += 1
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
        self.df.to_excel(f"{self.today}_order.xlsx", index=False, mode="a", header=None)
        self.order = []
        self.df = pd.DataFrame(columns=["Order", "Price", "Category", "Date"])

root = tk.Tk()
app = App(root)
root.mainloop()
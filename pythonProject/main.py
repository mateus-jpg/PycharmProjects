import csv
import tkinter as tk
import pandas as pd
from datetime import date
from escpos.printer import Dummy
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu")
        self.master.geometry("400x400")
        self.master.config(bg="white")  # set background color
        self.menu = {

################ Menu Cucina #############################
            "Cucina": {


                "Cucina": {
                    # Pulled pork burger 9.5 vegan burger 9.5 sausage focaccia 7 cous cous 6 dolcetto 3 
                    "Pulled pork burger": 9.5,
                    "Vegan burger": 9.5,
                    "Sausage focaccia": 7,
                    "Cous cous": 6,
                    "Dolcetto": 3
                    }
                },

################ Menu Santa Maria #############################
             "Santa Maria": {
                "Burger": {
                    "Cheeseburger": 9, 
                    "Bacon Burger": 11, 
                    "Veggie Burger": 8
                    },
                "Fries": {
                    "Regular": 4, 
                    "Curly": 5, 
                    "Sweet Potato": 6
                    }
                },

 ################ Menu preti #############################    
             "Preti": {
                "BIBITE": {
                     "Chinotto Bio":3.5, 
                     "Aranciata Bio": 3.5, 
                     "Melagrana Bio": 3.5,
                     "Fritz Kola": 3.5,
                     "Fritz Kola zero": 3.5,
                     "Acqua": 1
                    },
                "VINO": {
                    "Tempesta (rosso)": 3, 
                    "Tempesta Bottiglia" :18,
                    "Sgass rosè": 3.5, 
                    "Sgass rosè Bottiglia": 20,
                    "Gran Selva": 3,
                    "Gran Selva Bottiglia": 18,
                    "Marescial (prosecco)": 3.5,
                    "Marescial Bottiglia": 20
                    },
                "AERITIVI" : {
                    # add spritz bianco 2 apritz aperol 3.5 spritz campari 3.5 americano 5.5
                    "Spritz bianco" : 2,
                    "Spritz aperol" : 3.5,
                    "Spritz campari" : 3.5,
                    "Americano" : 5.5
                    },
                "DRINKS": {
                    # add Negroni 7 gin tonic 5.5 gin lemon 5.5 vodka tonic 5.5 vodka lemon 5.5 moscow mule 7
                    "Negroni" : 7,
                    "Gin tonic" : 5.5,
                    "Gin lemon" : 5.5,
                    "Vodka tonic" : 5.5,
                    "Vodka lemon" : 5.5,
                    "Moscow mule" : 7
                    },
                }
            }
        self.order = []
        self.order_number = 0
        self.today = date.today().strftime("%Y-%m-%d")
        self.df = pd.DataFrame(columns=["Order", "Price", "Category", "Date"])
        self.create_widgets()

    def create_widgets(self):
        self.category_labels = []
        self.category_buttons = []
        column = 0
        for category, subcategories in self.menu.items():
            self.category_labels.append(tk.Label(self.master, text=category, fg="black"))
            self.category_labels[-1].grid(row=0, column=column+1, padx=10, pady=10, sticky="w")
            row = 1
            button_column = column
            for subcategory, items in subcategories.items():
                self.category_labels.append(tk.Label(self.master, text=subcategory, fg="black"))
                self.category_labels[-1].grid(row=row, column=column+1, padx=10, pady=10, sticky="w")
                row += 1
                for i, (item, price) in enumerate(items.items()):
                    self.category_buttons.append(tk.Button(self.master, text=f"{item}",
                                                            command=lambda item=item, price=price: self.add_to_order(item, price)))
                    self.category_buttons[-1].grid(row=row, column=button_column, padx=10, pady=10)
                    button_column += 1
                    if i % 3 == 2:
                        button_column = column
                        row += 1
                button_column = column
                row += 1
            column += 3
        self.order_text = tk.Text(self.master, width=50, height=30)
        self.order_text.grid(row=1, column=9, columnspan=3, padx=10, pady=10)
        self.delete_order_button = tk.Button(self.master, text="Delete Order", command=self.delete_order, bg="red")
        self.delete_order_button.grid(row=row, column= 3, padx=10, pady=10)
        self.delete_last_order_button = tk.Button(self.master, text="Delete Last Order", command=self.delete_last_order, bg="orange")
        self.delete_last_order_button.grid(row=row, column=4, padx=10, pady=10)
        self.print_order_button = tk.Button(self.master, text="Print Order", command=self.print_order, bg="green")
        self.print_order_button.grid(row=row, column=5,  padx=10, pady=10)

    def add_to_order(self, name, price, category):
        self.order.append(name, price, category)

    def delete_order(self): 
        self.order = []

    def delete_last_order(self):
        self.order.pop()

    def print_order(self):
        self.order_number += 1
        with USB(0x0416, 0x5011) as p:  # replace with your printer's vendor and product IDs
            p.text("Order:\n")
            for item, price,  in self.order:
                p.text(f"{item} - ${price}\n")
            total = sum(price for _, price in self.order)
            p.text(f"Total: ${total}\n")
        data = []
        for item in self.order:
            name, price = item
            category = ""
            for c in self.menu.keys():
                if name in self.menu[c].keys():
                    category = c
                    break
            data.append({"Order": name, "Price": price, "Category": category, "OrderNumber": self.order_number, "Date": self.today})
        with open(f"{self.today}_order.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Order", "Price", "Category", "OrderNumber", "Date"])
            if f.tell() == 0:
                writer.writeheader()
            writer.writerows(data)
        self.order = []

root = tk.Tk()
app = App(root)
root.mainloop()
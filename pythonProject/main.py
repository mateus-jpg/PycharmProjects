import tkinter as tk
import pandas as pd
from datetime import date
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
        self.today = date.today().strftime("%Y-%m-%d")
        self.df = pd.DataFrame(columns=["Order", "Price", "Category", "Date"])
        self.create_widgets()

    def create_widgets(self):
        self.category_labels = []
        self.category_buttons = []
        column = 0
        for category, subcategories in self.menu.items():
            self.category_labels.append(tk.Label(self.master, text=category, fg="white"))
            self.category_labels[-1].grid(row=0, column=column, padx=10, pady=10, sticky="w")
            row = 1
            for subcategory, items in subcategories.items():
                self.category_labels.append(tk.Label(self.master, text=subcategory, fg="white"))
                self.category_labels[-1].grid(row=row, column=column, padx=10, pady=10, sticky="w")
                row += 1
                for i, (item, price) in enumerate(items.items()):
                    self.category_buttons.append(tk.Button(self.master, text=f"{item} - ${price}",
                                                            command=lambda item=item, price=price: self.add_to_order(item, price)))
                    self.category_buttons[-1].grid(row=row, column=column, padx=10, pady=10)
                    if i % 3 == 2:
                        row += 1
                row += 1
            column += 1
        self.print_order_button = tk.Button(self.master, text="Print Order", command=self.print_order)
        self.print_order_button.grid(row=row, column=0, columnspan=column, padx=10, pady=10)

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
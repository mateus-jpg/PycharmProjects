import csv
import tkinter as tk
import pandas as pd
from datetime import date
from escpos.printer import Usb
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu")
        self.master.geometry("400x400")
        self.total = 0
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

                "SPINA": {
                    # SANTA MARIA 5 MOMPRACEM 5 WOTTGENSTEIN 5 GEROGE BEST 5
                    "Santa Maria": 5,
                    "Mompracem": 5,
                    "Wottgenstein": 5,
                    "George Best": 5
                },
                 "LATTINA": {
                     # SANTA MARIA 6 SAGE 'EM ALL 6 GESSLER 6
                        "Santa Maria": 6,
                        "Sage 'em all": 6,
                        "Gessler": 6,
                        "Session IPA": 6,
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
                    if i % 3 == 0 and i != 0:
                        button_column = column
                        row += 1
                    self.category_buttons.append(tk.Button(self.master, text=f"{item.center(20)}",
                                                            command=lambda item=item, price=price: self.add_to_order(item, price, category)))
                    self.category_buttons[-1].grid(row=row, column=button_column, padx=10, pady=10)
                    button_column += 1

                button_column = column
                row += 1
            column += 3
        self.order_text = tk.Text(self.master, width=50, height=30)
        self.order_text.grid(row=1, column=9, columnspan=3, rowspan=10, padx=10, pady=10)
        self.total_label = tk.Label(self.master, text="Total: 0€", fg="black")
        self.total_label.grid(row=14, column=9, columnspan=3, padx=10, pady=10)
        self.delete_order_button = tk.Button(self.master, text="Delete Order", command=self.delete_order, bg="red")
        self.delete_order_button.grid(row=row, column= 3, padx=10, pady=10)
        self.delete_last_order_button = tk.Button(self.master, text="Delete Last Order", command=self.delete_last_order, bg="orange")
        self.delete_last_order_button.grid(row=row, column=4, padx=10, pady=10)
        self.print_order_button = tk.Button(self.master, text="Print Order", command=self.print_order, bg="green")
        self.print_order_button.grid(row=row, column=5,  padx=10, pady=10)

    def add_to_order(self, name, price, category):
        self.order.append([name, price, category])
        self.order_text.insert(tk.END, f"{name} - ${price}\n")
        self.total += price
        self.total_label.config(text=f"Total: ${self.total}")

    def delete_order(self): 
        self.order = []
        self.order_text.delete("1.0", tk.END)
        self.total = 0
        self.total_label.config(text=f"Total: ${self.total}")

    def delete_last_order(self):
        if self.order:
            self.order.pop()
            self.order_text.delete("1.0", tk.END)
            for item, price, _ in self.order:
                self.order_text.insert(tk.END, f"{item} - ${price}\n")
            self.total -= price
            self.total_label.config(text=f"Total: ${self.total}")
    def print_order(self):
        self.order_number += 1
        with Usb(0x0416, 0x5011) as p:  # replace with your printer's vendor and product IDs
            for category, subcategories in self.menu.items():
                items_in_order = [name for name, _, _ in self.order if name in subcategories]
                if items_in_order:
                    p.text(f"----- {category} -----\n")
                    for item in items_in_order:
                        price = subcategories[item]
                        count = sum(1 for name, _, _ in self.order if name == item)
                        p.text(f"{item} x{count} - ${price * count:.2f}\n")
                    p.text("\n")
            total = sum(price for _, price, _ in self.order)
            p.text("Scontrino non fiscale")
            p.text("\n")
            p.text(f"Grazie! Stai sostentando la nostra raccolta fondi per Bajed Andala\n")
        data = []
        for item in self.order:
            name, price, category = item
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
        self.total = 0
        self.order_text.delete("1.0", tk.END)
        self.total_label.config(text=f"Total: ${self.total}")

root = tk.Tk()
app = App(root)
root.mainloop()
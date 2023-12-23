import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.geometry("700x500")
root.title("Gestion de Stock Pharmacie")
notebook = ttk.Notebook(root)
med_tab = ttk.Frame(notebook)
add_tab = ttk.Frame(notebook)
notebook.add(med_tab, text='Accueil')
notebook.add(add_tab, text='Ajouter')

####### l'onglet acceuille
filter_frame = tk.Frame(med_tab, bg="lightblue")
table_frame = tk.Frame(med_tab, bg="lightgreen")
filter_frame.pack(fill="both", expand=True)
table_frame.pack(fill="both", expand=True)


filter_frame.columnconfigure(0, weight=1)
filter_frame.columnconfigure(1, weight=1)
filter_frame.columnconfigure(2, weight=1)
filter_frame.rowconfigure(1, weight=1)
filter_column_val=tk.StringVar()
filter_column = ttk.Combobox(filter_frame, textvariable=filter_column_val,values=("Medicament", "Description", "Prix", "Categorie", "Fournisseur", "Quantité", "Ordonnance ou Pas"))
filter_column_val.set("Medicament")
filter_column.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

filter_condition_val=tk.StringVar()
filter_condition= ttk.Combobox(filter_frame, textvariable=filter_condition_val,values=("Contient", "=", "<", ">"))
filter_condition_val.set("Contient")
filter_condition.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

filter_value_val=tk.StringVar()
filter_value = ttk.Entry(filter_frame, textvariable=filter_value_val)
filter_value_val.set("Tappez ici la valeur avec laquelle vous voulez chercher")
filter_value.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

search_button = ttk.Button(filter_frame, text="Rechercher")
search_button.grid(row=1, column=3, sticky="se", pady=10, padx=20)


###### l'ongler d'ajout
notebook.pack(fill="both", expand=True)
root.mainloop()
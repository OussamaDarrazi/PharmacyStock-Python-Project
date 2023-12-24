import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from BaseDesDonnees import BDPharmacy


db = BDPharmacy()
root = tk.Tk()
root.tk.call('source', 'forest-light.tcl') 
style = ttk.Style()
style.theme_use("forest-light")
root.geometry("700x500")
root.title("Gestion de Stock Pharmacie")
notebook = ttk.Notebook(root)
med_tab = ttk.Frame(notebook)
add_tab = ttk.Frame(notebook)
notebook.add(med_tab, text='Accueil')
notebook.add(add_tab, text='Ajouter')

####### l'onglet acceuille
def remplir_tableau():

    query = """SELECT m.Id, m.Nom_Medicament, m.Description, m.Prix, C.Categorie, F.Fournisseur, m.Quantite, m.Ordonnace_ou_Non 
                FROM Medicaments as m
                LEFT JOIN Fournisseurs as F ON m.Fournisseur_Id = F.id
                LEFT JOIN Categories as C ON m.Categorie_ID = C.id
                """
    #la condition
    condition = "WHERE "
    if filter_column_val.get() == "Medicament":
        condition += "m.Nom_Medicament"
    elif filter_column_val.get() == "Description":
        condition += "m.Description"
    elif filter_column_val.get() == "Categorie":
        condition += "C.Categorie"
    elif filter_column_val.get() == "Fournisseur":
        condition += "F.Fournisseur"
    elif filter_column_val.get() == "Quantité":
        condition += "m.Quantite"
    elif filter_column_val.get() == "Ordonnance ou Pas":
        condition += "m.Ordonnace_ou_Non"
    
    if filter_condition_val.get() == "Contient":
        condition+=" LIKE "
    else:
        condition+=" " +filter_condition_val.get() + " "
    if filter_condition_val.get() == "Contient":
        condition+= "'%" + filter_value_val.get() + "%'"
    else:
        condition+= filter_value_val.get()

    if filter_column_val.get() in ("Medicament", "Description", "Categorie", "Fournisseur") and filter_condition_val.get() != "Contient":
        showerror("Erreur", f"{filter_column_val.get()} est une donnée textuelle est ne peux pas être comparée par des operateur algebrique")

    for row in table.get_children():
        table.delete(row)
    query +=condition
    print(query)
    resultat_db = db.executer_requete_select(query)
    for resultat in resultat_db:
        table.insert("", index="end", values=resultat)
    

filter_frame = tk.Frame(med_tab)

filter_frame.pack(fill="both", expand=True)


tk.Label(filter_frame,text="Chercher Les medicaments").grid(row=0, columnspan=3, sticky="w")

filter_frame.columnconfigure(0, weight=1)
filter_frame.columnconfigure(1, weight=1)
filter_frame.columnconfigure(2, weight=1)
filter_frame.rowconfigure(2, weight=1)
filter_column_val=tk.StringVar() #field to filter by
filter_column = ttk.Combobox(filter_frame, textvariable=filter_column_val,values=("Medicament", "Description", "Prix", "Categorie", "Fournisseur", "Quantité", "Ordonnance ou Pas"))
filter_column_val.set("Medicament")
filter_column.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

filter_condition_val=tk.StringVar() #condition operator
filter_condition= ttk.Combobox(filter_frame, textvariable=filter_condition_val,values=("Contient", "=", "<", ">"))
filter_condition_val.set("Contient")
filter_condition.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

filter_value_val=tk.StringVar() ##condition value
filter_value = ttk.Entry(filter_frame, textvariable=filter_value_val)
filter_value_val.set("Tappez ici la valeur avec laquelle vous voulez chercher")
filter_value.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")

search_button = ttk.Button(filter_frame, text="Rechercher", command=remplir_tableau)
search_button.grid(row=2, column=2, sticky="se", pady=10, padx=20)

#################################
table_frame = tk.Frame(med_tab)
table_frame.pack(fill="both", expand=True)
y_table_scroll = tk.Scrollbar(table_frame)
y_table_scroll.pack(side=tk.RIGHT, fill=tk.Y)
x_table_scroll = tk.Scrollbar(table_frame,orient='horizontal')
x_table_scroll.pack(side= tk.BOTTOM,fill=tk.X)

table = ttk.Treeview(table_frame,columns=("ID", "MED", "DESC", "PRIX", "CATEGORIE", "FOURNISSEUR", "QUANTITE", "ORDONNANCE"),show="headings", yscrollcommand=y_table_scroll.set, xscrollcommand =x_table_scroll.set)
table.heading("ID", text="ID")
table.heading("MED", text="MED")
table.heading("DESC", text="DESC")
table.heading("PRIX", text="PRIX")
table.heading("CATEGORIE", text="CATEGORIE")
table.heading("FOURNISSEUR", text="FOURNISSEUR")
table.heading("QUANTITE", text="QUANTITE")
table.heading("ORDONNANCE", text="ORDONNANCE")
table.pack(anchor="s",fill="both")
y_table_scroll.config(command=table.yview)
x_table_scroll.config(command=table.xview)
# data = db.executer_requete_select("""SELECT m.Id, m.Nom_Medicament, m.Description, m.Prix, C.Categorie, F.Fournisseur, m.Quantite, m.Ordonnace_ou_Non 
#                                   FROM Medicaments as m
#                                   LEFT JOIN Fournisseurs as F ON m.Fournisseur_Id = F.id
#                                   LEFT JOIN Categories as C ON m.Categorie_ID = C.id
#                                    """)

# for row in data:
#     table.insert(parent="", index=row[0], values=row)
###### l'ongler d'ajout
notebook.pack(fill="both", expand=True)
root.mainloop()
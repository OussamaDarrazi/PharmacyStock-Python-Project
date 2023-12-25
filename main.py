import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog
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
    elif filter_column_val.get() == "Prix":
        condition += "m.Prix"
    elif filter_column_val.get() == "Fournisseur":
        condition += "F.Fournisseur"
    elif filter_column_val.get() == "Quantité":
        condition += "m.Quantite"
    elif filter_column_val.get() == "Ordonnance ou Pas":
        condition += "m.Ordonnace_ou_Non"
    #WHERE F.Fournisseur
    if filter_condition_val.get() == "Contient":
        condition+=" LIKE "
    else:
        condition+=" " +filter_condition_val.get() + " "

    if filter_condition_val.get() == "Contient":
        condition+= "'%" + filter_value_val.get() + "%'"
    else:
        condition+= filter_value_val.get()

    if filter_column_val.get() in ("Medicament", "Description", "Categorie", "Fournisseur"):
        if filter_condition_val.get() != "Contient":
            showerror("Erreur", f"{filter_column_val.get()} est une donnée textuelle est ne peux pas être comparée par des operateurs algebriques")
    elif filter_column_val.get() not in ("Medicament", "Description", "Categorie", "Fournisseur"):
        if filter_condition_val.get() == "Contient":
            showerror("Erreur", f"{filter_column_val.get()} est une donnée numerique est ne peux être comparée que par des operateurs algebriques")
        if not filter_value_val.get().isnumeric():
            showerror("Erreur", f"{filter_column_val.get()} est une donnée numerique est ne peux être comparée qu'à des valeurs numeriques")
        

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
table_to_insert = tk.StringVar()
def ajouter_depuis_csv():
    file_path = filedialog.askopenfilename()
    if file_path:
        db.inserer_medicament_csv(file_path)
        showinfo(f"Tous les données de {file_path} sont inserées!")

add_tab.rowconfigure(0, weight=1)
add_tab.rowconfigure(2, weight=1)
add_tab.columnconfigure(0, weight=1)
add_form = tk.Frame(add_tab)
add_file = tk.Frame(add_tab)
add_form.grid(row=0, column=0, sticky="nsew")
tk.Label(add_tab, text="------------------ OU -------------------").grid(row=1, column=0, sticky="nsew")
add_file.grid(row=2, column=0, sticky="nsew")





#TODO: HANDLE FORM DATA 
#form elements
add_form.columnconfigure(0, weight=1)
add_form.columnconfigure(1, weight=1)
add_form.columnconfigure(2, weight=1)
# medicament  ENTRY
med_VAR=tk.StringVar()
form_medicament = ttk.Entry(add_form,textvariable=med_VAR)
med_VAR.set('nom')
form_medicament.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
# description ENTRY
des_var=tk.StringVar()
form_description = ttk.Entry(add_form,textvariable=des_var)
des_var.set('description')
form_description.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
# prix ENTRY
prix_var=tk.StringVar()
form_prix = ttk.Entry(add_form,textvariable=prix_var)
prix_var.set('prix')
form_prix.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
# category combobox
categ_var=tk.StringVar()
rows_cate=db.executer_requete_select("select Categorie from Categories order by Categorie")
liste_cat=[]
for row in rows_cate :
    liste_cat.append(row[0])
form_category = ttk.Combobox(add_form,textvariable=categ_var,values=liste_cat)
categ_var.set(liste_cat[0])
form_category.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
# fournisseur combobox
fourn_var=tk.StringVar()
rows_four=db.executer_requete_select("select Fournisseur from Fournisseurs order by Fournisseur")
liste_four=[]
for row in rows_four :
    liste_four.append(row[0])
form_fournisseur = ttk.Combobox(add_form,textvariable=fourn_var, values=liste_four)
fourn_var.set(liste_four[0])
form_fournisseur.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
# quantité entry
quantity_var=tk.StringVar()
form_quantite = ttk.Entry(add_form,textvariable=quantity_var)
quantity_var.set('quantite')
form_quantite.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
# ordonance ou non combobox
ordo_var=tk.StringVar()
form_ordonnance = ttk.Combobox(add_form, values=("Oui", "Non"),textvariable=ordo_var)
ordo_var.set('ordonnance')
form_ordonnance.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
#bouton confirmation :
def add_to_db():
    fourni_id=db._cursor.execute('select id from Fournisseurs where  Fournisseur = (?)',(fourn_var.get(),)).fetchone()[0]
    categ_id=db._cursor.execute('select id from Categories where  Categorie = (?)',(categ_var.get(),)).fetchone()[0]
    ord_ind=1 if ordo_var.get()=='Oui' else 0
    if not prix_var.get().isnumeric() or not quantity_var.get().isnumeric():
        showerror("Error", "Prix et Quantité sont des données numeriques")
    elif len(db.executer_requete_select(f"select * from Medicaments where Nom_medicament = '{med_VAR.get()}'")) >0:
        if not askyesno("Warning", f"{med_VAR.get()} est deja dans la base de données, Voulez vous l'ajouter?"):
            showinfo("Info", f"{med_VAR.get()} n'a pas été ajouté")
        else:
            db.inserer_medicament(med_VAR.get(),des_var.get(),prix_var.get(),categ_id,fourni_id,quantity_var.get(),ord_ind)
            showinfo("Info", f"{med_VAR.get()} a été ajouté")
    else:
        db.inserer_medicament(med_VAR.get(),des_var.get(),prix_var.get(),categ_id,fourni_id,quantity_var.get(),ord_ind)
        showinfo("Info", f"{med_VAR.get()} a été ajouté")
confirmation = ttk.Button(add_form, text='Ajouter', command=add_to_db)
confirmation.grid(row=2,column=2,padx=10,pady=10,sticky='se')
###bouton pour ajouter depuis un fichier csv 
csv_upload_button = ttk.Button(add_file,text="Ajouter depuis un fichier CSV", command=ajouter_depuis_csv)
csv_upload_button.pack(side=tk.TOP, anchor=tk.CENTER)
notebook.pack(fill="both", expand=True)
root.mainloop()
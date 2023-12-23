import csv
import sqlite3

class BDPharmacy:
    _instance = None

    def __init__(self):
        self._connection = sqlite3.connect("pharmacydb.db")
        self._cursor = self._connection.cursor()
        self._cursor.execute("""Create Table if not exists Fournisseurs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Fournisseur TEXT NOT NULL,
                            Contact_Num TEXT
        )""")
        self._cursor.execute("""Create Table if not exists Categories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Categorie TEXT NOT NULL
        )""")
        self._cursor.execute("""Create Table if not exists Medicaments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Nom_Medicament TEXT NOT NULL,
                            Description TEXT,
                            Prix FLOAT NOT NULL,
                            Categorie_Id INTEGER NOT NULL,
                            Fournisseur_Id INTEGER NOT NULL,
                            Quantite INTEGER NOT NULL DEFAULT 0,
                            Ordonnace_ou_Non INTEGER NOT NULL,
                            FOREIGN KEY (categorie_id) REFERENCES Categories (id),
                            FOREIGN KEY (fournisseur_id) REFERENCES Fournisseurs (id)
        )""")


    def executer_requete_select(self, query: str):
        """
        executer une requete select generique
        """
        self._cursor.execute(query)
        resultat = self._cursor.fetchall()
        return resultat
    
    def inserer_medicament(self, nom_medicament, description, prix, catergorie_id, fournisseur_id, qte, ordonnance_ou_non):
        """
        Inserer un medicament
        Usage:
            db.inserer_medicament("Dolipran", "kidawi kolchi", 10.34, 0, 0, 12, 0)
        """
        self._cursor.execute("INSERT INTO Medicaments (Nom_Medicament, Description, Prix, Categorie_Id, Fournisseur_Id, Quantite, Ordonnace_ou_Non) VALUES (?,?,?,?,?,?,?)", (nom_medicament, description, prix, catergorie_id, fournisseur_id, qte, ordonnance_ou_non))
        self._connection.commit()


    def inserer_medicament_csv(self, csv_file):
        """
        Inserer un medicament depuis un fichier csv

        """
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)

            for row in csv_reader:
                nom_medicament, description, prix, categorie_id, fournisseur_id, qte, ordonnance_ou_non = row
                self.inserer_medicament(nom_medicament, description, prix, categorie_id, fournisseur_id, qte, ordonnance_ou_non)

    
db = BDPharmacy()

db.inserer_medicament("Dolipran", "kidawi kolchi", 10.34, 0, 0, 12, 0)

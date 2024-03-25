import tkinter as tk
import sqlite3

class Supervision_Effectifs:
    def __init__(self, root):
        self.root = root
        self.root.title("Supervision des Effectifs")

        # Ajuster la taille des cadres pour remplir la fenêtre entière
        self.root.grid_rowconfigure(0, weight=1)  # Ajuster la ligne principale
        self.root.grid_columnconfigure(0, weight=1)  # Ajuster la colonne principale

        # Utiliser sticky pour étirer le cadre et le canvas dans toutes les directions
        canvas.grid(row=0, column=0, sticky="nsew")
        self.calendar_frame.grid(row=0, column=0, sticky="nsew")

        
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect("data\databases\main_data.db")
        self.cursor = self.conn.cursor()

        # Création de la table 'effectifs' si elle n'existe pas
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS effectifs
                                (id INTEGER PRIMARY KEY, nom TEXT, prenom TEXT, id_grade INTEGER, FOREIGN KEY(id_grade) REFERENCES grades(id))''')

        # Création de la table 'grades' si elle n'existe pas
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS grades
                                (id INTEGER PRIMARY KEY, nom TEXT)''')

        # Configuration de la liste des grades
        self.grades = self.get_grades()

        # Création des widgets
        self.create_widgets()

    def get_grades(self):
        self.cursor.execute("SELECT * FROM grades")
        return self.cursor.fetchall()

    def create_widgets(self):
        # Frame pour les boutons d'actions
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        # Boutons d'actions
        add_button = tk.Button(action_frame, text="Ajouter", command=self.add_effectif)
        add_button.grid(row=0, column=0, padx=10)

        remove_button = tk.Button(action_frame, text="Retirer", command=self.remove_effectif)
        remove_button.grid(row=0, column=1, padx=10)

        modify_button = tk.Button(action_frame, text="Modifier", command=self.modify_effectif)
        modify_button.grid(row=0, column=2, padx=10)

        # Liste des effectifs
        self.effectifs_listbox = tk.Listbox(self.root, width=50)
        self.effectifs_listbox.pack(padx=10, pady=5)

        # Remplir la liste des effectifs
        self.fill_effectifs_listbox()

    def fill_effectifs_listbox(self):
        # Effacer la liste actuelle
        self.effectifs_listbox.delete(0, tk.END)

        # Récupérer les effectifs depuis la base de données
        self.cursor.execute("SELECT idUnite, grades.nom, effectifs.nom, prenom, telephone, mail FROM effectifs, grades WHERE effectifs.id_grade = grades.rang ORDER BY id_grade")
        effectifs = self.cursor.fetchall()

        # Remplir la liste avec les informations des effectifs
        for identifiant, grade, nom, prenom, tel, mail in effectifs:
            self.effectifs_listbox.insert(tk.END, f"[{grade}] - {nom} {prenom} | Id : {identifiant} | Tel : {tel} | E-Mail : {mail}")

            
        
        

    def add_effectif(self):
        # TODO: Afficher une fenêtre de saisie pour ajouter un effectif
        pass

    def remove_effectif(self):
        # Vérifier si un effectif est sélectionné
        if self.effectifs_listbox.curselection():
            pass

    def modify_effectif(self):
        # Vérifier si un effectif est sélectionné
        if self.effectifs_listbox.curselection():
            # TODO: Afficher une fenêtre de saisie pour modifier les informations de l'effectif
            pass

root = tk.Tk()
app = Supervision_Effectifs(root)
root.mainloop()

import tkinter as tk
from tkinter import ttk
from calendar import monthcalendar

class PompiersEmploiDuTempsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emploi du Temps Pompiers")

        self.current_month = 1
        self.current_year = 2024
        self.create_widgets()

    def create_widgets(self):
        # Création de l'étiquette du titre
        self.label = tk.Label(self.root, text="Emploi du Temps Pompiers", font=('Helvetica', 16))
        self.label.grid(row=0, column=0, columnspan=7)

        # Création du tableau (Treeview) pour afficher l'emploi du temps
        self.tree = ttk.Treeview(self.root, columns=('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'))
        self.tree.grid(row=1, column=0, columnspan=7, padx=10, pady=10)

        # Configuration des en-têtes du tableau
        self.tree.heading('#0', text='Semaine/Mois', anchor='w')
        for day in ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'):
            self.tree.heading(day, text=day)

        # Mise à jour du calendrier initial
        self.update_calendar()

        # Bouton pour afficher par semaine
        self.show_week_button = tk.Button(self.root, text="Afficher par Semaine", command=self.show_week)
        self.show_week_button.grid(row=2, column=0, pady=10)

        # Bouton pour afficher par mois
        self.show_month_button = tk.Button(self.root, text="Afficher par Mois", command=self.show_month)
        self.show_month_button.grid(row=2, column=1, pady=10)

    def update_calendar(self):
        # Suppression des anciennes données du tableau
        self.tree.delete(*self.tree.get_children())
        # Obtention des semaines du mois en cours
        weeks = monthcalendar(self.current_year, self.current_month)

        # Ajout des données au tableau
        for week_num, week in enumerate(weeks, start=1):
            week_str = f"Semaine {week_num}"
            values = [week_str] + [str(day) if day != 0 else '' for day in week]
            self.tree.insert('', 'end', values=values)

    def show_week(self):
        # Changement des en-têtes pour afficher par semaine
        self.tree["column"] = ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche')
        self.update_calendar()

    def show_month(self):
        # Changement des en-têtes pour afficher par mois
        self.tree["column"] = ('Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim')
        self.update_calendar()

# Initialisation de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = PompiersEmploiDuTempsApp(root)
    root.mainloop()

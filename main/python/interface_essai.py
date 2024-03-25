import tkinter as tk
from tkinter import ttk
from calendar import monthcalendar

def update_calendar():
    # Suppression des anciennes données du tableau
    tree.delete(*tree.get_children())
    # Obtention des semaines du mois en cours
    weeks = monthcalendar(current_year, current_month)

    # Ajout des données au tableau
    for week_num, week in enumerate(weeks, start=1):
        week_str = f"Semaine {week_num}"
        for day_index, day in enumerate(week):
            day_str = f"{day}" if day != 0 else ''
            tree.insert('', 'end', values=(week_str, jours[day_index], day_str))

def show_week():
    # Changement des en-têtes pour afficher par semaine
    tree["columns"] = ('Semaine', 'Jour', 'Jour de la semaine', 'Jour du mois')
    tree.heading('#2', text='Jour de la semaine')
    tree.heading('#3', text='Jour du mois')
    update_calendar()

def show_month():
    # Changement des en-têtes pour afficher par mois
    tree["columns"] = ('Semaine', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche')
    tree.heading('#2', text='Lundi')
    tree.heading('#3', text='Mardi')
    tree.heading('#4', text='Mercredi')
    tree.heading('#5', text='Jeudi')
    tree.heading('#6', text='Vendredi')
    tree.heading('#7', text='Samedi')
    tree.heading('#8', text='Dimanche')
    update_calendar()

# Initialisation des variables
current_month = 1
current_year = 2024
jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

# Création de la fenêtre principale
root = tk.Tk()
root.title("Emploi du Temps Pompiers")

# Création du tableau (Treeview) pour afficher l'emploi du temps
tree = ttk.Treeview(root, columns=('Semaine', 'Jour', 'Jour de la semaine', 'Jour du mois'))
tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Configuration des en-têtes du tableau
tree.heading('#0', text='Semaine/Mois', anchor='w')
tree.heading('#1', text='Jour', anchor='w')
tree.heading('#2', text='Jour de la semaine', anchor='w')
tree.heading('#3', text='Jour du mois', anchor='w')

# Mise à jour du calendrier initial
update_calendar()

# Bouton pour afficher par semaine
show_week_button = tk.Button(root, text="Afficher par Semaine", command=show_week)
show_week_button.grid(row=1, column=0, pady=10)

# Bouton pour afficher par mois
show_month_button = tk.Button(root, text="Afficher par Mois", command=show_month)
show_month_button.grid(row=1, column=1, pady=10)

# Lancement de la boucle principale
root.mainloop()

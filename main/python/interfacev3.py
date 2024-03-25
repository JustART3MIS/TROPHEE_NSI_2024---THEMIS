import tkinter as tk
from tkinter import messagebox
from interfacev2 import CalendarApp

class Accueil(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion de Planning des Pompiers")
        self.geometry("400x300")

        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(pady=10)

        self.accueil_label = tk.Label(self, text="Bienvenue dans l'application de gestion de planning des pompiers", font=('Helvetica', 14))
        self.accueil_label.pack(pady=20)

        self.button_planning = tk.Button(self.menu_frame, text="Afficher Planning", command=self.afficher_planning)
        self.button_planning.grid(row=0, column=0, padx=10)

        self.button_dates = tk.Button(self.menu_frame, text="Dates Importantes", command=self.afficher_dates)
        self.button_dates.grid(row=0, column=1, padx=10)

        self.button_quitter = tk.Button(self.menu_frame, text="Quitter", command=self.quitter_application)
        self.button_quitter.grid(row=0, column=2, padx=10)

    def afficher_planning(self):
        # Fonction pour afficher la fenêtre du planning
        planning = CalendarApp
        planning.grab_set()

    def afficher_dates(self):
        # Fonction pour afficher la fenêtre des dates importantes
        messagebox.showinfo("Dates Importantes", "Fenêtre des dates importantes")

    def quitter_application(self):
        # Fonction pour quitter l'application
        if messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir quitter l'application ?"):
            self.destroy()

if __name__ == "__main__":
    app = Accueil()
    app.mainloop()


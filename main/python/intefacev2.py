try :
    import os, time
    import tkinter as tk
    from tkinter import messagebox
    import datetime, sqlite3, locale, calendar

except ImportError:
    
    os.system("pip install sqlite==3.45.2")
    time.sleep(1.5)
    os.system("pip install datetime")
    time.sleep(1.5)
    os.system("pip install tkinter==3.12.2")
    time.sleep(1.5)
    os.system("pip install locale==3.10.2")
    time.sleep(1.5)
    os.system("pip install calendar")
       
    if messagebox.showinfo("Installation des bibliothèques", """Votre appareil ne possédait pas les bibliothèques nécessaires au fonctionnement de ce logiciel. Nous vous les avons donc installées avec succès !""", ):
        exec(open(r"interfacev2").read())

# Set the locale to French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')



class CalendarApp(tk.Toplevel):
    def __init__(self, parent):
        
        self.parent = parent
        super().__init__(parent)
        self.title("Thémis - Gestion de l'Astreinte")

        # Obtenir la taille de l'écran
        self.screen_width = parent.winfo_screenwidth()
        self.screen_height = parent.winfo_screenheight()
        
        # Taille de la fenêtre
        window_width = int(self.screen_width * 0.8)  # 80% de la largeur de l'écran
        window_height = int(self.screen_height * 0.8)  # 80% de la hauteur de l'écran
        
        # Centrer la fenêtre sur l'écran
        x_position = (self.screen_width - window_width) // 2
        y_position = (self.screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        self.current_year = tk.IntVar()
        self.current_month = tk.IntVar()

        # Initialize current year and month
        self.current_year.set(2024)
        self.current_month.set(3)

        self.month_label = tk.Label(self, text="", font=("Arial", 24, "bold"))
        self.month_label.grid(row=0, column=0, columnspan=7)

        # Create a canvas to contain the calendar frame
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=1, column=0, columnspan=7, sticky="nsew")

        # Add a frame inside the canvas to hold the calendar
        self.calendar_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.calendar_frame, anchor="nw")

        # Initialize days_labels list
        self.days_labels = []

        self.create_calendar()

        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect("data\databases\main_data.db")
        self.cursor = self.conn.cursor()

        # Création de la table 'affectations' si elle n'existe pas
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS affectations
                                (date_garde TEXT, id_pompier INTEGER)''')

        self.gardes_info = [None] * 31  # Initialisation de la liste des gardes avec 31 éléments
        self.update_calendar()


    def create_calendar(self):
        # Create a grid of buttons for dates
        for row in range(5):  # You can adjust the number of rows as needed
            for col in range(7):  # 7 columns for the days of the week
                button = tk.Button(self.calendar_frame, text="", font=("Arial", 16), padx=30, pady=20, relief="ridge")
                button.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)  # Add padding and make buttons expand to fill cell
                self.days_labels.append(button)

        # Previous month button
        prev_button = tk.Button(self, text="Mois précédent", command=self.prev_month)
        prev_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Next month button
        next_button = tk.Button(self, text="Mois suivant", command=self.next_month)
        next_button.grid(row=2, column=5, columnspan=2, pady=10)

        # Configure canvas scrolling
        self.grid_rowconfigure(1, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)   

    def save_info(self, day, id_pompier, popup):
        # Récupérer les informations du pompier sélectionné depuis la base de données
        self.cursor.execute(f"SELECT grades.nom, effectifs.nom, prenom FROM effectifs, grades WHERE effectifs.id_grade = grades.rang AND idUnite = {id_pompier}")
        pompier_info = self.cursor.fetchone()

        # Insérer les informations de garde dans la table 'affectations'
        date_garde = f"{self.current_year.get()}-{self.current_month.get():02d}-{day:02d}"
        self.cursor.execute("INSERT INTO affectations (date_garde, id_pompier) VALUES (?, ?)", (date_garde, id_pompier))
        self.conn.commit()

        self.days_labels[(day-1)*2].config(text=f"{day}\n{pompier_info[1]} {pompier_info[2]}\n{pompier_info[0]}", bg="lightgreen")
        popup.destroy()

    def prev_month(self):
        self.current_month.set(self.current_month.get() - 1)
        if self.current_month.get() == 0:
            self.current_month.set(12)
            self.current_year.set(self.current_year.get() - 1)
        self.update_calendar()

    def next_month(self):
        self.current_month.set(self.current_month.get() + 1)
        if self.current_month.get() == 13:
            self.current_month.set(1)
            self.current_year.set(self.current_year.get() + 1)
        self.update_calendar()

    def show_popup(self, day):
        popup = tk.Toplevel(self.parent)
        popup.title(f"Pompier de garde le {day} {calendar.month_name[self.current_month.get()]}")
        
        # Centrer la fenêtre contextuelle sur la fenêtre principale
        popup_width = 400
        popup_height = 200
        x_position = (self.parent.winfo_width() - popup_width) // 2 + self.parent.winfo_x()
        y_position = (self.parent.winfo_height() - popup_height) // 2 + self.parent.winfo_y()
        
        
        popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")
        
        label = tk.Label(popup, text="Sélectionnez le pompier :")
        label.pack(pady=5)
        
        # Récupérer les données des pompiers depuis la base de données
        self.cursor.execute("SELECT grades.nom, effectifs.nom, prenom, idUnite FROM effectifs, grades WHERE effectifs.id_grade = grades.rang ORDER BY id_grade")
        pompiers = self.cursor.fetchall()

        if pompiers:  # Vérifier si des pompiers ont été récupérés
            pompier_var = tk.StringVar(popup)
            pompier_var.set("Sélectionnez un pompier")  # Sélection par défaut

            pompier_menu = tk.OptionMenu(popup, pompier_var, *[f"[{grade}] - {nom} {prenom} | {id_unite}" for grade, nom, prenom, id_unite in pompiers])
            pompier_menu.pack(pady=5)

            save_button = tk.Button(popup, text="Enregistrer", command=lambda: self.save_info(day, pompier_var.get().split("| ")[1], popup))
            save_button.pack(pady=5)
        else:
            error_label = tk.Label(popup, text="Aucun pompier disponible.")
            error_label.pack(pady=5)

    def update_calendar(self):
        month_name = calendar.month_name[self.current_month.get()].capitalize()
        self.month_label.config(text=f"{month_name} {self.current_year.get()}")

        days_in_month = calendar.monthrange(self.current_year.get(), self.current_month.get())[1]

        for label in self.days_labels:
            label.config(text="", bg="white")  # Réinitialiser la couleur de fond à blanc
            label.unbind("<Button-1>")  # Unbind any previous event bindings

        # Récupérer les dates de garde de ce mois
        self.cursor.execute("SELECT date_garde, id_pompier FROM gardes WHERE strftime('%Y-%m', date_garde) = ?", (f"{self.current_year.get()}-{self.current_month.get():02d}",))
        gardes = self.cursor.fetchall()
    
        for i in range(1, days_in_month + 1):
            day_label = self.days_labels[i - 1]
            day_label.config(text=str(i))

            # Vérifier si le jour est une date de garde et marquer dans le calendrier
            for garde in gardes:
                garde_date = datetime.datetime.strptime(garde[0], '%Y-%m-%d').date()  # Convertir la date de garde en objet datetime.date
                if garde_date.day == i:
                    day_label.config(bg="lightgreen")

            # Rétablir les liens d'événement pour chaque case
            day_label.bind("<Button-1>", lambda event, day=i: self.show_popup(day))
            
            # Réinitialiser les couleurs de fond des cases et rétablir les informations de garde
            for i in range(1, days_in_month + 1):
                day_label = self.days_labels[i - 1]

                if len(str(i)) == 1:
                    day_label.config(text="0" + str(i), bg="white")
                else:
                    day_label.config(text=str(i), bg="white")

                # Rétablir les informations de garde pour ce jour
                if self.gardes_info[i - 1] is not None:
                    day_label.config(text=self.gardes_info[i - 1], bg="lightgreen")

                # Rétablir les liens d'événement pour chaque case
                day_label.bind("<Button-1>", lambda event, day=i: self.show_popup(day))

    def quitter_application(self):
        # Fonction pour quitter l'application
        if messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir quitter l'application ?"):
            self.destroy()

class Accueil(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Thémis - Accueil")
        self.current_screen = None

         # Définir le Logo
        self.logo = tk.PhotoImage(file = 'data/images/logo.ico')
        self.iconphoto(True, self.logo)
        
        # Obtenir la taille de l'écran
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # Taille de la fenêtre
        window_width = int(self.screen_width * 0.8)  # 80% de la largeur de l'écran
        window_height = int(self.screen_height * 0.8)  # 80% de la hauteur de l'écran
        
        # Centrer la fenêtre sur l'écran
        x_position = (self.screen_width - window_width) // 2
        y_position = (self.screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.menu_frame = tk.Frame(self)
        self.menu_frame.grid()

        self.accueil_label = tk.Label(self, text="Bienvenue dans l'application de gestion de planning des pompiers", font=('Helvetica', 14))
        self.accueil_label.grid()
        self.button_planning = tk.Button(self.menu_frame, text="Afficher Planning", command=self.afficher_planning)
        self.button_planning.grid(row=0, column=0, padx=10)

        self.button_dates = tk.Button(self.menu_frame, text="Dates Importantes", command=self.afficher_unites)
        self.button_dates.grid(row=0, column=1, padx=10)

        self.button_quitter = tk.Button(self.menu_frame, text="Quitter", command=self.quitter_application)
        self.button_quitter.grid(row=0, column=2, padx=10)

    def afficher_planning(self):
        # Afficher l'écran du planning
        if self.current_screen:
            self.current_screen.destroy()  # Détruire l'écran actuellement affiché s'il existe

        self.current_screen = CalendarApp(self)  # Créer une instance de CalendarApp
        self.current_screen.grid(row=1, column=0, sticky="nsew")  # Afficher l'écran du planning

        # Ajouter un bouton pour revenir à l'accueil
        back_button = tk.Button(self.current_screen, text="Retour à l'accueil", command=self.retour_accueil)
        back_button.grid(row=2, column=0, columnspan=7, pady=10)

    def retour_accueil(self):
        # Afficher à nouveau l'écran d'accueil
        if self.current_screen:
            self.current_screen.destroy()  # Détruire l'écran du planning
        self.current_screen = None  # Réinitialiser l'écran actuellement affiché

    def afficher_unites(self):
        pass
    #    # Afficher la fenêtre des unités
    #    if self.current_screen:
    #        self.current_screen.destroy()
    #    
    #    self.current_screen = 

    def quitter_application(self):
        # Fonction pour quitter l'application
        if messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir quitter l'application ?"):
            self.destroy()



root = Accueil()
root.mainloop()
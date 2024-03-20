import tkinter as tk
import calendar, datetime, sqlite3, locale

# Set the locale to French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendrier Pompier")
        
        # Obtenir la taille de l'écran
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        
        # Taille de la fenêtre
        window_width = int(self.screen_width * 0.8)  # 80% de la largeur de l'écran
        window_height = int(self.screen_height * 0.8)  # 80% de la hauteur de l'écran
        
        # Centrer la fenêtre sur l'écran
        x_position = (self.screen_width - window_width) // 2
        y_position = (self.screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        self.current_year = tk.IntVar()
        self.current_month = tk.IntVar()

        # Initialize current year and month
        self.current_year.set(2024)
        self.current_month.set(3)

        self.month_label = tk.Label(self.root, text="", font=("Arial", 24, "bold"))
        self.month_label.grid(row=0, column=0, columnspan=7)

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.grid(row=1, column=0, columnspan=7)

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
        self.days_labels = []
        for i in range(1, 32):
            day_label = tk.Label(self.calendar_frame, text="", font=("Arial", 16), padx=20, pady=10, relief="ridge")
            day_label.grid(row=(i-1)//7, column=(i-1)%7)
            self.days_labels.append(day_label)

        # Previous month button
        prev_button = tk.Button(self.root, text="Mois précédent", command=self.prev_month)
        prev_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Next month button
        next_button = tk.Button(self.root, text="Mois suivant", command=self.next_month)
        next_button.grid(row=2, column=5, columnspan=2, pady=10)

    def save_info(self, day, id_pompier, popup):
        # Récupérer les informations du pompier sélectionné depuis la base de données
        self.cursor.execute(f"SELECT grades.nom, effectifs.nom, prenom FROM effectifs, grades WHERE effectifs.id_grade = grades.rang AND idUnite = {id_pompier}")
        pompier_info = self.cursor.fetchone()

        # Insérer les informations de garde dans la table 'affectations'
        date_garde = f"{self.current_year.get()}-{self.current_month.get():02d}-{day:02d}"
        self.cursor.execute("INSERT INTO affectations (date_garde, id_pompier) VALUES (?, ?)", (date_garde, id_pompier))
        self.conn.commit()

        self.days_labels[day-1].config(text=f"{day}\n{pompier_info[1]} {pompier_info[2]}\n{pompier_info[0]}", bg="lightgreen")
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
        popup = tk.Toplevel(self.root)
        popup.title(f"Pompier de garde le {day} {calendar.month_name[self.current_month.get()]}")
        
        # Centrer la fenêtre contextuelle sur la fenêtre principale
        popup_width = 400
        popup_height = 200
        x_position = (self.root.winfo_width() - popup_width) // 2 + self.root.winfo_x()
        y_position = (self.root.winfo_height() - popup_height) // 2 + self.root.winfo_y()
        
        popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")
        
        label = tk.Label(popup, text="Sélectionnez le pompier :")
        label.pack(pady=5)
        
        # Récupérer les données des pompiers depuis la base de données
        self.cursor.execute("SELECT grades.nom, effectifs.nom, prenom, idUnite FROM effectifs, grades WHERE effectifs.id_grade = grades.rang")
        pompiers = self.cursor.fetchall()

        pompier_var = tk.StringVar(popup)
        pompier_var.set("Sélectionnez un pompier")  # Sélection par défaut

        pompier_menu = tk.OptionMenu(popup, pompier_var, *[f"[{grade}] - {nom} {prenom} | {id_unite}" for grade, nom, prenom, id_unite in pompiers])
        pompier_menu.pack(pady=5)

        save_button = tk.Button(popup, text="Enregistrer", command=lambda: self.save_info(day, pompier_var.get().split("| ")[1], popup))
        save_button.pack(pady=5)
    
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
                day_label.config(text=str(i), bg="white")

                # Rétablir les informations de garde pour ce jour
                if self.gardes_info[i - 1] is not None:
                    day_label.config(text=self.gardes_info[i - 1], bg="lightgreen")

                # Rétablir les liens d'événement pour chaque case
                day_label.bind("<Button-1>", lambda event, day=i: self.show_popup(day))


root = tk.Tk()
app = CalendarApp(root)
root.mainloop()

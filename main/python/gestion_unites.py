            ##########################################################################
            #      __  __  __           _   _         _____          _       __      #
            #     / / |  \/  |         | | (_)       / ____|        | |      \ \     #
            #    / /  | \  / |_   _ ___| |_ _  ___  | |     ___   __| | ___   \ \    #
            #   < <   | |\/| | | | / __| __| |/ __| | |    / _ \ / _` |/ _ \   > >   #
            #    \ \  | |  | | |_| \__ \ |_| | (__  | |___| (_) | (_| |  __/  / /    #
            #     \_\ |_|  |_|\__, |___/\__|_|\___|  \_____\___/ \__,_|\___| /_/     #
            #                  __/ |                                                 #
            #                 |___/                                                  #
            ##########################################################################
        ################################################################################
        #  _____                                          _   _       _   _ _ _        #
        # |  __ \                                ___     | \ | |     (_) (_) | |       #
        # | |__) |___  _ __ ___   __ _ _ __     ( _ )    |  \| | __ _  ___ | | | ___   #
        # |  _  // _ \| '_ ` _ \ / _` | '_ \    / _ \/\  | . ` |/ _` |/ _ \| | |/ _ \  #
        # | | \ \ (_) | | | | | | (_| | | | |  | (_>  <  | |\  | (_| |  __/| | |  __/  #
        # |_|  \_\___/|_| |_| |_|\__,_|_| |_|   \___/\/  |_| \_|\__,_|\___||_|_|\___|  #
        #                                                                              #
        ################################################################################         

#########################
###### IMPORTATIONS #####
#########################

import sqlite3 as sql
from tabulate import tabulate

############################################
###### CONNEXION A LA BASE DE DONNEES ######
############################################

db = sql.connect("main\data\databases\main_data.db")

cur = db.cursor()

#####################################
##### DEFINITION DES FONCTIONS ######
#####################################

def voir_effectifs():
    cur.execute("SELECT * FROM effectifs")
    effectifs = cur.fetchall()

    # Convertir les tuples en listes
    for index in range(len(effectifs)):
        nouvelle_liste = []

        for contenu in effectifs[index]:
            nouvelle_liste.append(contenu)

        effectifs[index] = nouvelle_liste

    # Récupération de tous les grades dans l'ordre dans lequel ils apparaissent
    ordre_grades = []
    for index_grade in range(len(effectifs)):
        ordre_grades.append(effectifs[index_grade][3])

    # Rajout du nom du grade en plus de son id
    for ref_grade in range(len(ordre_grades)):
        # Récupération des 
        cur.execute(f"SELECT nom FROM grades WHERE rang = {ordre_grades[ref_grade]}")
        grade = cur.fetchone()[0]
        ordre_grades[ref_grade] = f"{ordre_grades[ref_grade]} ({grade})"
        effectifs[ref_grade][3] = ordre_grades[ref_grade]


    headers = ["ID", "Nom", "Prénom", "Grade", "Téléphone", "Email"]

    ## Utilisez la fonction tabulate pour afficher le tableau avec les en-têtes
    table = tabulate(effectifs, headers, tablefmt="pretty")

    return table

def ajouter_unite():
    pass

def modifier_unite():
    pass

def retirer_unite():
    pass

def montee_grade(id_unite = None, nb_grades = 1, ):
    if id_unite != None:
        pass

    else:
        pass

def retrogradation():
    pass

print(voir_effectifs())
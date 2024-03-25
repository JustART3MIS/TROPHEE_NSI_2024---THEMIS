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

# Requête pour obtenir les noms de toutes les tables dans la base de données
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Récupérer les résultats de la requête
tables = cur.fetchall()

# Afficher les noms des tables
if tables:
    print("Tables existantes dans la base de données :")
    for table in tables:
        print(table[0])
    print("\n ------------ \n")
else:
    print("Aucune table trouvée dans la base de données.")


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


def ajouter_unite(nom:str, prenom:str, grade:int, telephone:int, mail:str):
    """
    Cree une nouvelle entree dans la table effectifs avec les infos fournies par
    l'appel. L'id de l'unite sera le nombre des id des unites + 1.

    Entrées :
        nom (str): nom de l'unite
        prenom (str): prenom de l'unite
        grade (int): grade de l'unite
        telephone (int): numero de telephone de l'unite
        mail (str): e-mail de l'unite

    Sortie : 
        Aucune
    """
    # On ajoute l'unite dans la base de donnees avec les renseignements
    cur.execute(f"INSERT INTO effectifs VALUES('{nom}', '{prenom}', '{grade}', '{telephone}', '{mail}')")

    db.commit()# Applique les modifications effectuees au fichier main_data.db


def modifier_unite(id_unite:int, nom:str = None, prenom:str = None, telephone:int = None, mail:str = None):
    """
    Modifie une ou plusieurs coordonnées d'une unite

    Entrées :
        id_unite(int): id de l'unite que l'on veut modifier
        nom(str): nom de l'unite
        prenom(str): prenom de l'unite
        telephone(int): numero de telephone de l'unite
        mail(str): adresse e-mail de l'unite

    Sortie : 
        Aucune
    """
    # Si un nom a ete donné, on remplace l'ancien par celui donné par l'utilisateur
    if nom is not None:
        # Mise a jour de la colonne 'nom' de l'unite dans la base de donnees
        cur.execute(f"UPDATE effectifs SET nom = '{nom}' WHERE idUnite = '{id_unite}'")

    # Si un prenom a ete donné, on remplace l'ancien par celui donné par l'utilisateur
    if prenom is not None:
        # Mise a jour de la colonne 'prenom' de l'unite dans la base de donnees
        cur.execute(f"UPDATE effectifs SET prenom = '{prenom}' WHERE idUnite = '{id_unite}'")

    # Si un numero de telephone a ete donné, on remplace l'ancien par celui donné par l'utilisateur
    if telephone is not None:
        # Mise a jour de la colonne 'telephone' de l'unite dans la base de donnees
        cur.execute(f"UPDATE effectifs SET telephone = '{telephone}' WHERE idUnite = '{id_unite}'")

    # Si un e-mail a ete donné, on remplace l'ancien par celui donné par l'utilisateur
    if mail is not None:
        # Mise a jour de la colonne 'mail' de l'unite dans la base de donnees
        cur.execute(f"UPDATE effectifs SET mail = '{mail}' WHERE idUnite = '{id_unite}'")

    db.commit()


def retirer_unite(id_unite):
    """
    Supprime une unite de la base de donnees a partir de son id

    Entrée :
        id_unite(int): id de l'unite que l'ont veut retirer

    Sortie : 
        Aucune
    """
    # On supprime de la base de données l'unite que l'on a sélectionné à partir de son id
    cur.execute(f"DELETE FROM effectifs WHERE idUnite = '{id_unite}'")

    db.commit()


def montee_grade(id_unite, nb_grades = 1):
    """
    Passage d'une unite d'un ou plusieurs grades superieurs

    Entrées :
        id_unite(int): id de l'unite dont on veut monter le grade
        nb_grades(int): nombre entier superieur a 0 correspondant au nombre
        de grades a augmenter 
    
    Sortie :
        Aucune
    """
    # On recupere le numero de grade de l'unite choisie dans une variable grade_actuel
    cur.execute(f"SELECT grade FROM effectifs WHERE idUnite = '{id_unite}'")
    grade_actuel = int(cur.fetchone()[0])

    # On modifie le grade de l'unite en ajoutant au grade actuel le nombre donné en entrée
    cur.execute(f"UPDATE effectifs SET grade = '{grade_actuel+nb_grades}' WHERE idUnite = '{id_unite}'")

    db.commit()


def retrogradation(id_unite, nb_grades = 1):
    """
    Retrogradation d'une unite d'un ou plusieurs grades

    Entrées :
        id_unite(int): id de l'unite dont on veut baisser le grade
        nb_grades(int): nombre entier superieur a 0 correspondant au nombre
        de grades a baisser
    
    Sortie :
        Aucune
    """
    # On récupère le numero de grade de l'unite choisie dans une variable grade_actuel
    cur.execute(f"SELECT grade FROM effectifs WHERE idUnite = '{id_unite}'")
    grade_actuel = int(cur.fetchone()[0])

    # On modifie le grade de l'unite en retranchant le nombre de grades donné en entrée
    cur.execute(f"UPDATE effectifs SET grade = '{grade_actuel-nb_grades}' WHERE idUnite = '{id_unite}'")

    db.commit()


def connexion(identifiant:str = None, mdp:str = None) -> bool:
    """
    Vérifie si l'utilisateur a rentré les bons identifiants lors de sa
    connexion

    Entrées :
        identifiant : nom d'utilisateur rentré par l'utilisateur.
        mdp : mot de passe rentré par l'utilisateur.

    Sortie :
        True si l'utilisateur a bien été authentifié, False sinon.
    """
    if identifiant != None and mdp != None:

        # Selectionne le numero de reference du mot de passe lié a l'identifiant entré
        # Selectionne None si ce n'est lié à aucun compte enregistré
        if identifiant == "" and mdp == "":
            #easter egg
            return None
        cur.execute(f"SELECT mdp_compte FROM effectifs WHERE id_compte = '{identifiant}'")
        
        try:
            #recup le 1er resultat, unpack car (num,)
            (numero_compte, *_) = cur.fetchall()[0]# Stocke le resultat de la selection dans une variable
        except IndexError: # identifiant non trouvé
            numero_compte = None


        if numero_compte != None: # Si le compte existe

            # Selectionne le mot de passe relié a l'identifiant entré
            cur.execute(f"SELECT contenu FROM passwords WHERE id_compte = '{numero_compte}' ")
            bon_mdp = cur.fetchone()[0] # Stocke le bon mot de passe dans une variable

            if mdp == bon_mdp : # Si le mot de passe est le même que celui enregistré dans la base de données
            # Renvoie True si le mot de passe entré par l'utilisateur correspond a celui enregistré dans la database
                return True
            #si connect avec mauvais mdp
            return False
        #si connect avec mauvais id
        return False
    # Si connect with optional arg, ne devrait jamais arrivé
    return False


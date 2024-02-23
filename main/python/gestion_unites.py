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
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

############################################
###### CONNEXION A LA BASE DE DONNEES ######
############################################

db = sql.connect("main\data\databases\main_data.db")

cur = db.cursor()

#####################################
##### DEFINITION DES FONCTIONS ######
#####################################


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
#!/usr/bin/env python3

import math 
import random 
import yaml
import sys
import os


# TODO: charger la configuration depuis 
# un fichier YAML
CONFIG = {
    "tagfile" : "tags.yaml",
    "exoDIR"  : "Exos",
    "catDIR"  : "Catalogue",
    "semDIR"  : "Semaines",
    "fihDIR"  : "Fiches",
    "reqDIR"  : "Request",
    "debug"   : False,
    "log"     : []
        }

def debugInfo (action, description):
    """
        Ajoute l'information au log
        de debug

        action      : string
            nom de l'action entreprise
        description : string
            valeurs des variables et spécificités

        @return : string
    """
    if CONFIG["debug"] == True:
        CONFIG["log"].append ("[INFO ] ({}) : {}".format (action, description))

def debugError (action, description):
    """
        Log l'erreur

        action      : string
            nom de l'action entreprise
        description : string
            valeurs des variables et spécificités

        @return : string
    """
    CONFIG["log"].append ("[ERROR] ({}) : {}".format (action, description))



def openFile (filename):
    """
        Ouvre le fichier en lecture seule

        filename : string
            le chemin du fichier à ouvrir

        @return : string
    """
    debugInfo ("OPENFILE", filename))

    return open (filename, "r")
        

DATABASE = yaml.load (open (CONFIG["tagfile"], "r"))


def fetchExercice (exoID):
    """
        Écrit textuellement 
        le contenu de l'exercice exoID

        exoID : int 
            le numéro de l'exercice

        @return : unit
    """
    debugInfo ("EXOWRITE", "exoID : {}".format (exoID))
    return "".join(openFile ("{}/{}.tex".format (CONFIG["exoDIR"],
        exoID)).readlines ())

def fetchCours (semaine):
    """
        Récupère les questions 
        de cours pour une semaine 
        donnée 
    """
    debugInfo ("COURS", " questions de cours de « {} »".format (semaine))
    with open ("{}/{}.yaml".format (CONFIG["semDIR"], semaine),"r") as f
        return yaml.load (f)



## TYPE REQUEST : STRING DICT
# où les clefs sont exactement les clefs 
# des métadonnées des exercices 

def fetchRequest (reqname):
    """ 
        Charche une requête dans un 
        fichier 
    """
    debugInfo ("LOADREQ", " requête {}".format (reqname))
    with open ("{}/{}.yaml".format (CONFIG["reqDIR"], reqname),"r") as f
        return yaml.load (f)

def saveRequest (reqname, request):
    """
        Enregistre une requête dans 
        un fichier 
    """
    debugInfo ("SAVEREQ", " requête {}".format (reqname))
    with open ("{}/{}".format (CONFIG["reqDIR"], reqname), "w") as f:
        yaml.dump (request, f, default_flow_style=False)

def fetchExercices (request):
    """
        Fait une recherche d'exercices 
        étant donné une requête passée 
        en argument.

        request : <Request> 
            La requête à effectuer sur la DB

        @return : iterator exoID
    """
    debugInfo ("DBREQ", "request : {}".format (request))

    for exoID in DATABASE.keys ():
        if requestValidate (request, exoID):
            yield exoID
    
if __name__ == "__main__":
    # TODO: ici ajouter l'interactivité pour 
    # par exemple tester des requêtes, et 
    # les enregistrer dans des fichiers 
    print ("coucou")

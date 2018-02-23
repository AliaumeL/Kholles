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
    "fihDIR"  : "Fiches",
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
    return "[INFO ] ({}) : {}".format (action, description)

def debugError (action, description):
    """
        Log l'erreur

        action      : string
            nom de l'action entreprise
        description : string
            valeurs des variables et spécificités

        @return : string
    """
    return "[ERROR] ({}) : {}".format (action, description)


def openFile (filename):
    """
        Ouvre le fichier en lecture seule

        filename : string
            le chemin du fichier à ouvrir

        @return : string
    """
    if CONFIG["debug"] == True:
        CONFIG["log"].append (debugInfo ("OPENFILE", filename))

    return open (filename, "r")
        

DATABASE = yaml.load (open (CONFIG["tagfile"], "r"))


def writeExercice (exoID):
    """
        Écrit textuellement 
        le contenu de l'exercice exoID

        exoID : int 
            le numéro de l'exercice

        @return : unit
    """
    print ("".join(openFile ("{}/{}.tex".format (CONFIG["exoDIR"],
        exoID)).readlines ()))


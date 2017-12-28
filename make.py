#!/usr/bin/env python3

import math 
import random 
import yaml
import sys
import os




class Interactive:
    def __init__ (self):
        self.tabs   = 0
        self.debug  = 0
        self.logger = None

    def parseArgs (self):
        pass 

    def log (self, name, desc):
        if self.debug == 3:
            if self.logger == None:
                self.logger = 0 
            else: 
                self.logger += 1
            print ("[{}] {} : {}".format (self.logger,name,desc))
        elif self.debug == 2:
            if self.logger == None:
                self.logger = []

            self.logger.append ((name, desc))
        else:
            pass


    def open (self, f, m):
        self.log ("FILEOPEN", "ouvre le fichier {} en mode {}".format (f,m))
        return open (f,m)
    
    def openExo (self, name):
        return self.open ("Exos/{}.tex".format (name), "r")

    def openCatalogue (self, name):
        return yaml.load (self.open ("Catalogue/{}.yaml".format (name), "r"))

    def openCatalogueTex (self, name):
        return self.open ("Catalogue/{}.tex".format (name), "w")

    def openExercices (self):
        return yaml.load (self.open ("tags.yaml", "r"))

    def openCatalogueTemplate (self):
        return self.open ("Catalogue/template.tex","r")


class Database:
    def __init__ (self):
        self.exercies = None

    def listExercices (self):
        return self.exercices.items ()


#### INTERACTION ####

I = Interactive ()
I.debug = 3
I.parseArgs ()

D = Database ()
D.exercices = I.openExercices ()



def catalogueBuilder (name):
    """ Construit un catalogue des 
        exercices avec des caractéristiques 
        données. Le tout se trouvant 
        dans un fichier `catalogue/name.yaml`
    """
    catadesc = I.openCatalogue (name)
    catalist = []
    
    # TODO: c'est une boucle horrible 
    # qui fait des choses terriblement non 
    # efficaces !
    for ID,exo in D.listExercices ():
        for prop,value in catadesc.items ():
            try:
                testval = exo[prop]
            except KeyError:
                pass

            if isinstance (value, list):
                b = True
                for v in value:
                    if v not in testval:
                        b = False
                if b:
                    catalist.append ((ID,exo))
            elif exo[prop] == value:
                catalist.append ((ID,exo))


    # ÉCRITURE DANS LE FICHIER
    output = I.openCatalogueTex (name)

    template  = I.openCatalogueTemplate ()
    for l in template.readlines ():
        output.write (l) 
    template.close ()
    

    # TODO: trier par catégorie de tags ... !?!
    for (ID,exo) in catalist:
        exoctn = I.openExo (ID)
        output.write ("\\exoID{" + ID + "}\n")
        for l in exoctn.readlines ():
            output.write (l)
        exoctn.close ()


    output.write ("\n\\end{document}")
    output.close ()

    # Compile une ou deux fois pour être sûr 
    os.system ("cd Catalogue && pdflatex {}.tex".format (name)) 
    os.system ("cd Catalogue && pdflatex {}.tex".format (name)) 
    
    # Supprime les fichiers intermédiaires
    os.system ("cd Catalogue && rm *.out")
    os.system ("cd Catalogue && rm *.log")
    os.system ("cd Catalogue && rm *.toc")
    os.system ("cd Catalogue && rm *.aux")

        



catalogueBuilder ("algebre")



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

    def launchExtEditor (self, name):
        self.log ("FILEEDIT", "ouvre le fichier {}".format (name))
        os.system ("open {}".format (name))

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
    
    def openExo (self, name)::
        self.log ("OPENEXO", "accède à l'exercice {}".format (name))
        return self.open ("Exos/{}.tex".format (name), "r")

    def openCatalogue (self, name):
        return yaml.load (self.open ("Catalogue/{}.yaml".format (name), "r"))

    def openCatalogueTex (self, name):
        return self.open ("Catalogue/{}.tex".format (name), "w")

    def openExercices (self):
        return yaml.load (self.open ("tags.yaml", "r"))

    def openCatalogueTemplate (self):
        return self.open ("Catalogue/template.tex","r")

    def openFicheTemplate (self,name="template"):
        return self.open ("Fiches/{}.tex".format (name),"r")

    def openFiche (self, name):
        return yaml.load (self.open ("Fiches/{}.yaml".format (name), "r"))

    def openFicheTex (self, name):
        return self.open ("Fiches/{}.tex".format (name), "w")


class LaTeX:
    def __init__ (self, filehandler):
        self.output = filehandler

    def cmd (self, name):
        self.output.write ("\\" + name + "\n")

    def cmdA (self, name, *args):
        self.output.write ("\\" + name + "{" + "}{".join (args) + "}" + "\n")

    def begin (self, name):
        self.output.write("\\begin{" + name + "}\n")
    
    def end  (self, name):
        self.output.write("\\end{" + name + "}\n")

    def space (self):
        self.output.write ("\n\n")


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
    L      = LaTeX (output)

    template  = I.openCatalogueTemplate ()
    for l in template.readlines ():
        output.write (l) 
    template.close ()
    

    # TODO: trier par catégorie de tags ... !?!
    def sortKey (x):
        ID,exo = x 
        return (exo.values ())

    # catalist.sort (key = sortKey) 
    for (ID,exo) in catalist:
        exoctn = I.openExo (ID)
        L.cmdA ("exoID", ID)
        for l in exoctn.readlines ():
            output.write (l)
        exoctn.close ()

    L.end ("document")
    output.close ()

    # Compile une ou deux fois pour être sûr 
    os.system ("cd Catalogue && pdflatex {}.tex".format (name)) 
    os.system ("cd Catalogue && pdflatex {}.tex".format (name)) 
    
    # Supprime les fichiers intermédiaires
    os.system ("cd Catalogue && rm *.out")
    os.system ("cd Catalogue && rm *.log")
    os.system ("cd Catalogue && rm *.toc")
    os.system ("cd Catalogue && rm *.aux")

       
def ficheBuilder (name):
    """ Construire une fiche d'exercices
        à partir d'un fichier qui liste 
        les exercices 
    """

    fichedesc = I.openFiche (name)

    eleves  = [ nom for trinome in fichedesc["trinômes"]
                    for nom in trinome ] 
    semaine = str(fichedesc["semaine"])
    date    = fichedesc["date"]
    titre   = fichedesc["titre"]
    cours   = fichedesc["cours"]

    random.shuffle (cours)

    # ÉCRITURE DANS LE FICHIER
    output = I.openFicheTex (name)
    L      = LaTeX (output)

    # Le « bruit » 
    template  = I.openFicheTemplate ("headers")
    for l in template.readlines ():
        output.write (l) 
    template.close ()

    # Définition des en-têtes 
    L.cmdA ("lhead", "MPSI -- Semaine " + semaine) 
    L.cmdA ("rhead", date) 

    L.space ()

    L.begin ("document")

    L.space ()

    L.begin ("center")
    L.cmdA ("rule", "15em", "2pt")
    L.space ()
    L.cmdA ("vspace", "1em")
    L.cmdA ("textbf", "\\huge{" + titre + "}")
    L.cmdA ("vspace", "0.5em")
    L.space ()
    L.cmdA ("rule", "15em", "2pt")
    L.end   ("center")
    
    L.space ()


    output.write ("""
    \\begin{center}
        \\rule[0.23em]{1.5em}{1pt} 
        \\textbf{Question de cours}
        \\rule[0.23em]{24em}{1pt}
    \\end{center}
    """)

    L.space ()

    L.begin ("center")
    output.write ("""\\begin{minipage}{0.8\\linewidth}
    \\begin{tabular}{rl}
    """)
    
    # INSÉRER ICI LES QUESTIONS DE COURS 

    for (eleve,question) in zip (eleves, cours):
        output.write ("\\textbf{" + eleve + "} & " + question + " \\\\ \n")


    output.write ("\\end{tabular}\n\\end{minipage}\n")
    L.end   ("center")

    output.write ("""
    \\begin{center}
        \\rule{35em}{1pt}
    \\end{center}
    """)

    for trinome in fichedesc["trinômes"]:
        for eleve in trinome:
            L.space ()
            L.cmdA ("textbf", eleve)
            L.cmd ("resetexo")
            L.space ()
            for exo in fichedesc[eleve]:
                L.begin ("exo")
                
                exoctn = I.openExo (exo)
                for ligne in exoctn.readlines ():
                    output.write (ligne)
                exoctn.close ()

                L.end ("exo")
                L.space ()
        L.cmd("newpage")

    L.end("document")
    output.close ()




# catalogueBuilder ("algebre")
# ficheBuilder ("S-13")






# Statistiques en python
from scipy import stats

notes = open ("notes.txt","r")

def removeSpaces (x):
    """ Supprime les espaces dans une chaine de caractères
        (espaces, tabulations etc...) """
    return "".join (x.split (" "))

def extractNotes (line):
    [nom,notesN] = line.split (":")
    notesN = notesN.split (",")
    return (nom,notesN)


notes = dict(extractNotes (removeSpaces (line[:-1]))
        for line in notes.readlines ())

notesTotal = [ int (note[:-1]) 
        for (_,N) in notes.items ()
        for note in N ]

notesGat   = [ int (note[:-1]) 
               for (_,N) in notes.items () 
               for note in N 
               if note[-1] == "G" ]

notesAli   = [ int (note[:-1]) 
               for (_,N) in notes.items () 
               for note in N 
               if note[-1] == "A" ]


descTotal = stats.describe (notesTotal)
descGat = stats.describe (notesGat)
descAli = stats.describe (notesAli)

print ("Moyenne: {} (Ali) | {} (Gat) | {} (Total)".format (descAli.mean,
    descGat.mean, descTotal.mean))
print ("Variance: {} (Ali) | {} (Gat) | {} (Total)".format (descAli.variance,
    descGat.variance, descTotal.variance))

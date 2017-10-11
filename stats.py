# Statistiques en python
from scipy import stats
import matplotlib.pyplot as plt

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

print(descAli)

print ("Moyenne: {} (Ali) | {} (Gat) | {} (Total)".format (descAli.mean,
    descGat.mean, descTotal.mean))
print ("Variance: {} (Ali) | {} (Gat) | {} (Total)".format (descAli.variance,
    descGat.variance, descTotal.variance))


plt.hist([notesAli, notesGat], bins = range(0,20), color = ['yellow', 'green'],
            edgecolor = 'black', hatch = '/', label = ['Ali', 'Gat'],
            histtype = 'bar')
plt.ylabel('Nb eleves')
plt.xlabel('Note')
plt.title('Ste Marie')
plt.legend()

plt.show()

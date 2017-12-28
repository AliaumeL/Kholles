import re 

f = open ("exosvrac.tex","r")

ctn = f.read ()

SEC = re.split ("\\\\section{[^}]+}", ctn)
ctn = "".join (SEC)
SEC = re.split ("\\\\subsection{[^}]+}", ctn)
ctn = "".join (SEC)
SEC = re.split ("\\\\subsubsection{[^}]+}", ctn)
ctn = "".join (SEC)

L = ctn.split ("\\exercice")

L = L[2:]

L = [ "\\exercice" + exo for exo in L ]

# print (L)

letter  = "A"

for i,exo in enumerate (L):
    g = open ("Exos/A{:03d}.tex".format (i), "w")

    print (exo)

    g.write (exo)
    g.close ()



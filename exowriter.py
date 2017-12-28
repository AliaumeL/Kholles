
f = open ("tags.yaml","w")

def writeExo (number):
    s = """
A{:03d}:
    année: SUP
    difficultée: "***"
    tags: 
        - Mathématiques

    """.format (number)

    f.write (s)


for i in range (225):
    writeExo (i)



import numpy

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def formatFile(Path):
    path = Path

    data = open(path, 'r')
    lines = data.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].split('\n')
        lines[i] = lines[i][0].split(',')

    # Eliminamos los valores que sean missing
    nouArray = []
    for i in lines:
        boolInterrogant = False
        for j in i:
            if (j == '?'):
                boolInterrogant = True

        if (boolInterrogant == False):
            nouArray.append(i)
    lines = nouArray

    # Convertimos los datos no numericos en valores numericos en funcion a la coumna
    conv = [[] for i in range(len(lines[0]))]  # Matriu de conversio (Una llista per a cada atribut)
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            val = lines[i][j]  # Per cada valor de cada mostra:
            if (not isfloat(val) and val != '?'):
                if (not val in conv[j]):
                    conv[j].append(val)
                lines[i][j] = conv[j].index(val)
    data.close()

    return conv, numpy.array(lines)
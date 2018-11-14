import InfoFunctions as info
from Tree import *


class ID3:
    # data = array 2D numpy con todas las muestras.
    #        cada muestra es una linea con n columnas con el valor de cada atributo
    #		 ***LA PRIMERA COLUMNA ES LA CLASIFICACION
    #		->	[(muestras) [ (columnas) [(valor)],[], ...], [ [],[],... ], [ [],[],... ], ...]
    #
    # classCount = numero de classes distintas en que se clasifican las muestras
    #
    # colDomain = lista con el valor maximo que pueden tomar los atributos de cada colmna
    #		-> [x1,x2,x3,...] x1 = valor maximo que puede tomar el atributo 1

    def __init__(self, data, classCount, colDomain):
        self.data = data
        self.classCount = classCount
        self.tree = None
        self.colDomain = colDomain
        self.root = None

    # Cuenta el numero de muestras que pertenecen a cada classe de samples
    def countClass(self, samples):
        count = []
        for i in range(self.classCount):
            count.append(0)

        for i in samples:
            count[i[0]] = count[i[0]] + 1

        return count

    # Cuenta el numero de muestras que pertenecen a cada classe de samples filtrado segun valores de atributos
    # -> atribCols = lista con las columnas de los atributos seleccionados
    # -> atribVals = lista con los valores de los atributos seleccionados
    def countClassFilter(self, samples, atribCols, atribVals):
        count = [0 for i in range(self.classCount)]
        # for i in range(self.classCount):
        # count.append(0)

        for i in samples:  # Para cada muestra
            entra = len(atribCols)
            for a in range(len(atribCols)):  # Para cada atributo
                if (i[atribCols[a]] == atribVals[a]):
                    entra = entra - 1
            if entra == 0:
                count[i[0]] = count[i[0]] + 1

        return count

    def ID3(self):

        cclass = self.countClass(self.data)  # Numero de muestras de cada clase
        entro = info.entropia(cclass)  # Entropia de todas las muestras

        self.root = Box(None, entro, cclass, 0)  # Nodo raiz

        cols = range(1, self.data.shape[1])  # lista atributos por los que podemos dividir	(de 1 a n (1 = clase))

        self.doID3(self.root, cols, [], [])

        return self.root

    # Hacer ID3 recurivammente
    # Busca el mejor atributo i divide, generando los nodos
    # Debuelve el nuevo nodo divisor
    # -> box : clase Box, conjunto de muestras que queremos dividir
    # -> atribList : lista de atributos por los que aun podemos dividir
    # -> atribDiv : lista de atributos por los que hemos dividido las muestras
    # -> atribVal : valor de los atributos por los que hemos dividido
    def doID3(self, box, atribList, atribDiv, atribVal):

        # ---------------- Calcular el gain mas alto ----------------
        gain = {}
        numelems = box.getNumElems()
        # Calcular el gain de todos los atributos
        for col in atribList:
            A = []
            # Calcular el num de elementos de cada clase segun el atributo
            for val in range(self.colDomain[col - 1] + 1):
                A.append(self.countClassFilter(self.data, atribDiv + [col], atribVal + [val]))

            gain[info.gain(box.getEntropy(), numelems, A)] = col
        # gain.append(info.gain(box.getEntropy(), numelems, A))

        # ---------------- Dividir con el mejor atributo ----------------
        choseAtrib = gain[max(gain)]
        newDivider = Divider(box, choseAtrib)
        box.setNext(newDivider)

        # atribDiv.append(choseAtrib)
        newAtribDiv = atribDiv[:]
        newAtribDiv.append(choseAtrib)

        newAtribList = atribList[:]
        del newAtribList[newAtribList.index(choseAtrib)]
        # ---------------- Calcular los nodos hijos ----------------

        for val in range(self.colDomain[choseAtrib - 1] + 1):
            cclass = self.countClassFilter(self.data, newAtribDiv, atribVal + [val])  # Numero de muestras de cada clase
            entro = info.entropia(cclass)  # Entropia de las muestras
            newBox = Box(newDivider, entro, cclass, val)  # Anadir un nuevo nodo
            newDivider.addChild(newBox)

            if (newBox.getEntropy() != 0 and newAtribList != []):
                self.doID3(newBox, newAtribList, newAtribDiv, atribVal + [val])

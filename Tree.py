from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph


class Tree:
    def __init__(self, root, names=None, conv=None):
        self.root = root
        self.rootGraph = None
        self.names = names
        self.conv = conv

    # Classificar una mostra
    def classify(self, sample):
        actBox = self.root

        while (True):
            if actBox.getNext() != None:
                actDiv = actBox.getNext()
                val = sample[actDiv.getAtr()]
                for b in actDiv.getChilds():
                    if b.getAtrValue() == val:
                        actBox = b
            else:
                return actBox.getClass()

    # Mostrar el arbre per pantalla
    def render(self):
        nodeval = "Entro: " + str(round(self.root.getEntropy(), 3))
        if (self.root.getNext() != None):
            nodeval = '- ' + self.names[self.root.getNext().getAtr()] + ' - ' + nodeval
            root = Node(nodeval)
            self.buildRenderTree(self.root.getNext(), root)
        else:
            root = Node(nodeval)

        self.rootGraph = root

        for pre, fill, node in RenderTree(root):
            print("%s%s" % (pre, node.name))

    # Construeix el arbre per a ser impres per pantalla de forma recursiva
    # Tnod = objecte de la clase Divider
    # Rnod = Node pare
    def buildRenderTree(self, Tnod, Rnod):

        atribu = Tnod.getAtr()

        for b in Tnod.getChilds():
            nodeval = "Entro: " + str(round(b.getEntropy(), 3))
            if b.getNext() == None:
                nodeval = nodeval + ' Class = ' + self.conv[0][b.getClass()]
                n = Node(self.conv[atribu][b.getAtrValue()] + ' ' + nodeval, parent=Rnod)
            else:
                nodeval = self.conv[atribu][b.getAtrValue()] + ' - ' + self.names[
                    b.getNext().getAtr()] + ' - ' + nodeval
                n = Node(nodeval, parent=Rnod)
                self.buildRenderTree(b.getNext(), n)

    # Guarda el arbre en format dot per a obrir-lo amb graphviz
    def renderDot(self):
        RenderTreeGraph(self.rootGraph).to_dotfile("tree2.dot")


# Contine informacion sobre las muestras que salen de una clasificacion
# -> parent = nodo divisor del que proviene
# -> classCount = lista con el numero de muestras de cada clase
#			: [num elemntos clase 0, num elemntos clase 1, ...]
# -> AValue = valor del atributo por el cual ha sido dividido

class Box:

    def __init__(self, parent, entropy, classCount, AValue):
        self.parent = parent
        self.numElems = 0
        self.entropy = entropy
        for i in classCount:
            self.numElems = self.numElems + i
        self.classCount = classCount
        self.next = None  # Un divider
        self.AValue = AValue

    def getParent(self):
        return self.parent

    def getEntropy(self):
        return self.entropy

    def getClassCount(self):
        return self.classCount

    def setNext(self, next):
        self.next = next

    def getNext(self):
        return self.next

    def getNumElems(self):
        return self.numElems

    def getClass(self):
        return self.classCount.index(max(self.classCount))

    def getAtrValue(self):
        return self.AValue


# Divide las muestras segun un atributo
# -> parent = nodo Box del que proviene
# -> attr = atributo que divide

class Divider:

    def __init__(self, parent, attr):
        self.parent = parent
        self.attr = attr  # indice de la columna del atributo a dividir
        self.childs = []  # array de objetos Box

    def addChild(self, box):
        self.childs.append(box)

    def getAtr(self):
        return self.attr

    def getChilds(self):
        return self.childs

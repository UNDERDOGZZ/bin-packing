from pprint import pprint
from tkinter import *
import os

def read(filename):
    with open(filename) as f:
        line = f.readline().strip()
        planchaAncho, planchaAlto = [int(x) for x in line.split(' ')]
        line = f.readline().strip()
        x = line.split(' ')
        n = int(x[0])
        datosRectangulos = []
        for i in range(n):
            line = f.readline().strip()
            indicador, ancho, alto, numPiezas = [x for x in line.split(' ')]
            indicador = str(indicador)
            ancho = int(ancho)
            alto = int(alto)
            numPiezas = int(numPiezas)
            datosRectangulos.append((indicador, ancho, alto, numPiezas))
        #print (datosRectangulos[0][1],datosRectangulos[0][2])
    return planchaAncho, planchaAlto, datosRectangulos

planchaAncho, planchaAlto, datosRectangulos = read("entrada.txt")

master = Tk()
w = Canvas(master, width=planchaAncho, height=planchaAlto)  # Size of the window
#

class Rectangulo:
    def __init__(self, ancho, alto, color, x=None, y=None):
        self.ubicado = False
        self.ancho = ancho
        self.alto = alto
        self.color = color
        self.x = x
        self.y = y

    def __repr__(self):
        return "ractangulo({}) : {}x{}, {};{}, ubicado: {}".format(self.color, self.ancho, self.alto, self.x, self.y, self.ubicado)

    def encaja(self, node):
        if not node.usado and node.ancho >= self.ancho and node.alto >= self.alto:
            self.ubicado = True
            self.x = node.x
            self.y = node.y
            return True
        else:
            return False

    def girar(self):
        self.ancho, self.alto = self.alto, self.ancho

    def dibujar(self):
        w.create_rectangle(self.x, self.y, self.x + self.ancho, self.y + self.alto, fill=self.color, outline="black")

    def tocandoBordes(self, max_x, max_y):
        if self.x + self.ancho == max_x:
            return self.ancho + 2 * self.alto
        elif self.y + self.alto == max_y:
            return 2 * self.ancho + self.alto
        else:
            return self.ancho + self.alto


class Node:
    def __init__(self, ancho, alto, x=0, y=0):
        self.usado = False
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto

    def __repr__(self):
        return "Node : {}x{}, {};{}, usado: {}".format(self.ancho, self.alto, self.x, self.y, self.usado)

    def encontrar(self, ancho, alto):
        return self.derecha, self.abajo

    def separar(self, rectangulo):
        self.usado = True
        node_abajo = Node(self.ancho, self.alto - rectangulo.alto, self.x, self.y + rectangulo.alto)
        node_derecha = Node(self.ancho - rectangulo.ancho, rectangulo.alto, self.x + rectangulo.ancho, self.y)

        return node_abajo, node_derecha

    def dibujar(self):
        w.create_rectangle(self.x, self.y, self.x + self.w, self.y + self.h, fill="black", outline="red")

rectangulos = list()
i = 0
# crear rectangulos

for i in range(len(datosRectangulos)):
    rectangulos.append(Rectangulo(datosRectangulos[i][1],datosRectangulos[i][2], "white"))

#print rectangulos

nodes = list()
w.configure(background='black')
w.pack()
nodes.append(Node(planchaAncho, planchaAlto))  # area de empaquetado
# nodes.append(Node(360, 260))
ymax = 0

rectangulos.sort(key=lambda x: (x.alto * x.ancho), reverse=True)
for rectangulo in rectangulos:
    nodes.sort(key=lambda x: x.y)
    for node in nodes:
        if not rectangulo.ubicado:  # revisa si el rectangulo no ha sido ubicado
            if not rectangulo.encaja(node):  # si no entra, gira
                rectangulo.girar()
            if rectangulo.encaja(node):  # revisa si entra
                score1 = rectangulo.tocandoBordes(nodes[0].ancho, nodes[0].alto)
                rectangulo.girar()
                score2 = rectangulo.tocandoBordes(nodes[0].ancho, nodes[0].alto)
                if ymax < rectangulo.y + rectangulo.ancho:
                    # print(block.y+block.w)
                    ymax = rectangulo.y + rectangulo.ancho
                if score1 > score2 or score1 == score2:
                    rectangulo.girar()
                #node.draw()
                rectangulo.dibujar() # dibujar rectangulo

                node_abajo, node_derecha = node.separar(rectangulo)

                if node_abajo.ancho > 0 and node_abajo.alto > 0:
                    nodes.append(node_abajo)
                if node_derecha.ancho > 0 and node_derecha.alto > 0:
                    nodes.append(node_derecha)
                    #node.draw()
            else:  # si no entra, vuelve a girar
                rectangulo.girar()
        w.update()

pprint(rectangulos)
areas = 0.0
areaTotal = planchaAncho*planchaAlto
for i in range(len(rectangulos)):
    if rectangulos[i].ubicado:
        areas = areas + rectangulos[i].ancho*rectangulos[i].alto
print ("Area total: ",areaTotal)
print ("Area cubierta: ", areas)
areaDesocupada = areaTotal-areas
print ("Area no ocupada: ", areaDesocupada)
desperdicio = (areaDesocupada/areaTotal)*100
print ("Desperdicio: ", desperdicio,"%")

file = open("/Users/ricardoguevara/Documents/Complejidad Algortimica/Bin-Packing/salida.txt", "w")
file.write("Area total: "+str(areaTotal)+os.linesep)
file.write("Area cubierta: "+str(areas)+os.linesep)
file.write("Area no ocupada: "+str(areaTotal)+os.linesep)
file.write("Desperdicio: "+str(desperdicio)+"%"+os.linesep)
file.close()

mainloop()
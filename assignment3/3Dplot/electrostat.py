# -*- coding: utf-8 -*-
"""
electrostat.py
Nathalie van Sterkenburg (11037466)

Berekent de potentiaal op een oppervlak als alleen de randcondities gegeven zijn.
Plot het resultaat in 2D en 3D, plot een grafiek van de potentiaal in het midden
van het oppervlak en plot de convergentie-monitor.
Voert ook de extra opdrachten uit en doet hetzelfde voor de potentialen van een
condensator, puntlading en potentiaal in een halve cirkel.

Nauwkeurigheid is laag omdat ook de drie extra opgaven worden uitgevoerd en de 
code anders heel traag is. De nauwkeurigheid kan worden verhoogd door de globale
variabelen op regel 25 kleiner te maken. Het wordt dan wel geadviseerd het 
berekenen van een of meerdere potentialen uit te schakelen. Dit kan helemaal
onderaan de code.
Plots van de nauwkeurig bepaalde potentialen zijn in de bijgevoegde zip folder
te vinden.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Emin = 0.5

class randcondities:
    """ Klasse met alle randcondities en constanten. """
    
    def __init__(self, x_min, x_max, y_min, y_max, V0, intervallen, omega):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.V0 = V0
        self.intervallen = intervallen
        self.hx = (x_max - x_min) / intervallen
        self.hy = (y_max - y_min) / intervallen
        
        """
        Met behulp van omega wordt de relaxatietijd ingesteld.
        Uitproberen van verschillende omega wijst uit dat als omega iets kleiner
        is dan 2 het programma het snelst is en het beste resultaat levert.
        Als omega echter te dicht bij 2 komt, functioneert het programma niet
        meer goed, hetzelfde geldt voor wanneer de potentiaal te dicht bij 0 komt.
        Omega moet dus in ieder geval tussen 0 en 2 liggen.
        """
        self.omega = omega

voorwaarden = randcondities(0., 1., 0., 1, 10., 100, 1.)

def main(condities = voorwaarden):
    """ Berekent de potentiaal van probleem 1 en plot alle resultaten. """
    
    V = []
    x = []
    y = []
    
    # vult lijsten x en y met juiste waarden en matrix V met randcondities en nullen
    for j in range(condities.intervallen + 1):
        
        # voegt lijst (om matrix te creëren) of waarde aan de lijst toe
        V.append([])
        x.append(condities.x_min + j * condities.hx)
        y.append(condities.y_min + j * condities.hy)
            
        # voegt waarde aan matrix toe
        for i in range(condities.intervallen + 1):
            
            # randcondities
            if j == 0:
                V[j].append(condities.V0)
            
            else:
                V[j].append(0)
    
    # berekent potentiaal
    V, Elijst = potentiaal(V)
    
    # de plots
    drieDplot(x, y, V, "probleem 1")
    middenPlot(x, y, V, "probleem 1")
    
    # 2D plot staat uit om het aantal plots te beperken
    # kan worden ingeschakeld door "#" te verwijderen
    #tweeDplot(V, "probleem 1")

    # plot convergentie-monitor
    plt.figure()
    plt.plot([x for x in range(1, len(Elijst) + 1)], Elijst)
    plt.xlabel("aantal stappen (a.u.)")
    plt.ylabel("E (a.u.)")
    plt.title("E uitgezet tegen het aantal stappen dat al is gezet (probleem 1)")
    plt.show()
    
    
def potentiaal(V, switch = 0, condities = voorwaarden):
    """ 
    Berekent de potentiaal met alleen de randcondities. Met switch kan worden
    ingesteld welke randcondities er zijn. switch = 0 voor randcondities aan de rand.
    """
    
    # initializeren waarden
    Everschil = 100
    Evorig = 0
    E = 0
    Elijst = []
    
    # Everschil geeft een indicatie van de nauwkeurigheid
    # loop wordt gestopt bij voldoende nauwkeurigheid
    while Everschil > Emin:
        
        # potentiaal wordt op ieder punt berekend
        for j in range(1, condities.intervallen + 1):
            
            for i in range(1, condities.intervallen + 1):
                
                # nodig voor de potentiaal in een kwart cirkel
                x_waarde = condities.x_min + i * condities.hx
                y_waarde = condities.y_min + j * condities.hy
                
                # randvoorwaarde wordt niet aangepast in geval van puntlading
                if switch == 1 and j == condities.intervallen / 2 and i == condities.intervallen / 2:
                    switch = 1
                    
                # randvoorwaarde wordt niet aangepast in geval van kwart cirkel
                if switch == 2 and x_waarde ** 2 + y_waarde ** 2 > 0.99 and x_waarde ** 2 + y_waarde ** 2 < 1.01:
                    switch = 2
                
                # berekenen potentiaal
                elif i < condities.intervallen and j < condities.intervallen:
                    Vxy = (1 - condities.omega) * V[j][i] + condities.omega * (V[j][i-1] + V[j][i+1] + V[j-1][i] + V[j+1][i]) / 4.
                
                    V[j][i] = Vxy
        
                # nieuwe E wordt ook berekend
                E += (V[j][i] - V[j][i-1]) ** 2 + (V[j][i] - V[j-1][i]) ** 2
        
        # Everschil wordt berekend en waarden worden geüpdate
        Everschil = abs(Evorig - E)
        Elijst.append(E)
        Evorig = E
        E = 0
        
    return V, Elijst
    
def drieDplot(x, y, V, title):
    """ Plot de potentiaal in 3D. """
    print(len(x))
    print(len(y))
    print(len(V))

    x_matrix, y_matrix = np.meshgrid(np.array(x), np.array(y))
    
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    surf = ax.plot_surface(x_matrix, y_matrix , np.array(V), cmap=plt.cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_xlabel("x (a.u.)")
    ax.set_ylabel("y (a.u.)")
    ax.set_zlabel("Potentiaal (a.u.)")
    ax.set_title("Potentiaal op de rechthoek (%s)" %(title))
    fig.colorbar(surf, shrink=0.5, aspect=5, label = "Potentiaal (a.u.)")
    plt.show()
    
    
def tweeDplot(V, title):
    """ Plot de potentiaal in 2D. """
    
    fig, ax = plt.subplots()
    im = ax.imshow(V, origin = 'lower', extent = [0,1,0,1])
    ax.set_xlabel("x (a.u.)")
    ax.set_ylabel("y (a.u.)")
    ax.set_title("Potentiaal op de rechthoek (%s)" %(title))
    fig.colorbar(im, orientation = 'horizontal', label = "Potentiaal (a.u.)")
    plt.show()
    

def middenPlot(x, y, V, title, condities = voorwaarden):
    """ Plot van de potentiaal in het midden. """
    
    plt.figure()        
    plt.plot(x, V[int(condities.intervallen / 2)], label = "x")
    plt.plot(y, [Vy[int(condities.intervallen / 2)] for Vy in V], label = "y")
    plt.legend()
    plt.xlabel("Positie (a.u.)")
    plt.ylabel("Potentiaal (a.u.)")
    plt.title("De potentiaal uitgezet tegen de positie in de x en y richting met de andere coordinaat in het midden (%s)" %(title))
    plt.show()


def condensator(condities = voorwaarden):
    """ Berekent de potentiaal van een condensator en plot de resultaten. """
    
    V = []
    x = []
    y = []
    
    # vult lijsten x en y met juiste waarden en matrix V met randcondities en nullen
    for j in range(condities.intervallen + 1):
        
        # voegt lijst (om matrix te creëren) of waarde aan de lijst toe
        V.append([])
        x.append(condities.x_min + j * condities.hx)
        y.append(condities.y_min + j * condities.hy)
            
        # voegt waarde aan matrix toe
        for i in range(condities.intervallen + 1):
            
            # randcondities
            if j == 0:
                V[j].append(condities.V0)
            
            elif j == condities.intervallen:
                V[j].append(-condities.V0)
                
            else:
                V[j].append(0)
    
    # berekent potentiaal
    V = potentiaal(V)[0]
    
    # de plots
    drieDplot(x, y, V, "condensator")
    
    # 2D en midden plot staat uit om aantal plots te beperken
    # kan worden ingeschakeld door "#" te verwijderen
    #tweeDplot(V, "condensator")
    #middenPlot(x, y, V, "condensator")
    

def puntlading(condities = voorwaarden):
    """ Berekent de potentiaal van een puntlading en plot de resultaten. """
    
    V = []
    x = []
    y = []
    
    # vult lijsten x en y met juiste waarden en matrix V met randcondities en nullen
    for j in range(condities.intervallen + 1):
        
        # voegt lijst (om matrix te creëren) of waarde aan de lijst toe
        V.append([])
        x.append(condities.x_min + j * condities.hx)
        y.append(condities.y_min + j * condities.hy)
            
        # voegt waarde aan matrix toe
        for i in range(condities.intervallen + 1):
            
            # randcondities
            if j == condities.intervallen / 2 and i == condities.intervallen / 2:
                V[j].append(100 * condities.V0)
                
            else:
                V[j].append(0)
    
    # berekent potentiaal
    V = potentiaal(V, 1)[0]
    
    # de plots
    drieDplot(x, y, V, "puntlading")
    
    # 2D en midden plot staat uit om aantal plots te beperken
    # kan worden ingeschakeld door "#" te verwijderen
    #tweeDplot(V, "puntlading")
    #middenPlot(x, y, V, "puntlading")
    

def cirkel(condities = voorwaarden):
    """ Berekent de potentiaal van een kwart cirkel en plot de resultaten. """
    
    V = []
    x = []
    y = []
    
    # vult lijsten x en y met juiste waarden en matrix V met randcondities en nullen
    for j in range(condities.intervallen + 1):
        
        x_waarde = condities.x_min + j * condities.hx
        y_waarde = condities.y_min + j * condities.hy
        
        # voegt lijst (om matrix te creëren) of waarde aan de lijst toe
        V.append([])
        x.append(x_waarde)
        y.append(y_waarde)
            
        # voegt waarde aan matrix toe
        for i in range(condities.intervallen + 1):
            
            # randcondities
            x_waarde = condities.x_min + i * condities.hx
            
            if x_waarde ** 2 + y_waarde ** 2 > 0.99 and x_waarde ** 2 + y_waarde ** 2 < 1.01:
                V[j].append(condities.V0 / 4.)
                
            else:
                V[j].append(0)
    
    # berekent potentiaal
    V = potentiaal(V, 2)[0]
    
    # de plots
    tweeDplot(V, "kwart cirkel")
    
    # 3D en midden plot staan uit om aantal plots te beperken
    # kan worden ingeschakeld door "#" te verwijderen
    #drieDplot(x, y, V, "kwart cirkel")
    
    # merk op bij midden plot dat x en y hetzelfde zijn in dit probleem en dus
    # over elkaar heen liggen
    #middenPlot(x, y, V, "kwart cirkel")
    

if __name__ == "__main__":
    """ 
    Er kunnen vier verschillende potentialen berekent worden. Een of meerdere
    potentialen kunnen tijdelijk worden uitgeschakeld door een "#" voor de functie
    te zitten. Minder potentialen tegelijk betekent een kortere runtime.
    """
    
    main()
    condensator()
    puntlading()
    cirkel()



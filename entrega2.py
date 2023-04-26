#from simpleai.search import MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack,LEAST_CONSTRAINING_VALUE,HIGHEST_DEGREE_VARIABLE
from itertools import combinations

def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    
    #Variables son pos_paredes, pos_cajas, pos_obj y pos_jugador
    
    lista_paredes = []
    i = 0
    for pared in cantidad_paredes:
        lista_paredes.append('pared' + i)
        i = i + 1
    
    lista_cajas = []
    i = 0
    for caja in cantidad_cajas_objetivos:
        lista_cajas.append('caja' + i)
        i = i + 1

    lista_objetivos = []
    i = 0
    for caja in cantidad_cajas_objetivos:
        lista_objetivos.append('objetivo' + i)
        i = i + 1
    


    jugador = ['jugador']

    variables = []    
    variables = lista_paredes + lista_cajas + lista_objetivos + jugador

    dominio = {}
    def borde_rectangulo(filas, columnas):
        borde = []
        for fila in range(filas):
            borde.append((fila, 0))
            borde.append((fila, columnas-1))
        for columna in range(1, columnas-1):
            borde.append((0, columna))
            borde.append((filas-1, columna))
        return borde
    
    bordes = borde_rectangulo(filas,columnas)
    coord_valids = []
    for fila in filas:
        for colum in columnas:
            new_coord = (fila,colum)
            if new_coord not in bordes:
                coord_valids.append(new_coord)

    for var in variables:


    #restric    
    # El mapa tiene forma rectangular, siempre.

    # Solo la posición de las paredes "internas" del mapa importan y se intentarán ubicar. El borde en cambio se asume fijo, y no se incluye dentro de la grilla que hay que resolver.
    
    # La cantidad de cajas y objetivos siempre será la misma, y solo habrá un jugador, como en el juego normal.
    
    # No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador. Nótese que los objetivos no son objetos físicos, podría el jugador comenzar en la misma posición que un objetivo, o una caja comenzar sobre un objetivo también.
    
    # Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar.
    
    # El juego no debe estar ya ganado. Es decir, las cajas no pueden estar todas ya ubicadas en las posiciones objetivos. Lo que sí está permitido es que algunas cajas comiencen ubicadas sobre objetivos (que puede suceder en el juego real, ya que quizás hay que moverlas para ganar).
    
    # Las cajas no deben tener más de una pared adyacente, ya que eso incrementa mucho las chances de que la caja nunca pueda ser movida. Las cajas en los bordes son un caso especial: no deberían tener ninguna pared adyacente, ya que el borde implica que ya tienen una "pared" al lado.
    
    # No se pueden ubicar cajas en las esquinas del mapa, ya que nunca podrían ser movidas.


    def funcionrestriccion (variables,values):  #Variables: tupla de variables, values: tupla de valores
        return True
    
    
    
    return bordes

print(armar_mapa(3,4,2,2))

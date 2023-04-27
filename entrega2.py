#from simpleai.search import MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack,LEAST_CONSTRAINING_VALUE,HIGHEST_DEGREE_VARIABLE
from itertools import combinations, product

def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    
    #Variables son pos_paredes, pos_cajas, pos_obj y pos_jugador
    # La cantidad de cajas y objetivos siempre será la misma, y solo habrá un jugador, como en el juego normal.
    # Solo la posición de las paredes "internas" del mapa importan y se intentarán ubicar. El borde en cambio se asume fijo, y no se incluye dentro de la grilla que hay que resolver.
    lista_paredes = []
    i = 0
    for pared in range(cantidad_paredes):
        lista_paredes.append('pared' + str(i))
        i = i + 1
    
    lista_cajas = []
    i = 0
    for caja in range(cantidad_cajas_objetivos):
        lista_cajas.append('caja' + str(i))
        i = i + 1

    lista_objetivos = []
    i = 0
    for caja in range(cantidad_cajas_objetivos):
        lista_objetivos.append('objetivo' + str(i))
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
    for fila in range(filas):
        for colum in range(columnas):
            new_coord = (fila,colum)
            if new_coord not in bordes:
                coord_valids.append(new_coord)

    for var in variables:
        dominio[var] = coord_valids

    restricciones = []
    #restric    
    # El mapa tiene forma rectangular, siempre. --Ni idea todavia
    # No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador. Nótese que los objetivos no son objetos físicos, podría el jugador comenzar en la misma posición que un objetivo, o una caja comenzar sobre un objetivo también.
    variables_chocan = lista_cajas + lista_paredes + jugador
    
    def NoSameCoord (variables,values):
        #var1,var2 =variables
        val1,val2 = values
        return val1 != val2

    for var1,var2 in combinations(variables_chocan,2):
            restricciones.append(
                ((var1,var2),NoSameCoord)
            )     
   
    # Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar.
    lista_paredes_obj = lista_paredes + lista_objetivos
    for var1,var2 in product(lista_paredes, lista_objetivos, repeat=2):
        restricciones.append(
            ((var1,var2),NoSameCoord)
        )
    
    # El juego no debe estar ya ganado. Es decir, las cajas no pueden estar todas ya ubicadas en las posiciones objetivos. Lo que sí está permitido es que algunas cajas comiencen ubicadas sobre objetivos (que puede suceder en el juego real, ya que quizás hay que moverlas para ganar).
    
    lista_cajas_objetivos = lista_cajas + lista_objetivos
    def NoWinGame(variables,values):
        cant_variables = 0
        for var in variables:
            cant_variables = cant_variables +1
        i =0
        max_repetitions = cant_variables/2 -1 #como hay igual cantidad de cajas que de objetivos, la suma siempre da par y su mitad sera entera. Le resto 1 pq si llega a esa mitad quiere decir que todas las cajas y obj tienen el mismo valor.
        for val in values:
            for val2 in values:
                if val == val2:
                    max_repetitions = max_repetitions -1
                    if max_repetitions < 0:
                        return False
        
        return True

    restricciones.append(
        (lista_cajas_objetivos,NoWinGame)
    ) 
    # Las cajas no deben tener más de una pared adyacente, ya que eso incrementa mucho las chances de que la caja nunca pueda ser movida. Las cajas en los bordes son un caso especial: no deberían tener ninguna pared adyacente, ya que el borde implica que ya tienen una "pared" al lado.
    
    # No se pueden ubicar cajas en las esquinas del mapa, ya que nunca podrían ser movidas.    
    
    return dominio

print(armar_mapa(3,4,2,2))

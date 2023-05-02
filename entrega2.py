# import simpleia
from simpleai.search import MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack,LEAST_CONSTRAINING_VALUE,HIGHEST_DEGREE_VARIABLE
from itertools import combinations, product

def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    filas = filas 
    columnas = columnas 
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
    corner = []
    corner.append((0,0))
    corner.append((filas-1,0))
    corner.append((0,columnas-1))
    corner.append((filas-1,columnas-1))

    coord_valids = []
    for fila in range(filas):
        for colum in range(columnas):
            new_coord = (fila,colum)
            coord_valids.append(new_coord)

    coord_valids_no_corner = []
    for coords in coord_valids:
        if coords not in corner:
            coord_valids_no_corner.append(coords)
    for var in variables:
        if 'caja' in var:
            dominio[var] = coord_valids_no_corner            
        else:
            dominio[var] = coord_valids

    restricciones = []
    #restric    
    # El mapa tiene forma rectangular, siempre. --Ni idea todavia
    # No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador. Nótese que los objetivos no son objetos físicos, podría el jugador comenzar en la misma posición que un objetivo, o una caja comenzar sobre un objetivo también.
    variables_chocan = lista_cajas + lista_paredes + jugador
    
    def NoSameCoord (variables,values):
        #var1,var2 =variables
        val1,val2 = values

        if val1 == val2:
            return False
        else:
            return True
    

    for var1,var2 in combinations(variables_chocan,2):
            restricciones.append(
                ((var1,var2),NoSameCoord)
            )     
   
    # Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar.
    #lista_paredes_obj = lista_paredes + lista_objetivos
    for pared in lista_paredes:
        for objetivo in lista_objetivos:
            restricciones.append(
                ((pared,objetivo),NoSameCoord)
            )
    
    #objetivos no en el mismo lugar
    if len(lista_objetivos) > 1 :
        for obj1,obj2 in combinations(lista_objetivos,2):
            restricciones.append(
                ((obj1,obj2),NoSameCoord)
            )

    # El juego no debe estar ya ganado. Es decir, las cajas no pueden estar todas ya ubicadas en las posiciones objetivos. Lo que sí está permitido es que algunas cajas comiencen ubicadas sobre objetivos (que puede suceder en el juego real, ya que quizás hay que moverlas para ganar).
    
    lista_cajas_objetivos = lista_cajas + lista_objetivos
    def NoWinGame(variables,values):
        max_repetitions = cantidad_cajas_objetivos
        for val1,val2 in combinations(values,2):
             if val1 == val2:
                    max_repetitions = max_repetitions -1
                    if max_repetitions < 0:
                        return False
        # for val in values:
        #     for val2 in values:
        #         if val == val2:
        #             max_repetitions = max_repetitions -1
        #             if max_repetitions < 0:
        #                 return False
        
        return True

    restricciones.append(
        (lista_cajas_objetivos,NoWinGame)
    ) 
    

    # Las cajas no deben tener más de una pared adyacente, ya que eso incrementa mucho las chances de que la caja nunca pueda ser movida. Las cajas en los bordes son un caso especial: no deberían tener ninguna pared adyacente, ya que el borde implica que ya tienen una "pared" al lado.
    
    def inBorder(val):
        fila,columna = val

        if fila == 0:
            return True
        if fila == filas-1:
            return True
        if columna == 0:
            return True
        if columna == columnas -1:
            return True
        return False
    
    def adyacentes(coord1, coord2):
    #Devuelve True si coord1 y coord2 son adyacentes
        fila1, columna1 = coord1
        fila2, columna2 = coord2
        
        if fila1 == fila2:
            if abs(columna1 - columna2)  == 1:
                return True
        
        if columna1 == columna2: 
            if abs(fila1 - fila2) == 1:
                return True
        return False


    def NotTwoWallsNear (variables,values):
        pared1,pared2,caja = variables
        valPared1,valPared2,valCaja = values
        # fila_caja,columna_caja = valCaja
        # fila_pared1,columna_pared1 = valPared1 
        if valPared1 == valPared2:
            return False
        
        inborder = inBorder(valCaja)
        ady1 = adyacentes(valPared1,valCaja)
        ady2 = adyacentes(valPared2,valCaja)
        # cant_adjy = 0
        if inborder: 
            #no puede tener otra adyacemte
            if ady1 or ady2:
                return False
            else:
                return True
        else:
            if ady1 and ady2:
                return False
            else:
                return True
    
    def NotWallsNear(variables,values):
        pared1,caja = variables
        valPared1,valCaja = values
        # fila_caja,columna_caja = valCaja
        # fila_pared1,columna_pared1 = valPared1 
        
        inborder = inBorder(valCaja)
        ady1 = adyacentes(valPared1,valCaja)
        # cant_adjy = 0
        if inborder: 
            #no puede tener otra adyacemte
            if ady1:
                return False
            else:
                return True
        else:
            return True
        

    if len(lista_paredes) >1:
        for pared1,pared2  in combinations(lista_paredes, 2):
            for caja in lista_cajas:
            
                restricciones.append(
                    ((pared1,pared2,caja),NotTwoWallsNear)
            )
    else:
         for pared in lista_paredes:
             for caja in lista_cajas:
                restricciones.append(
                        ((pared,caja),NotWallsNear)
                )
    

    # No se pueden ubicar cajas en las esquinas del mapa, ya que nunca podrían ser movidas. 
    #Esquinas: (0,0), (fila-1,0), (0,columna-2), (fila-1,columna-1)  
    # corner = []
    # corner.append((0,0))
    # corner.append((filas-1,0))
    # corner.append((0,columnas-1))
    # corner.append((filas-1,columnas-1))

    # def NotInCorner(variables,values):
    #     for val in values:
    #         if val not in corner: #or val == (1,1) or val == (filas-2,1)or val == (1,columnas-2) or val == (filas-2,columnas-2):
    #             return True
    #         else:
    #             return False
    
    # for box in lista_cajas:
    #     restricciones.append(
    #             ((box),NotInCorner)
    #     )
    
    

    problem = CspProblem(variables, dominio, restricciones)
    solution = backtrack(
        problem,
        inference=True,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE,
    )

    lista_paredes_result = []
    lista_cajas_result = []
    lista_objetivos_result = []

    personaje = solution['jugador']

    for pared in lista_paredes:
        lista_paredes_result.append(solution[pared])

    
    for caja in lista_cajas:
        lista_cajas_result.append(solution[caja])

   
    for objetivo in lista_objetivos:
        lista_objetivos_result.append(solution[objetivo])

    return (lista_paredes_result, lista_cajas_result, lista_objetivos_result, personaje)


test = armar_mapa(3,3,1,1)
print(test)

from simpleai.search import MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack,LEAST_CONSTRAINING_VALUE,HIGHEST_DEGREE_VARIABLE
from itertools import combinations, product

def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    filas = filas 
    columnas = columnas 

    #Variables son pos_paredes, pos_cajas, pos_obj y pos_jugador
    # La cantidad de cajas y objetivos siempre será la misma, y solo habrá un jugador, como en el juego normal.
    # Solo la posición de las paredes "internas" del mapa importan y se intentarán ubicar. El borde en cambio se asume fijo, y no se incluye dentro de la grilla que hay que resolver.
    
    lista_paredes = []

    for i in range(cantidad_paredes):
        lista_paredes.append('pared' + str(i))

    
    lista_cajas = []
    lista_objetivos = []

    for i in range(cantidad_cajas_objetivos):
        lista_cajas.append('caja' + str(i))
        lista_objetivos.append('objetivo' + str(i))
    

    jugador = ['jugador']

    variables = []    
    variables = lista_paredes + lista_cajas + lista_objetivos + jugador

    dominio = {}    
 
    corner = []
    corner.append((0,0))
    corner.append((filas - 1,0))
    corner.append((0, columnas - 1))
    corner.append((filas - 1, columnas - 1))

    coord_valids = []
    for fila in range(filas):
        for colum in range(columnas):
            new_coord = (fila, colum)
            coord_valids.append(new_coord)

    coord_valids_no_corner = []
    for coords in coord_valids:
        if coords not in corner:
            coord_valids_no_corner.append(coords)
    for var in variables:
        if 'caja' in var:
            # Si es caja, no le agrego al dominio los corners.
            dominio[var] = coord_valids_no_corner            
        else:
            # Si no, le agrego todas las coordenadas.
            dominio[var] = coord_valids

    restricciones = []
  
    # El mapa tiene forma rectangular, siempre.
    # No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador. 
    # Nótese que los objetivos no son objetos físicos, podría el jugador comenzar en la misma posición que un objetivo, o una caja 
    # comenzar sobre un objetivo también.

    variables_chocan = lista_cajas + lista_paredes + jugador
    
    def no_misma_coordenada(variables, values):
        val1, val2 = values

        if val1 == val2:
            return False
        else:
            return True
    
    # Iteramos las "variables que chocan", en todas sus combinaciones posibles, de a 2.
    for var1, var2 in combinations(variables_chocan, 2):
            restricciones.append(
                ((var1,var2), no_misma_coordenada)
            )     
   
    # Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar.
    for pared in lista_paredes:
        for objetivo in lista_objetivos:
            restricciones.append(
                ((pared, objetivo), no_misma_coordenada)
            )
    
    
    # Objetivos no en el mismo lugar.
    if len(lista_objetivos) > 1:
        for obj1, obj2 in combinations(lista_objetivos, 2):
            restricciones.append(
                ((obj1,obj2), no_misma_coordenada)
            )

    # El juego no debe estar ya ganado. Es decir, las cajas no pueden estar todas ya ubicadas en las posiciones objetivos. 
    # Lo que sí está permitido es que algunas cajas comiencen ubicadas sobre objetivos (que puede suceder en el juego real, 
    # ya que quizás hay que moverlas para ganar).

    lista_cajas_objetivos = lista_cajas + lista_objetivos
    def no_juego_ganado(variables, values):
        max_repetitions = cantidad_cajas_objetivos

        for val1, val2 in combinations(values, 2):
             if val1 == val2:
                    max_repetitions = max_repetitions - 1
                    if max_repetitions < 0: 
                        return False
                    
        return True

    restricciones.append(
        (lista_cajas_objetivos, no_juego_ganado)
    ) 
    

    # Las cajas no deben tener más de una pared adyacente, ya que eso incrementa mucho las chances de que la caja nunca
    # pueda ser movida. Las cajas en los bordes son un caso especial: no deberían tener ninguna pared adyacente, ya que el borde 
    # implica que ya tienen una "pared" al lado.
    
    def en_borde(val):
        fila, columna = val

        if fila == 0:
            return True
        if fila == filas - 1:
            return True
        if columna == 0:
            return True
        if columna == columnas - 1:
            return True
        return False
    
    def adyacentes(coord1, coord2):
    # Devuelve True si coord1 y coord2 son adyacentes
        fila1, columna1 = coord1
        fila2, columna2 = coord2
        
        if fila1 == fila2:
            if abs(columna1 - columna2)  == 1:
                return True
        
        if columna1 == columna2: 
            if abs(fila1 - fila2) == 1:
                return True
        return False


    def no_dos_paredes_cerca(variables,values):
        valPared1, valPared2, valCaja = values

        if valPared1 == valPared2:
            return False
        
        inborder = en_borde(valCaja)
        ady1 = adyacentes(valPared1, valCaja)
        ady2 = adyacentes(valPared2, valCaja)

        if inborder: 
            # no puede tener otra adyacente
            if ady1 or ady2:
                return False
            else:
                return True
        else:
            if ady1 and ady2:
                return False
            else:
                return True
    
    def no_paredes_cerca(variables, values):
        pared1, caja = variables
        valPared1,valCaja = values
        
        inborder = en_borde(valCaja)
        ady1 = adyacentes(valPared1, valCaja)

        if inborder: 
            #no puede tener otra adyacente
            if ady1:
                return False
            else:
                return True
        else:
            return True
        

    if len(lista_paredes) > 1:
        for pared1, pared2  in combinations(lista_paredes, 2):
            for caja in lista_cajas:
            
                restricciones.append(
                    ((pared1,pared2,caja), no_dos_paredes_cerca)
            )
    else:
         for pared in lista_paredes:
             for caja in lista_cajas:
                restricciones.append(
                        ((pared,caja), no_paredes_cerca)
                ) 
    
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


test = armar_mapa(5, 4, 3, 3)
print(test)

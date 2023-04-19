
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
    astar,
    greedy,
)
from simpleai.search.viewers import WebViewer, BaseViewer


def jugar(paredes, cajas, objetivos, jugador, maximos_movimientos):

    # coordenadas paredes
    PAREDES = paredes

    # coordenada global objetivos
    OBJETIVOS = objetivos

    #Maximos movimientos
    MaxMov = maximos_movimientos

    # listado de acciones disponibles
    ACTIONS = (
    'arriba',
    'abajo',
    'izquierda',
    'derecha',
    )
    
    def distanciaObjetivoCercano(box):
        min_distance = float('inf')
        for goal in OBJETIVOS:
            distance = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
            if distance < min_distance:
                min_distance = distance
        return min_distance


    def movimientoValido(jugador, accion, boxes):
        nueva_coord = None
       
        # Calcular la nueva coordenada del jugador segun la accion
        if accion == 'arriba':
            nueva_coord = (jugador[0], jugador[1] - 1)
        elif accion == 'abajo':
            nueva_coord = (jugador[0], jugador[1] + 1)
        elif accion == 'izquierda':
            nueva_coord = (jugador[0] - 1, jugador[1])
        elif accion == 'derecha':
            nueva_coord = (jugador[0] + 1, jugador[1])

        # Verificar si la nueva coordenada del jugador es una pared
        if nueva_coord in PAREDES:
            return False

        # Si la nueva coordenada del jugador hace mover una caja, verificar si la caja se puede mover en la misma dirección
        if nueva_coord in boxes:
            nueva_coord_caja = None
            if accion == 'arriba':
                nueva_coord_caja = (nueva_coord[0], nueva_coord[1] - 1)
            elif accion == 'abajo':
                nueva_coord_caja = (nueva_coord[0], nueva_coord[1] + 1)
            elif accion == 'izquierda':
                nueva_coord_caja = (nueva_coord[0] - 1, nueva_coord[1])
            elif accion == 'derecha':
                nueva_coord_caja = (nueva_coord[0] + 1, nueva_coord[1])

            # Verificar si la nueva coordenada de la caja es una pared o tiene una caja adyacente
            if nueva_coord_caja in PAREDES or nueva_coord_caja in boxes:
                return False

        # Si la nueva coordenada del jugador no es una pared ni una caja, es un movimiento válido
        return True

    def nuevaCoord(jugador, accion):
        nueva_coord = None
        # Calcular la nueva coordenada del jugador segun la accion
        if accion == 'arriba':
            nueva_coord = (jugador[0], jugador[1] - 1)
        elif accion == 'abajo':
            nueva_coord = (jugador[0], jugador[1] + 1)
        elif accion == 'izquierda':
            nueva_coord = (jugador[0] - 1, jugador[1])
        elif accion == 'derecha':
            nueva_coord = (jugador[0] + 1, jugador[1])

        return nueva_coord



    def list_to_tuple(lst):
        return tuple(lst)


    def tuple_to_list(tup):
        return [coord for coord in tup]


    # listado coordenadas cajas,  posicion jugador, cantidad de movimientos máximos)
    INITIAL = (list_to_tuple(cajas), jugador, maximos_movimientos)
    class SokobanProblem(SearchProblem):
        def cost(self, state1, action, state2):
            return 1

        def is_goal(self, state):
            boxes, jugador, mov_restantes = state
            #Sera objetivo cuando las coordenadas de las cajas esten en la lista de objetivos.
            #Siempre y cuando los maximos movientos no se hayan alcanzado
            boxes = list_to_tuple(boxes)
            for caja in cajas:
               if caja not in OBJETIVOS:
                    return False
            
            if mov_restantes < 0:
                return False
            
            return True

        def actions(self, state):
            acciones_disponibles = []
            boxes, jugador, mov_restantes = state
            
            #No miro mov_restantes porque deberia darse cuenta al llamar a isgoal que ya no tiene movimientos/no sirve ese camino
            coord_x, coord_y = jugador
            for accion in ACTIONS:
                accion_disponible = movimientoValido(jugador,accion,boxes)
                if accion_disponible:
                    acciones_disponibles.append(accion)
                            
            return acciones_disponibles

        def result(self, state, action):
            boxes, jugador, mov_restantes = state
           
            new_jugador_coord = nuevaCoord(jugador,action)
           
            mov_restantes = mov_restantes -1

            new_cajas = []
            #Verificar si la nueva posision hace mover una caja
            if new_jugador_coord in boxes:
                boxes = list_to_tuple(cajas)
                for caja in boxes:
                    new_caja_coord = caja
                    if new_jugador_coord == caja:
                        new_caja_coord = nuevaCoord(caja,action)
                    new_cajas.append(new_caja_coord)                
            if len(new_cajas) == 0 :
                return (boxes,new_jugador_coord,mov_restantes)
            else:
                return (new_cajas,new_jugador_coord,mov_restantes)
                

        def heuristic(self, state):
            boxes, jugador, mov_restantes = state
            #La heuristica sera suma de la distancia manhattan de cada caja con su objetivo mas cercano
            distancia = 0
            boxes = list_to_tuple(boxes)
            for caja in boxes:
                distancia_caja = distanciaObjetivoCercano(caja)
                distancia += distancia_caja
            return distancia

    if __name__ == "__main__":
        viewer = BaseViewer()
        result = ()
        result = astar(SokobanProblem(INITIAL), graph_search=True, viewer=viewer)

        if result is not None:
            print("Estado meta:")
            print(result.state)

            pasos=[]
            for action, state in result.path():
                if action is not None:
                    fila_nueva, columna_nueva = action
                    fila, columna = posicion_pj         
                    if fila<fila_nueva:
                        pasos.append("abajo")
                    if fila>fila_nueva:
                        pasos.append("arriba")
                    if columna<columna_nueva:
                        pasos.append("derecha")
                    if columna>columna_nueva:
                        pasos.append("izquierda")
                posicion_pj=state[1]               
                print("Moviendo Jugador", action, "llegué a:")
                print(pasos)
                print(state)
            return pasos 

        else:
            print("No se encontró una solución para el problema de búsqueda.")
    else:
        viewer = BaseViewer()
        secuencia = []
        result = astar(SokobanProblem(INITIAL), graph_search=True)
        for action, state in result.path():
            if action != None:
                secuencia.append(action[1])
        return secuencia
    
# paredes = [
#         (0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
#         (1,0),(1,6),
#         (2,0),(2,6),
#         (3,0),(3,6),
#         (4,0),(4,6),
#         (5,0),(5,6),
#         (6,0),(6,6),
#         (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6)
#     ]
# objetivos = [(5,4)]
# cajas = [(5,3)]
# jugador = (5,2)
# movimientos = 40
    
# secuencia = jugar(paredes, cajas, objetivos, jugador, movimientos)
# print(secuencia)
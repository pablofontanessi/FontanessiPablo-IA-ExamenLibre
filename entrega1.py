
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
        if accion == 'abajo':
            nueva_coord = (jugador[0] + 1, jugador[1])
        elif accion == 'arriba':
            nueva_coord = (jugador[0] - 1, jugador[1])
        elif accion == 'derecha':
            nueva_coord = (jugador[0], jugador[1] + 1)
        elif accion == 'izquierda':
            nueva_coord = (jugador[0], jugador[1] - 1)

        # Verificar si la nueva coordenada del jugador es una pared
        if nueva_coord in PAREDES:
            return False

        # Si la nueva coordenada del jugador hace mover una caja, verificar si la caja se puede mover en la misma dirección
        if nueva_coord in boxes:
            nueva_coord_caja = None
            if accion == 'abajo':
                nueva_coord_caja = (nueva_coord[0] + 1, nueva_coord[1])
            elif accion == 'arriba':
                nueva_coord_caja = (nueva_coord[0] - 1, nueva_coord[1])
            elif accion == 'derecha':
                nueva_coord_caja = (nueva_coord[0], nueva_coord[1] + 1)
            elif accion == 'izquierda':
                nueva_coord_caja = (nueva_coord[0], nueva_coord[1] - 1)

            # Verificar si la nueva coordenada de la caja es una pared o tiene una caja adyacente
            if nueva_coord_caja in PAREDES or nueva_coord_caja in boxes:
                return False

        # Si la nueva coordenada del jugador no es una pared ni una caja, es un movimiento válido
        return True

    def nuevaCoord(jugador, accion):
        nueva_coord = None
        # Calcular la nueva coordenada del jugador segun la accion
        if accion == 'abajo':
            nueva_coord = (jugador[0] + 1, jugador[1])
        elif accion == 'arriba':
            nueva_coord = (jugador[0] - 1, jugador[1])
        elif accion == 'derecha':
            nueva_coord = (jugador[0], jugador[1] + 1)
        elif accion == 'izquierda':
            nueva_coord = (jugador[0], jugador[1] - 1)

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
            # Sera objetivo cuando las coordenadas de las cajas esten en la lista de objetivos.
            # Siempre y cuando los maximos movientos no se hayan alcanzado

            for caja in boxes:
                if caja not in OBJETIVOS:
                    return False

            if mov_restantes < 0:
                return False

            return True

        def actions(self, state):
            acciones_disponibles = []
            boxes, jugador, mov_restantes = state

            for accion in ACTIONS:

                if movimientoValido(jugador, accion, boxes):
                    acciones_disponibles.append(accion)

            return tuple(acciones_disponibles)


        def result(self, state, action):
            boxes, jugador, mov_restantes = state

            new_jugador_coord = nuevaCoord(jugador,action)

            mov_restantes = mov_restantes -1

            new_cajas = []
            #Verificar si la nueva posición hace mover una caja
            if new_jugador_coord in boxes:
                new_boxes = []
                for caja in boxes:
                    new_caja_coord = caja
                    if new_jugador_coord == caja:
                        new_caja_coord = nuevaCoord(caja,action)
                    new_boxes.append(new_caja_coord)
            else:
                new_boxes = boxes

            return (list_to_tuple(new_boxes), new_jugador_coord, mov_restantes)

                        

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
            pasos=[]
            for action, state in result.path():
                if action is not None:
                    print(action)
                    
            return pasos 

        else:
            print("No se encontró una solución para el problema de búsqueda.")
    else:
        viewer = BaseViewer()
        secuencia = []
        result = astar(SokobanProblem(INITIAL), graph_search=True)
        for action, state in result.path():
            if action != None:
                secuencia.append(action)
        return secuencia
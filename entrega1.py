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

    # listado de acciones disponibles
    ACTIONS = (
        'arriba',
        'abajo',
        'izquierda',
        'derecha',
    )
    
    def distancia_objetivo_cercano(box):
        distancia_minima = float('inf')

        for objetivo in objetivos:
            distance = abs(box[0] - objetivo[0]) + abs(box[1] - objetivo[1])
            if distance < distancia_minima:
                distancia_minima = distance

        return distancia_minima


    def movimiento_valido(jugador, accion, boxes):
        nueva_coordenada = None
       
        # Calcular la nueva coordenada del jugador segun la accion
        if accion == 'abajo':
            nueva_coordenada = (jugador[0] + 1, jugador[1])
        elif accion == 'arriba':
            nueva_coordenada = (jugador[0] - 1, jugador[1])
        elif accion == 'derecha':
            nueva_coordenada = (jugador[0], jugador[1] + 1)
        elif accion == 'izquierda':
            nueva_coordenada = (jugador[0], jugador[1] - 1)

        # Verificar si la nueva coordenada del jugador es una pared
        if nueva_coordenada in paredes:
            return False

        # Si la nueva coordenada del jugador hace mover una caja, verificar si la caja se puede mover en la misma dirección
        if nueva_coordenada in boxes:
            nueva_coordenada_caja = None
            if accion == 'abajo':
                nueva_coordenada_caja = (nueva_coordenada[0] + 1, nueva_coordenada[1])
            elif accion == 'arriba':
                nueva_coordenada_caja = (nueva_coordenada[0] - 1, nueva_coordenada[1])
            elif accion == 'derecha':
                nueva_coordenada_caja = (nueva_coordenada[0], nueva_coordenada[1] + 1)
            elif accion == 'izquierda':
                nueva_coordenada_caja = (nueva_coordenada[0], nueva_coordenada[1] - 1)

            # Verificar si la nueva coordenada de la caja es una pared o tiene una caja adyacente
            if nueva_coordenada_caja in paredes or nueva_coordenada_caja in boxes:
                return False

        # Si la nueva coordenada del jugador no es una pared ni una caja, es un movimiento válido
        return True

    def nueva_coordenada(jugador, accion):
        nueva_coordenada = None
        # Calcular la nueva coordenada del jugador segun la accion
        if accion == 'abajo':
            nueva_coordenada = (jugador[0] + 1, jugador[1])
        elif accion == 'arriba':
            nueva_coordenada = (jugador[0] - 1, jugador[1])
        elif accion == 'derecha':
            nueva_coordenada = (jugador[0], jugador[1] + 1)
        elif accion == 'izquierda':
            nueva_coordenada = (jugador[0], jugador[1] - 1)

        return nueva_coordenada

    def lista_a_tupla(lista):
        return tuple(lista)

    # listado coordenadas cajas (tupla de tuplas),  posicion jugador, cantidad de movimientos máximos)
    INITIAL = (lista_a_tupla(cajas), jugador, maximos_movimientos)

    class SokobanProblem(SearchProblem):
        def cost(self, state1, action, state2):
            return 1

        def is_goal(self, state):
            boxes, jugador, mov_restantes = state
            # Sera objetivo cuando las coordenadas de las cajas esten en la lista de objetivos.
            # Siempre y cuando los maximos movientos no se hayan alcanzado

            for caja in boxes:
                if caja not in objetivos:
                    return False

            if mov_restantes < 0:
                return False

            return True

        def actions(self, state):
            acciones_disponibles = []
            boxes, jugador, mov_restantes = state

            for accion in ACTIONS:

                if movimiento_valido(jugador, accion, boxes):
                    acciones_disponibles.append(accion)

            return tuple(acciones_disponibles)


        def result(self, state, action):
            boxes, jugador, mov_restantes = state

            new_jugador_coord = nueva_coordenada(jugador,action)

            mov_restantes = mov_restantes -1

            new_cajas = []
            #Verificar si la nueva posición hace mover una caja
            if new_jugador_coord in boxes:
                new_boxes = []
                for caja in boxes:
                    new_caja_coord = caja
                    if new_jugador_coord == caja:
                        new_caja_coord = nueva_coordenada(caja,action)
                    new_boxes.append(new_caja_coord)
            else:
                new_boxes = boxes

            return (lista_a_tupla(new_boxes), new_jugador_coord, mov_restantes)

                        

        def heuristic(self, state):
            boxes, jugador, mov_restantes = state
            #La heuristica sera suma de la distancia manhattan de cada caja con su objetivo mas cercano
            distancia = 0
            boxes = lista_a_tupla(boxes)
            for caja in boxes:
                distancia_caja = distancia_objetivo_cercano(caja)
                distancia += distancia_caja
            return distancia

    if __name__ == "__main__":
        viewer = BaseViewer()
        result = astar(SokobanProblem(INITIAL), graph_search=True, viewer=viewer)

        if result is not None:
            print("Estado meta:")
            print(result.state)

            secuencia=[]
            for action, state in result.path():
                if action is not None:
                    print(action)
                    
            return secuencia 

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
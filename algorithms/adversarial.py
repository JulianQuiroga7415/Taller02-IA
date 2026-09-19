from abc import ABC, abstractmethod
import math 
from algorithms.evaluation import evaluation_function
from world.game_state import GameState


class MultiAgentSearchAgent(ABC):
    """Clase base para los agentes de búsqueda adversaria."""

    def __init__(self, depth: int | str = 2) -> None:
        self.depth = int(depth)
        if self.depth < 1:
            raise ValueError("La profundidad debe ser al menos 1 ply")
        self.nodes_evaluated = 0

    @abstractmethod
    def get_action(self, state: GameState) -> str | None:
        raise NotImplementedError


class MinimaxAgent(MultiAgentSearchAgent):
    """Agente Minimax para el defensor MAX frente al intruso MIN."""

    def get_action(self, state: GameState) -> str | None:
        """
        Para mi primera version del codigo se utilizo el pseudocodigo proporcionado en el libro:

            jugador = 0

            def valor_max(estado):
                if estado.is_win() or estado.is_lose():
                    return self.utilidad(estado, jugador), None
                v = -math.inf
                for a in estado.get_legal_actions(0):
                    v2, a2 = valor_min(estado.generate_successor(0, a))
                    if v2 > v:
                        v, movimiento = v2, a
                return v, movimiento

            def valor_min(estado):
                if estado.is_win() or estado.is_lose():
                    return self.utilidad(estado, jugador), None
                v = math.inf
                for a in estado.get_legal_actions(1):
                    v2, a2 = valor_max(estado.generate_successor(1, a))
                    if v2 < v:
                        v, movimiento = v2, a
                return v, movimiento

            valor, movimiento = valor_max(state)
            return movimiento

        Pero al tratar de ejecutar esta version salian errores entonces se recurrio el uso de
        un agente inteligente para poder arreglarlos utilizando como prompt:
        (Mira mi codigo de implementacion de una funcion MiniMax [codigo de arriba] al ejecutarla me salen errores, podrias ayudarme
        a corregirlo y explicarme los cambios realizados?)

        A lo que el agente respondio:

        1. No tiene límite de profundidad. En este juego los agentes
           pueden quedarse quietos o devolverse, así que los estados se repiten
           y la recursión nunca termina (RecursionError). Además ignora
           self.depth.

        2. self.utilidad(estado, jugador) no existe en el proyecto. En los
           estados terminales y en los cortes se debe usar evaluation_function,
           que ya retorna +1000 / -1000 para victoria / derrota. La variable
           jugador sobra, porque el valor siempre se mide desde MAX.

        3. No reinicia ni incrementa self.nodes_evaluated, así que no se pueden
           medir los nodos explorados que piden los puntos 4d y 5c.

        4. Si un estado no tiene acciones legales, movimiento nunca se asigna
           y se produce UnboundLocalError.

        5. Los índices 0 y 1 quedan fijos en cada función. Es más claro
           calcular el siguiente agente con (agente + 1) % num_agents.

        Luego se aplicaron las correciones indicadas por el agente y el código ya corre y funciona de manera adecuada
        """
        self.nodes_evaluated = 0
        num_agents = state.get_num_agents()

        def es_corte(estado, profundidad):
            return estado.is_win() or estado.is_lose() or profundidad == 0

        def valor(estado, agente, profundidad):
            if agente == 0:
                return valor_max(estado, profundidad)
            return valor_min(estado, agente, profundidad)

        def valor_max(estado, profundidad):
            self.nodes_evaluated += 1

            if es_corte(estado, profundidad):
                return evaluation_function(estado), None

            acciones = estado.get_legal_actions(0)
            if not acciones:
                return evaluation_function(estado), None

            v, movimiento = -math.inf, None
            siguiente = 1 % num_agents
            for a in acciones:
                sucesor = estado.generate_successor(0, a)
                v2, _ = valor(sucesor, siguiente, profundidad - 1)
                if v2 > v:
                    v, movimiento = v2, a
            return v, movimiento

        def valor_min(estado, agente, profundidad):
            self.nodes_evaluated += 1
            if es_corte(estado, profundidad):
                return evaluation_function(estado), None
            acciones = estado.get_legal_actions(agente)
            if not acciones:
                return evaluation_function(estado), None
            v, movimiento = math.inf, None
            siguiente = (agente + 1) % num_agents
            for a in acciones:
                sucesor = estado.generate_successor(agente, a)
                v2, _ = valor(sucesor, siguiente, profundidad - 1)
                if v2 < v:  
                    v, movimiento = v2, a
            return v, movimiento

        _, movimiento = valor_max(state, self.depth)
        return movimiento


class AlphaBetaAgent(MultiAgentSearchAgent):
    """Agente Minimax que evita explorar ramas mediante poda alfa-beta."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción de Minimax aplicando poda alfa-beta.

        Debe usar la misma profundidad, orden de acciones y función de
        evaluación que Minimax.

        Tips:
        - Conserve la misma estructura y casos base de MinimaxAgent.
        - Inicie alpha en -infinito y beta en +infinito, y páselos en las
          llamadas recursivas.
        - En MAX actualice alpha y corte si valor >= beta; en MIN actualice beta
          y corte si valor <= alpha.
        """
        """self.nodes_evaluated = 1
        if state.is_win() or state.is_lose():
            return None
        memoria=state.get_legal_actions(0)
        if not memoria:
            return None
          
        def valor(estado:GameState, agente:int, profundidad:int, alfa:float, beta:float)->float:
          self.nodes_evaluated+=1
          if estado.is_win() or estado.is_lose() or profundidad== 0:
            return evaluation_function(estado)
          memoriamain=estado.get_legal_actions(agente)
          if not memoriamain:
            return evaluation_function(estado)
          siguiente_revision =(agente+1)%estado.get_num_agents()
          if agente==0:
            estado_new= float("-inf")
            for j in memoriamain:
              elegido = estado.generate_successor(agente,j)
              estado_new=max(estado_new,valor(elegido,siguiente_revision,profundidad-1,alfa,beta))
              if estado_new>= beta:
                return estado_new
              alfa=max(alfa,estado_new)
            return estado_new
            este fue mi codigo inicial, logre adelantar gran parte incluyendo la funcion valor y la rama de max,
            pero la verdad no supe si hacer min era igual que hacer max o si algo debia cambiar asi que preferi
            preguntarle a chat de esta manera confirmo que voy por buen camino y evito errores complicados a futuro.
            le mande el siguiente prompt bro llevo esto hecho de alfa beta voy bien? que me recomiendas agregar al codigo?
            a lo que chat me respondio 
            Vas muy bien brotha. Ya hiciste correctamente:

            Conteo de la raíz.
            Estados terminales.
            Corte por profundidad.
            Alternancia entre agentes.
            Rama de MAX.
            Actualización de alfa.
            Poda cuando estado_new >= beta.

            Te falta la rama de MIN y después seleccionar la acción desde la raíz.
            Te recomiendo hacer lo mismo que hiciste en la rama de MAX, pero con las condiciones invertidas para MIN. Es decir, en lugar de buscar el máximo valor, buscarás el mínimo valor y actualizarás beta en lugar de alfa. Además, asegúrate de manejar correctamente la selección de la acción desde la raíz después de calcular los valores para todas las acciones legales del agente MAX.
            por ultimo asegurate de agregar la raiz. Por lo que mi codigo final quedo asi"""
        self.nodes_evaluated = 1
        if state.is_win() or state.is_lose():
            return None
        memoria=state.get_legal_actions(0)
        if not memoria:
            return None
          
        def valor(estado:GameState, agente:int, profundidad:int, alfa:float, beta:float)->float:
          self.nodes_evaluated+=1
          if estado.is_win() or estado.is_lose() or profundidad== 0:
            return evaluation_function(estado)
          memoriamain=estado.get_legal_actions(agente)
          if not memoriamain:
            return evaluation_function(estado)
          siguiente_revision =(agente+1)%estado.get_num_agents()
          if agente==0:
            estado_new= float("-inf")
            for j in memoriamain:
              elegido = estado.generate_successor(agente,j)
              estado_new=max(estado_new,valor(elegido,siguiente_revision,profundidad-1,alfa,beta))
              if estado_new>= beta:
                return estado_new
              alfa=max(alfa,estado_new)
            return estado_new
          estado_new = float("inf")

          for j in memoriamain:
            elegido = estado.generate_successor(agente,j)
            estado_new = min(estado_new,valor(elegido,siguiente_revision,profundidad - 1,alfa,beta))
            if estado_new <= alfa:
                return estado_new
            beta = min(beta,estado_new)
          return estado_new
        mejor_accion = memoria[0]
        mejor_valor = float("-inf")

        alfa = float("-inf")
        beta = float("inf")

        for accion in memoria:

            sucesor = state.generate_successor(0,accion)

            valor_accion = valor(sucesor,1,self.depth - 1,alfa,beta)

            if valor_accion > mejor_valor:
                mejor_valor = valor_accion
                mejor_accion = accion

            alfa = max(alfa,mejor_valor)
        return mejor_accion
            
              

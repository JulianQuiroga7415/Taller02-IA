from abc import ABC, abstractmethod

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
        Retorna la acción del defensor con mayor valor Minimax.

        El defensor es MAX (agente 0), el intruso es MIN (agente 1) y cada
        acción consume un ply. Debe respetar el orden de las acciones legales,
        usar evaluation_function en terminales y cortes, y contar cada estado
        procesado una vez en self.nodes_evaluated, incluida la raíz.

        Tips:
        - Use state.get_legal_actions(agent_index) y
          state.generate_successor(agent_index, action) para expandir el árbol.
        - Compruebe state.is_win(), state.is_lose() y el corte de profundidad;
          evalúe esos estados con evaluation_function(state).
        - El siguiente agente es (agent_index + 1) % state.get_num_agents().
          depth=1 incluye una acción de MAX y depth=2 una de MAX y una de MIN.
        - Reinicie las métricas y cuente una vez cada estado procesado, incluida
          la raíz. Retorne la acción de MAX y conserve la primera en los empates.
        """
        # TODO: Add your code here
        raise NotImplementedError("Punto 4: implemente MinimaxAgent.get_action")


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
            
              

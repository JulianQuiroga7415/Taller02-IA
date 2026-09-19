import math

from world.game_state import GameState


def base_evaluation_function(state: GameState) -> float:
    """
    Retorna la evaluación base entregada para desarrollar el punto 4.

    Esta función no forma parte del código que debe modificar el estudiante y
    permite probar Minimax antes de desarrollar la heurística del punto 5.
    """
    if state.is_win():
        return 1000.0
    if state.is_lose():
        return -1000.0
    return float(state.get_score())


def evaluation_function(state: GameState) -> float:
    """
    Evalúa un estado desde la perspectiva del defensor MAX.

    Debe conservar las utilidades terminales de la evaluación base y diseñar
    una valoración no trivial para estados de corte. Minimax y alfa-beta usan
    esta misma función al comparar sus decisiones en el punto 5.

    Tips:
    - Los estados terminales ya se resuelven antes del bloque TODO; diseñe allí
      únicamente la valoración de estados no terminales.
    - Consulte state.defender_position, state.intruder_position,
      state.pending_terminals, state.get_score() y state.get_legal_actions(0).
    - state.layout.distance(start, goal) calcula y almacena en caché la distancia
      real por el mapa respetando los muros.
    - Maneje conjuntos vacíos y distancias infinitas, y mantenga todo estado no
      terminal estrictamente entre -1000 y +1000.
    """
    """if state.is_win() or state.is_lose():
        return base_evaluation_function(state)

    value=float(state.get_score())
    pemdientes=len(state.pending_terminals)
    value-=40.0*pemdientes
    if state.pending_terminals:
        cercano= min(state.layout.distance(state.defender_position,terminal) 
                     for terminal in state.pending_terminals)
                     
    este fue mi codigo inicial pero la verdad me confundio bastante el tema de
    los calculos para poder conseguir la nota numerica que define el estado actual del juego
    por lo que le pedi a chat que me diera unas pistas,
    brotha ya adelante un poco pero la verdad la parte de los calculos me confunde
    me podria ayudar con tips en aspecto de codigo pero no respuesta general? me respondio De una, sin darte todo completo. Vas aquí:

cercano = min(
    state.layout.distance(
        state.defender_position,
        terminal
    )
    for terminal in state.pending_terminals
)

Ahora piensa: entre más grande sea cercano, peor está el defensor. Entonces debes restarlo:

if math.isinf(cercano):
    value -= ???     # Penalización fuerte si no puede llegar
else:
    value -= ??? * cercano

Siguiente pista: calcula qué tan cerca está el intruso:

distancia_intruso = state.layout.distance(
    state.defender_position,
    state.intruder_position
)

Luego clasifica el peligro:

if distancia_intruso <= 1:
    value -= ???     # Mucho peligro

elif distancia_intruso == 2:
    value -= ???     # Peligro moderado

else:
    value += ???     # Estar lejos es favorable

Pista para movilidad:

movimientos = len(
    state.get_legal_actions(0)
)

Entre más movimientos tenga el defensor, mejor:

value += ??? * movimientos

Finalmente, el taller exige que un estado no terminal nunca alcance 1000 ni -1000:

return max(
    -999.0,
    min(???, value)
)

Valores razonables para experimentar:

Distancia a terminal: 5–10 por casilla
Peligro inmediato: 200–300
Peligro a dos casillas: 75–150
Movilidad: 2–5 por acción     el codigo final quedo asi"""
    
    
    if state.is_win() or state.is_lose():
        return base_evaluation_function(state)
    value = float(state.get_score())
    cerquita = len(state.pending_terminals)
    value -= 40.0 * cerquita
    if state.pending_terminals:
        cercano = min(state.layout.distance(state.defender_position, terminal) for terminal in state.pending_terminals)
        if math.isinf(cercano):
            value -= 250.0
        else:
            value -= 8.0 * cercano
    distancia_intruso = state.layout.distance(state.defender_position, state.intruder_position)
    if math.isinf(distancia_intruso):
        value += 80.0
    elif distancia_intruso <= 1:
        value -= 250.0
    elif distancia_intruso == 2:
        value -= 100.0
    else:
        value += 4.0 * min(distancia_intruso, 15)
    movilidad = max(0, len(state.get_legal_actions(0)) - 1)
    value += 3.0 * movilidad
    return max(-999.0, min(999.0, value))
        

import math
import random

from optimization.problem import SmartGridOptimizationProblem
from optimization.result import Configuration, OptimizationResult


def configuration_score(
    problem: SmartGridOptimizationProblem, configuration: Configuration
) -> float:
    """
    Combina cobertura, redundancia y exposición en un puntaje a maximizar.

    Tips:
    - Use problem.score_components(configuration); ya retorna cobertura,
      redundancia y exposición en ese orden.
    """
    # TODO: Add your code here
    valores=problem.score_components(configuration)
    cobertura, redundancia, exposicion = valores
    puntaje=cobertura-redundancia-exposicion
    return puntaje
    raise NotImplementedError("Punto 1: implemente configuration_score")


def hill_climbing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    max_iterations: int = 500,
) -> OptimizationResult:
    """
    Ejecuta ascenso de colina con mejora estricta.

    Debe examinar todos los vecinos, seleccionar el de mayor puntaje y
    conservar el orden entregado por el problema para desempatar. La búsqueda
    termina cuando no existe una mejora estricta o se alcanza el límite.

    Tips:
    - problem.neighbors(current) retorna vecinos válidos en el orden que debe
      usarse para desempatar.
    - Cada llamada a configuration_score(...) cuenta como una evaluación.
    - Inicialice los historiales con la configuración inicial y agregue solo las
      mejoras aceptadas antes de retornar el OptimizationResult.
    """
    """
    Este era mi codigo inicial 
    
    inicial=initial_configuration
        puntaje_inicial=configuration_score(problem, inicial)
        contador=0
        history=[inicial]
        score_history=[puntaje_inicial]
        puntaje_mejor=-100000000
        while contador<max_iterations:
            vecinos=problem.neighbors(inicial)
            for vecino in vecinos:
                if configuration_score(problem, vecino)>puntaje_mejor:
                    puntaje_mejor=configuration_score(problem, vecino)
                    mejor_vecino=vecino
            if puntaje_mejor>puntaje_inicial:
                inicial=mejor_vecino
                puntaje_inicial=puntaje_mejor
                contador+=1
                history.append(inicial)
                score_history.append(puntaje_inicial)
            else:
                break
        return OptimizationResult(inicial, puntaje_inicial, contador, history, score_history)
        
    Se lo mandé a Claude y me dijo que
    1. Estás llamando configuration_score dos veces por vecino
    if configuration_score(problem, vecino)>puntaje_mejor:
        puntaje_mejor=configuration_score(problem, vecino)

    Aquí calculas el puntaje del mismo vecino dos veces cuando la condición es verdadera (una en el if, otra dentro). 
    Eso infla artificialmente tu contador de evaluaciones — y encima, no tienes ningún contador de evaluaciones en tu código. 
    Necesitas:
    Guardar el resultado de configuration_score(problem, vecino) en una variable una sola vez por vecino.
    Sumar 1 a un contador de evaluaciones cada vez que llamas esa función (o sea, una vez por cada vecino recorrido, sin importar si mejora o no).
    
    2. puntaje_mejor y mejor_vecino no se reinician en cada vuelta del while
    Los inicializas una sola vez, antes del while. Eso significa que cuando entras a la segunda vuelta del bucle, puntaje_mejor todavía tiene el valor 
    de la ronda anterior en lugar de empezar de cero para buscar el máximo entre los nuevos vecinos. Aunque en este caso particular "funciona por casualidad" 
    (porque puntaje_mejor termina quedando igual a puntaje_inicial justo antes), es frágil y confuso. 
    Debes reiniciar dentro del while, al principio de cada ronda, antes del for:
    puntaje_mejor a un valor muy bajo (como tienes, -100000000, o mejor usa float('-inf')).
    mejor_vecino a algo como None.
    
    Entonces corregí estas dos cosas en mi código
    """
    # TODO: Add your code here
    inicial=initial_configuration
    puntaje_inicial=configuration_score(problem, inicial)
    contador=0
    history=[inicial]
    score_history=[puntaje_inicial]
    
    evaluaciones=1
    while contador<max_iterations:
        vecinos=problem.neighbors(inicial)
        puntaje_mejor=-1000000000000000000
        mejor_vecino=None
        for vecino in vecinos:
            puntaje_vecino=configuration_score(problem, vecino)
            evaluaciones+=1
            if puntaje_vecino>puntaje_mejor:
                puntaje_mejor=puntaje_vecino
                mejor_vecino=vecino
        if puntaje_mejor>puntaje_inicial:
            inicial=mejor_vecino
            puntaje_inicial=puntaje_mejor
            contador+=1
            history.append(inicial)
            score_history.append(puntaje_inicial)
        else:
            break
    return OptimizationResult(inicial, puntaje_inicial, evaluaciones, contador, history, score_history)
            
    
    raise NotImplementedError("Punto 1: implemente hill_climbing")


def cooling_schedule(initial_temperature: float, cooling_rate: float, iteration: int) -> float:
    """
    Retorna el programa geométrico T(t) = T0 * alpha**t.

    Esta función se invoca desde simulated_annealing en cada iteración.
    """
    # TODO: Add your code here
    raise NotImplementedError("Punto 2: implemente cooling_schedule")


def simulated_annealing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    initial_temperature: float = 20.0,
    cooling_rate: float = 0.97,
    max_iterations: int = 500,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta recocido simulado para un problema de maximización.

    Debe proponer un vecino aleatorio por iteración, aceptar siempre las
    mejoras y aplicar exp(delta / temperature) en los demás casos. El estado
    actual y el mejor estado encontrado deben conservarse por separado.

    Tips:
    - Seleccione el candidato con rng.choice(problem.neighbors(current)) y use
      exclusivamente rng para conservar la reproducibilidad.
    - Obtenga la temperatura con cooling_schedule(...) y calcule la aceptación
      con delta = puntaje_candidato - puntaje_actual y math.exp(...).
    - Mantenga separados el estado actual y el mejor encontrado; registre el
      estado actual después de cada intento, incluso si se rechaza.
    - Detenga la ejecución cuando la temperatura alcance minimum_temperature.
    """
    rng = rng or random.Random()
    minimum_temperature = 1e-9

    # TODO: Add your code here
    raise NotImplementedError("Punto 2: implemente simulated_annealing")


def one_point_crossover(
    parent1: Configuration, parent2: Configuration, rng: random.Random
) -> tuple[Configuration, Configuration]:
    """
    Realiza un cruce de un punto y retorna dos descendientes.

    La reparación de la cantidad de módulos se realiza posteriormente.

    Tips:
    - Seleccione con rng un corte interior, entre las posiciones 1 y len-1.
    - Cada descendiente combina el prefijo de un padre con el sufijo del otro.
    - Retorne tuplas y no repare aquí los descendientes.
    """
    if len(parent1) != len(parent2):
        raise ValueError("Los padres deben tener la misma longitud")
    if len(parent1) < 2:
        return parent1, parent2

    # TODO: Add your code here
    raise NotImplementedError("Punto 3: implemente one_point_crossover")


def swap_mutation(
    individual: Configuration, mutation_probability: float, rng: random.Random
) -> Configuration:
    """
    Aplica mutación por intercambio con la probabilidad indicada.

    Cuando ocurre una mutación, intercambia un bit activo y uno inactivo para
    conservar la cantidad de módulos instalados.

    Tips:
    - Use rng.random() para decidir si se aplica la mutación.
    - Identifique por separado los índices activos e inactivos y seleccione uno
      de cada grupo con rng.choice(...).
    - Si alguno de los dos grupos está vacío, no hay un intercambio posible.
    - Retorne una tupla nueva; no modifique el individuo recibido.
    """
    # TODO: Add your code here
    raise NotImplementedError("Punto 3: implemente swap_mutation")


def genetic_algorithm(
    problem: SmartGridOptimizationProblem,
    population_size: int = 40,
    generations: int = 100,
    mutation_probability: float = 0.05,
    elite_size: int = 2,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta un algoritmo genético generacional.

    Debe integrar la población inicial, la selección por torneo, el cruce, la
    reparación, la mutación y el elitismo entregados por el proyecto. Retorna
    el mejor individuo encontrado durante toda la ejecución.

    Tips:
    - Use problem.initial_population(...), problem.tournament_select(...) y
      problem.repair_configuration(...) para las operaciones ya entregadas.
    - Aplique one_point_crossover(...) antes de reparar y swap_mutation(...)
      después de la reparación.
    - Conserve los mejores individuos por elitismo y registre en los historiales
      el mejor global de cada generación.
    """
    rng = rng or random.Random()
    if population_size < 2:
        raise ValueError("La población debe tener al menos dos individuos")
    if generations < 0:
        raise ValueError("El número de generaciones no puede ser negativo")
    if not 0.0 <= mutation_probability <= 1.0:
        raise ValueError("La probabilidad de mutación debe estar entre 0 y 1")
    if not 0 <= elite_size <= population_size:
        raise ValueError("elite_size debe estar entre 0 y population_size")

    # TODO: Add your code here
    raise NotImplementedError("Punto 3: implemente genetic_algorithm")

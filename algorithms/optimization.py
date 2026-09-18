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
    return initial_temperature * (cooling_rate ** iteration)


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
    
    Aproximación inicial del codigo hecha por mi, en esta me base a partir del contexto del enunciado y del pseudocodigo brindado en clase
    
    rng = rng or random.Random()
    minimum_temperature = 1e-9
    actual = initial_configuration
    t = initial_temperature
    mejor = actual
    for i in range (max_iterations):
        temperatura = cooling_schedule(t, cooling_rate, i )
        if temperatura == 0:
            return mejor
        else:
            siguiente = rng.choice(problem.neighbors(actual))
            diferencia = configuration_score(problem,siguiente) - configuration_score(problem,actual)
            if diferencia > 0:
                actual = siguiente
            else:
                probabilidad = math.exp(diferencia / temperatura)
                if rng.random() < probabilidad:
                    actual = siguiente
            if configuration_score(problem,actual) > configuration_score(problem, mejor):
                mejor = actual
                
    return mejor
                
    A partir de esto decidi pasarle a claude mi codigo para que me brindara retroalimentación y me pudiera ayudar a identificar posibles errores sin darme directamente el codigo
    El prompt usado fue: Hola claude, tengo el siguiente codigo de recocido simulado, me podrias brindar retroalimentacion de su funcionamiento y los posibles errores del mismo sin darme el codigo resuelto            
                
    Esto fue lo que me contesto la IA:
    
    Dale, vamos por partes — te señalo dónde están los problemas y te dejo preguntas guía para que tú mismo llegues a la corrección.

    1. La condición de parada por temperatura
    Sigue siendo if temperatura == 0. Pregúntate: ¿con una fórmula T0 * alpha^i, existe algún i para el cual el resultado sea matemáticamente igual a cero? ¿O simplemente se hace cada vez más pequeño sin tocar nunca el cero? Tienes una variable minimum_temperature definida arriba que no estás usando en ningún lado — esa es la pista de qué deberías comparar en vez de 0.

    2. El tipo de retorno
    Mira la firma de la función: -> OptimizationResult. Ahora mismo tu return mejor entrega una Configuration, no un OptimizationResult. Pregúntate:

    ¿Qué campos tiene la clase OptimizationResult? (deberías ir a mirar optimization/result.py, que el enunciado dice que puedes consultar aunque no modificar).
    De esos campos, ¿cuáles ya tienes disponibles en tu función (mejor, su puntaje) y cuáles te falta ir armando a lo largo del loop (evaluaciones contadas, iteraciones contadas, historial)?
    ¿En qué momento del loop tendría sentido ir agregando cada paso al historial?

    3. Evaluaciones repetidas
    Cuenta cuántas veces llamas configuration_score en una sola vuelta del for. ¿Ese número te parece necesario, o hay algún resultado que ya calculaste antes y podrías guardar en una variable para reusarlo más abajo, en vez de volver a pedirlo?

    4. Un detalle que no habíamos visto: ¿qué pasa si nunca se cumple la parada por temperatura?
    Si el for corre las max_iterations completas sin que la temperatura baje del mínimo, ¿tu función también retorna algo correcto al final, o solo cubriste el caso del return de en medio? (Esto se conecta directo con el punto 2 — vas a necesitar construir el OptimizationResult en más de un lugar, o reorganizar la lógica para que solo haya un punto de salida).

    Tómate estos cuatro puntos, intenta resolverlos, y me muestras la siguiente versión.
    
    Luego de revisar esos errores y verificar cosas como que el tipo de retorno de la funcion debia ser un OptimizationResult, este fue mi algoritmo final.
    
    """
    rng = rng or random.Random()
    minimum_temperature = 1e-9
    actual = initial_configuration
    t = initial_temperature
    mejor = actual
    evaluations = 0
    iterations = 0
    history = []
    score_history = []
    score_mejor = configuration_score(problem, mejor)
    evaluations += 1
    for i in range (max_iterations):
        temperatura = cooling_schedule(t, cooling_rate, i )
        score_actual = configuration_score(problem, actual)
        evaluations += 1
        if temperatura <= minimum_temperature:
            iterations = i
            break
        else:
            siguiente = rng.choice(problem.neighbors(actual))
            score_siguiente = configuration_score(problem, siguiente)
            evaluations += 1
            diferencia = score_siguiente - score_actual
            
            if diferencia > 0:
                actual = siguiente
                score_actual = score_siguiente
            else:
                probabilidad = math.exp(diferencia / temperatura)
                
                if rng.random() < probabilidad:
                    actual = siguiente
                    score_actual = score_siguiente
          
            if score_actual > score_mejor:
                mejor = actual
                score_mejor = score_actual
            
            history.append(actual)    
            score_history.append(score_actual)
            
        iterations = i + 1
                    
    return OptimizationResult(mejor, score_mejor, evaluations, iterations, history, score_history)   



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

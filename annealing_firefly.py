import math
from statistics import median

import numpy as np


METHODS = {
    'production_method': ('Green', 'SMR', 'ATR', 'CCS'),
    'transport_method': ('Pipeline', 'Truck', 'LiquefiedTruck'),
}


def estimate_temperature(solutions, fitness, params, target):
    if not 0 < target < 1:
        raise ValueError('target acceptance must be between 0 and 1')
    uphill = []
    for solution in solutions:
        current = fitness(solution, params)
        for field, choices in METHODS.items():
            for method in choices:
                if method == solution[field]:
                    continue
                delta = fitness({**solution, field: method}, params) - current
                if delta > 0:
                    uphill.append(delta)
    return -median(uphill) / math.log(target) if uphill else 1.0


def cooling_rate(alpha, r_min, r_max, acceptance, step, steps, distance, max_distance):
    if not 0 < alpha < 1 or steps <= 0 or max_distance <= 0:
        raise ValueError('invalid base cooling rate or scale')
    correction = 1.05 if acceptance < r_min else 0.95 if acceptance > r_max else 1.0
    exponent = correction ** -1 * (1 + max(step, 0) / steps) / (1 + max(distance, 0) / max_distance)
    return min(alpha ** exponent, 0.999)


def propose(current, brighter, rng, beta0, gamma, mutation):
    candidate = current.copy()
    if brighter is not None:
        distance = sum(current[field] != brighter[field] for field in METHODS) / len(METHODS)
        attraction = beta0 * math.exp(-gamma * distance ** 2)
        for field in METHODS:
            if current[field] != brighter[field] and rng.random() < attraction:
                candidate[field] = brighter[field]
    for field, choices in METHODS.items():
        if rng.random() < mutation:
            alternatives = tuple(method for method in choices if method != candidate[field])
            candidate[field] = alternatives[int(rng.integers(len(alternatives)))]
    return candidate


def accept(delta, temperature, rng):
    return delta <= 0 or rng.random() < math.exp(-delta / temperature)


def search(initial, fitness, params, temperature, alpha, *, seed=None, iterations=1000,
           patience=200, beta0=1.0, gamma=1.0, mutation=0.2, progress=False):
    if not math.isfinite(temperature) or temperature <= 0 or not 0 < alpha < 1:
        raise ValueError('temperature must be finite and positive, and 0 < alpha < 1')
    if iterations < 1 or patience < 1 or not (0 <= beta0 <= 1 and 0 <= mutation <= 1 and math.isfinite(gamma) and gamma >= 0):
        raise ValueError('invalid iteration or firefly parameters')
    population = [dict(solution) for solution in initial]
    if not population:
        raise ValueError('initial population cannot be empty')
    for solution in population:
        if any(solution.get(field) not in options for field, options in METHODS.items()):
            raise ValueError('invalid production or transport method')
    scores = [fitness(solution, params) for solution in population]
    if not all(math.isfinite(score) for score in scores):
        raise ValueError('fitness must be finite')
    best = min(range(len(population)), key=scores.__getitem__)
    best_solution, best_score = population[best].copy(), scores[best]
    rng = np.random.default_rng(seed)
    stagnant = 0
    for step in range(1, iterations + 1):
        previous_score = best_score
        next_population, next_scores = [], []
        for current, score in zip(population, scores):
            quantities = current['production_quantity'], current['transport_quantity']
            brighter = [peer for peer, value in zip(population, scores) if value < score
                        and (peer['production_quantity'], peer['transport_quantity']) == quantities]
            guide = brighter[int(rng.integers(len(brighter)))] if brighter else None
            candidate = propose(current, guide, rng, beta0, gamma, mutation)
            new_score = fitness(candidate, params)
            if not math.isfinite(new_score):
                raise ValueError('fitness must be finite')
            if accept(new_score - score, temperature, rng):
                current, score = candidate, new_score
            next_population.append(current)
            next_scores.append(score)
            if score < best_score:
                best_solution, best_score = current.copy(), score
        population, scores = next_population, next_scores
        if progress and (step == 1 or step % 100 == 0):
            print(f'Iteration: {step}, Best Fitness: {best_score}, Temperature: {temperature}')
        temperature = max(temperature * alpha, np.finfo(float).tiny)
        stagnant = stagnant + 1 if best_score == previous_score else 0
        if stagnant >= patience:
            break
    if progress:
        print(f'Total Iterations: {step}, Best Fitness: {best_score}')
    return best_solution

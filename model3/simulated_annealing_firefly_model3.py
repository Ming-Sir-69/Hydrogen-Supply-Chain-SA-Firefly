import argparse

from adaptive_cooling_rate import adaptive_cooling_rate
from adaptive_initial_temperature import adaptive_initial_temperature
from calculate_fitness_model3 import calculate_fitness_wrapper
from generate_initial_solutions import generate_initial_solutions
from annealing_firefly import search


def run_simulated_annealing_firefly(initial_solutions, params, T_0, alpha, *, seed=None):
    return search(initial_solutions, calculate_fitness_wrapper, params, T_0, alpha,
                  seed=seed, progress=True)


if __name__ == "__main__":
    from initialize_parameters import get_initial_parameters

    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int)
    args = parser.parse_args()
    params = get_initial_parameters()
    initial_solutions = generate_initial_solutions(params)
    T_0 = adaptive_initial_temperature(len(initial_solutions), 0.66, params)
    alpha = adaptive_cooling_rate(0.995, 0.1, 0.9, 0.5, 10, 100, 500, 1000)
    best_solution = run_simulated_annealing_firefly(initial_solutions, params, T_0, alpha, seed=args.seed)
    print('Best Solution:')
    print(best_solution)

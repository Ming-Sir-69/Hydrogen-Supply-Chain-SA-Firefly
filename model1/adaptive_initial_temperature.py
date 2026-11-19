from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from annealing_firefly import estimate_temperature
from calculate_fitness_model1 import calculate_fitness_wrapper
from generate_initial_solutions import generate_initial_solutions


def adaptive_initial_temperature(num_solutions, target_acceptance_rate, params, tolerance=0.01):
    return estimate_temperature(generate_initial_solutions(params), calculate_fitness_wrapper,
                                params, target_acceptance_rate)


if __name__ == "__main__":
    from initialize_parameters import get_initial_parameters

    params = get_initial_parameters()
    print(f"Adjusted Initial Temperature: {adaptive_initial_temperature(12, 0.66, params)}")

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from annealing_firefly import cooling_rate


def adaptive_cooling_rate(alpha, r_min, r_max, current_acceptance_rate, t, N, d, D_max):
    return cooling_rate(alpha, r_min, r_max, current_acceptance_rate, t, N, d, D_max)


if __name__ == "__main__":
    print(f"Adjusted Cooling Rate: {adaptive_cooling_rate(0.95, 0.1, 0.9, 0.5, 10, 100, 500, 1000)}")

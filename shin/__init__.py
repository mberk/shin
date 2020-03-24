from math import sqrt
from typing import Sequence


def calculate_implied_probabilities(
        odds: Sequence[float],
        max_iterations: int = 1000,
        convergence_threshold: float = 1e-12) -> dict:
    if any(o < 1 for o in odds):
        raise ValueError('All odds must be >= 1')

    z = 0
    n = len(odds)
    inverse_odds = [1.0 / o for o in odds]
    sum_inverse_odds = sum(inverse_odds)
    delta = float('Inf')
    iterations = 0

    while delta > convergence_threshold and iterations < max_iterations:
        z0 = z
        z = (sum(sqrt(z ** 2 + 4 * (1 - z) * io ** 2 / sum_inverse_odds) for io in inverse_odds) - 2) / (n - 2)
        delta = abs(z - z0)
        iterations += 1

    p = [(sqrt(z ** 2 + 4 * (1 - z) * io ** 2 / sum_inverse_odds) - z) / (2 * (1 - z)) for io in inverse_odds]
    return {
        'implied_probabilities': p,
        'iterations': iterations,
        'delta': delta,
        'z': z
    }

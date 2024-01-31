from __future__ import annotations

from collections.abc import Collection
from collections.abc import Mapping
from math import sqrt
from typing import Any

from .shin import optimise as _optimise_rust


def _optimise(
    inverse_odds: list[float],
    sum_inverse_odds: float,
    n: int,
    max_iterations: int = 1000,
    convergence_threshold: float = 1e-12,
) -> tuple[float, float, float]:
    delta = float("Inf")
    z = 0.0
    iterations = 0
    while delta > convergence_threshold and iterations < max_iterations:
        z0 = z
        z = (
            sum(
                sqrt(z**2 + 4 * (1 - z) * io**2 / sum_inverse_odds)
                for io in inverse_odds
            )
            - 2
        ) / (n - 2)
        delta = abs(z - z0)
        iterations += 1
    return z, delta, iterations


def calculate_implied_probabilities(
    odds: Collection[float] | Mapping[Any, float],
    max_iterations: int = 1000,
    convergence_threshold: float = 1e-12,
    full_output: bool = False,
    force_python_optimiser: bool = False,
) -> dict[str, Any] | list[float] | dict[Any, float]:
    odds_seq = odds.values() if isinstance(odds, Mapping) else odds

    if len(odds_seq) < 2:
        raise ValueError("len(odds) must be >= 2")

    if any(o < 1 for o in odds_seq):
        raise ValueError("All odds must be >= 1")

    optimise = _optimise if force_python_optimiser else _optimise_rust

    n = len(odds_seq)
    inverse_odds = [1.0 / o for o in odds_seq]
    sum_inverse_odds = sum(inverse_odds)

    if n == 2:
        diff_inverse_odds = inverse_odds[0] - inverse_odds[1]
        z = ((sum_inverse_odds - 1) * (diff_inverse_odds**2 - sum_inverse_odds)) / (
            sum_inverse_odds * (diff_inverse_odds**2 - 1)
        )
        delta = 0.0
        iterations = 0.0
    else:
        z, delta, iterations = optimise(
            inverse_odds=inverse_odds,
            sum_inverse_odds=sum_inverse_odds,
            n=n,
            max_iterations=max_iterations,
            convergence_threshold=convergence_threshold,
        )

    p: list[float] | dict[Any, float] = [
        (sqrt(z**2 + 4 * (1 - z) * io**2 / sum_inverse_odds) - z) / (2 * (1 - z))
        for io in inverse_odds
    ]
    if isinstance(odds, Mapping):
        p = {k: v for k, v in zip(odds, p)}

    if full_output:
        return {
            "implied_probabilities": p,
            "iterations": iterations,
            "delta": delta,
            "z": z,
        }
    else:
        return p

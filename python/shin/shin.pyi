def optimise(
    inverse_odds: list[float],
    sum_inverse_odds: float,
    n: int,
    max_iterations: int = 1000,
    convergence_threshold: float = 1e-12,
) -> tuple[float, float, float]:
    ...

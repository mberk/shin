from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import sqrt
from typing import Any, Generic, Literal, TypeVar, overload

from .shin import optimise as _optimise_rust

T = TypeVar("T")
OutputT = TypeVar("OutputT", bound="list[float] | dict[Any, float]")


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


@dataclass
class ShinOptimisationDetails(Generic[OutputT]):
    implied_probabilities: OutputT
    iterations: float
    delta: float
    z: float

    @overload
    def __getitem__(self, key: Literal["implied_probabilities"]) -> OutputT: ...

    @overload
    def __getitem__(self, key: Literal["iterations"]) -> float: ...

    @overload
    def __getitem__(self, key: Literal["delta"]) -> float: ...

    @overload
    def __getitem__(self, key: Literal["z"]) -> float: ...

    def __getitem__(
        self, key: Literal["implied_probabilities", "iterations", "delta", "z"]
    ) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)


# sequence input, full output False
@overload
def calculate_implied_probabilities(
    odds: Sequence[float],
    *,
    max_iterations: int = ...,
    convergence_threshold: float = ...,
    full_output: Literal[False] = False,
    force_python_optimiser: bool = ...,
) -> list[float]: ...


# mapping, full output False
@overload
def calculate_implied_probabilities(
    odds: Mapping[T, float],
    *,
    max_iterations: int = ...,
    convergence_threshold: float = ...,
    full_output: Literal[False] = False,
    force_python_optimiser: bool = ...,
) -> dict[T, float]: ...


# sequence, full output True
@overload
def calculate_implied_probabilities(
    odds: Sequence[float],
    *,
    max_iterations: int = ...,
    convergence_threshold: float = ...,
    full_output: Literal[True],
    force_python_optimiser: bool = ...,
) -> ShinOptimisationDetails[list[float]]: ...


# mapping, full output True
@overload
def calculate_implied_probabilities(
    odds: Mapping[T, float],
    *,
    max_iterations: int = ...,
    convergence_threshold: float = ...,
    full_output: Literal[True],
    force_python_optimiser: bool = ...,
) -> ShinOptimisationDetails[dict[T, float]]: ...


def calculate_implied_probabilities(
    odds: Sequence[float] | Mapping[T, float],
    *,
    max_iterations: int = 1000,
    convergence_threshold: float = 1e-12,
    full_output: bool = False,
    force_python_optimiser: bool = False,
) -> (
    ShinOptimisationDetails[list[float]]
    | ShinOptimisationDetails[dict[T, float]]
    | list[float]
    | dict[T, float]
):
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

    p_gen = (
        (sqrt(z**2 + 4 * (1 - z) * io**2 / sum_inverse_odds) - z) / (2 * (1 - z))
        for io in inverse_odds
    )
    if isinstance(odds, Mapping):
        d = {k: v for k, v in zip(odds, p_gen)}
        if full_output:
            return ShinOptimisationDetails(
                implied_probabilities=d,
                iterations=iterations,
                delta=delta,
                z=z,
            )
        return d

    l = list(p_gen)
    if full_output:
        return ShinOptimisationDetails(
            implied_probabilities=l,
            iterations=iterations,
            delta=delta,
            z=z,
        )
    return l

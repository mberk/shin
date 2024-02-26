# shin

A Python implementation of Shin's method [[1](#1), [2](#2)] for calculating implied probabilities from bookmaker odds.

Probabilities calculated in this way have been shown to be more accurate than those obtained by the standard approach
of dividing the inverse odds by the booksum [[3](#3)].

# Installation

Requires Python 3.9 or above.

```
pip install shin
```

# Usage

```python
import shin

shin.calculate_implied_probabilities([2.6, 2.4, 4.3])
```

```
[0.37299406033208965, 0.4047794109200184, 0.2222265287474275]
```

Shin's method assumes there is some unknown proportion of bettors that are insiders, `z`, and this proportion along with
the implied probabilities can be estimated using an iterative procedure described in [[4](#4)].

Diagnostic information from the iterative procedure can be obtained by setting the `full_output` argument to `True`:

```python
import shin

shin.calculate_implied_probabilities([2.6, 2.4, 4.3], full_output=True)
```

```
ShinOptimisationDetails(
    implied_probabilities=[0.37299406033208965, 0.4047794109200184, 0.2222265287474275],
    iterations=426,
    delta=9.667822098435863e-13,
    z=0.01694251276407055
)
```

The returned object contains the following fields:

* `implied_probablities`
* `iterations` - compare this value to the `max_iterations` argument (default = `1000`) to check for failed convergence
* `delta` - the final change in `z` for the final iteration. Compare with the `convergence_threshold` argument
  (default = `1e-12`) to assess convergence
* `z` - the estimated proportion of theoretical betting volume coming from insider traders

When there are only two outcomes, `z` can be calculated analytically [[3](#3)]. In this case, the `iterations` and
`delta` fields of the returned `dict` are `0` to reflect this:

```python
import shin

shin.calculate_implied_probabilities([1.5, 2.74], full_output=True)
```

```
ShinOptimisationDetails(
    implied_probabilities=[0.6508515815085157, 0.3491484184914841],
    iterations=0.0,
    delta=0.0,
    z=0.03172728540646625
)
```

Note that with two outcomes, Shin's method is equivalent to the Additive Method of [[5](#5)].

# What's New in Version 0.2.0?

The latest version improves support for static typing and includes a breaking change.

## Breaking Change To `calculate_implied_probabilities()` Signature

All arguments to `calculate_implied_probabilities()` other than `odds` are now keyword only arguments. This change
simplified declaration of overloads to support typing the function's return value and will allow for more flexibility
in the API.

```py
from shin import calculate_implied_probabilities

# still works
calculate_implied_probabilities([2.0, 2.0])
calculate_implied_probabilities(odds=[2.0, 2.0])
calculate_implied_probabilities([2.0, 2.0], full_output=True)
## also any other combination of passing arguments as keyword args remains the same

# passing any arg other than `odds` as positional is now an error
calculate_implied_probabilibies([2.0, 2.0], 1000)  # Error
calculate_implied_probabilities([2.0, 2.0], max_iterations=1000)  # OK


calculate_impolied_probabilities([2.0, 2.0], 1000, 1e-12, True) # Error
calculate_implied_probabilities([2.0, 2.0], max_iterations=1000, convergence_threshold=1e-12, full_output=True)  # OK
```

See [this commit](https://github.com/mberk/shin/commit/06a4ce90fc9bb047cef4e70d8a429b69a6cfd181) for more details.

## Full Output Type

The `full_output` argument now returns a `ShinOptimisationDetails` object instead of a `dict`. This object is a
`dataclass` with the same fields as the `dict` that was previously returned.

For the read-only case, the `ShinOptimisationDetails` object can be used as a drop-in replacement for the `dict` that
was previously returned as it supports `__getitem__()`.

This change was introduced to support generic typing of the `implied_probabilities`, currently not supported by
`TypedDict` in versions of Python < 3.11.

See [this](https://github.com/mberk/shin/commit/467d88954d5ca958b6a1b73c9c4af412725b4d4a) and
[this](https://github.com/mberk/shin/commit/c9b6e42b9d791fa4e4219a993f0dd2524ceaa1b5) for more details.

# What's New in Version 0.1.0?

The latest version introduces some substantial changes and breaking API changes.

## Default Return Value Behaviour

Previously `shin.calculate_implied_probabilities` would return a `dict` that contained convergence details of the
iterative fitting procedure along with the implied probabilities:

```python
import shin

shin.calculate_implied_probabilities([2.6, 2.4, 4.3])
```

```
{'implied_probabilities': [0.37299406033208965,
  0.4047794109200184,
  0.2222265287474275],
 'iterations': 425,
 'delta': 9.667822098435863e-13,
 'z': 0.01694251276407055}
```

The default behaviour now is for the function to only return the implied probabilities:

```python
import shin

shin.calculate_implied_probabilities([2.6, 2.4, 4.3])
```

```
[0.37299406033208965, 0.4047794109200184, 0.2222265287474275]
```

The full output can still be had by setting the `full_output` argument to `True`:

```python
import shin

shin.calculate_implied_probabilities([2.6, 2.4, 4.3], full_output=True)
```

```
{'implied_probabilities': [0.37299406033208965,
  0.4047794109200184,
  0.2222265287474275],
 'iterations': 425,
 'delta': 9.667822098435863e-13,
 'z': 0.01694251276407055}
```

## Passing Mappings

A common scenario is to have a mapping between some selection identifiers and their odds. You can now pass such
mappings to `shin.calculate_implied_probabilities` and have a new `dict` mapping between the selection identifiers and
their probabilities returned:

```python
import shin

shin.calculate_implied_probabilities({"HOME": 2.6, "AWAY": 2.4, "DRAW": 4.3})
```

```
{'HOME': 0.37299406033208965,
 'AWAY': 0.4047794109200184,
 'DRAW': 0.2222265287474275}
```

This also works when asking for the full output to be returned:

```python
import shin

shin.calculate_implied_probabilities({"HOME": 2.6, "AWAY": 2.4, "DRAW": 4.3}, full_output=True)
```

```
{'implied_probabilities': {'HOME': 0.37299406033208965,
  'AWAY': 0.4047794109200184,
  'DRAW': 0.2222265287474275},
 'iterations': 426,
 'delta': 9.667822098435863e-13,
 'z': 0.01694251276407055}
```

## Controlling the Optimiser

Starting in version 0.1.0, the iterative procedure is implemented in Rust which provides a  considerable performance
boost. If you would like to use the old Python based optimiser use the `force_python_optimiser` argument:

```python
import timeit
timeit.timeit(
    "shin.calculate_implied_probabilities([2.6, 2.4, 4.3], force_python_optimiser=True)",
    setup="import shin",
    number=10000
)
```

```
3.9101167659973726
```

```python
import timeit
timeit.timeit(
    "shin.calculate_implied_probabilities([2.6, 2.4, 4.3])",
    setup="import shin",
    number=10000
)
```

```
0.14442387002054602
```

# References

<a id="1">[1]</a> 
[H. S. Shin, “Prices of State Contingent Claims with Insider
traders, and the Favorite-Longshot Bias”. The Economic
Journal, 1992, 102, pp. 426-435.](https://doi.org/10.2307/2234526)

<a id="2">[2]</a> 
[H. S. Shin, “Measuring the Incidence of Insider Trading in a
Market for State-Contingent Claims”. The Economic Journal,
1993, 103(420), pp. 1141-1153.](https://doi.org/10.2307/2234240)

<a id="3">[3]</a>
[E. Štrumbelj, "On determining probability forecasts from betting odds".
International Journal of Forecasting, 2014, Volume 30, Issue 4,
pp. 934-943.](https://doi.org/10.1016/j.ijforecast.2014.02.008)

<a id="4">[4]</a>
[B. Jullien and B. Salanié, "Measuring the Incidence of Insider Trading: A Comment on Shin".
The Economic Journal, 1994, 104(427), pp. 1418–1419](https://doi.org/10.2307/2235458)

<a id="5">[5]</a>
[S. Clarke, S. Kovalchik, M. Ingram, "Adjusting bookmaker’s odds to allow for
overround". American Journal of Sports Science, 2017, Volume 5, Issue 6,
pp. 45-49.](https://doi.org/10.11648/j.ajss.20170506.12)
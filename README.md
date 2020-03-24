# shin

A Python implementation of Shin's method [[1](#1), [2](#2)] for calculating implied probabilities from bookmaker odds.

Probabilities calculated in this way have been shown to be more accurate than those obtained by the standard approach
of dividing the inverse odds by the booksum [[3](#3)].

# Installation

Requires Python 3.5 or above.

```
pip install shin
```

# Usage

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

The returned `dict` contains the following fields

* `implied_probablities`
* `iterations` - Shin's method is an iterative procedure. Compare this value to the `max_iterations` argument
(default = `1000`) to check for failed convergence
* `delta` - the final change in `z` (see below) for the final iteration. Compare with the `convergence_threshold`
argument (default = `1e-12`) to assess convergence
* `z` - the estimated proportion of theoretical betting volume coming from insider traders 

# References

<a id="1">[1]</a> 
[H. S. Shin, “Prices of State Contingent Claims with Insider
traders, and the Favorite-Longshot Bias”. The Economic
Journal, 1992, 102, pp. 426-435.](https://doi.org/10.2307/2234526)

<a id="1">[2]</a> 
[H. S. Shin, “Measuring the Incidence of Insider Trading in a
Market for State-Contingent Claims”. The Economic Journal,
1993, 103(420), pp. 1141-1153.](https://doi.org/10.2307/2234240)

<a id="1">[3]</a>
[E. Štrumbelj, "On determining probability forecasts from betting odds".
International Journal of Forecasting, 2014, Volume 30, Issue 4,
pp. 934-943.](https://doi.org/10.1016/j.ijforecast.2014.02.008)

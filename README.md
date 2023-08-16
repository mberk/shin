# shin

A Python implementation of Shin's method [[1](#1), [2](#2)] for calculating implied probabilities from bookmaker odds.

Probabilities calculated in this way have been shown to be more accurate than those obtained by the standard approach
of dividing the inverse odds by the booksum [[3](#3)].

# Installation

Requires Python 3.6 or above.

```
pip install shin
```

# Usage

## Three or more outcomes

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

The returned `dict` contains the following fields:

* `implied_probablities`
* `iterations` - with three or more outcomes, Shin's method uses an iterative procedure. Compare this value to the
`max_iterations` argument (default = `1000`) to check for failed convergence
* `delta` - the final change in `z` (see below) for the final iteration. Compare with the `convergence_threshold`
argument (default = `1e-12`) to assess convergence
* `z` - the estimated proportion of theoretical betting volume coming from insider traders

## Two outcomes 

```python
import shin

shin.calculate_implied_probabilities([1.5, 2.74])
```

```
{'implied_probabilities': [0.6508515815085157, 0.3491484184914841],
 'iterations': 0,
 'delta': 0,
 'z': 0.03172728540646625}
```

When there are only two outcomes, `z` can be calculated analytically [[3](#3)]. In this case, the `iterations` and
`delta` fields of the returned `dict` are `0` to reflect this.

Note that with two outcomes, Shin's method is equivalent to the Additive Method of [[4](#4)].  

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

<a id="3">[4]</a>
[S. Clarke, S. Kovalchik, M. Ingram, "Adjusting bookmaker’s odds to allow for
overround". American Journal of Sports Science, 2017, Volume 5, Issue 6,
pp. 45-49.](https://doi.org/10.11648/j.ajss.20170506.12)
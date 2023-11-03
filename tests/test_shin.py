import pytest

import shin


def test_calculate_implied_probabilities():
    with pytest.raises(ValueError):
        shin.calculate_implied_probabilities([])

    with pytest.raises(ValueError):
        shin.calculate_implied_probabilities([1.98])

    with pytest.raises(ValueError):
        shin.calculate_implied_probabilities([0.9, 0.1])

    result = shin.calculate_implied_probabilities([2.6, 2.4, 4.3], full_output=True)

    assert pytest.approx(0.3729941) == result["implied_probabilities"][0]
    assert pytest.approx(0.4047794) == result["implied_probabilities"][1]
    assert pytest.approx(0.2222265) == result["implied_probabilities"][2]
    assert pytest.approx(0.01694251) == result["z"]

    result = shin.calculate_implied_probabilities(
        [2.6, 2.4, 4.3], full_output=True, force_python_optimiser=True
    )

    assert pytest.approx(0.3729941) == result["implied_probabilities"][0]
    assert pytest.approx(0.4047794) == result["implied_probabilities"][1]
    assert pytest.approx(0.2222265) == result["implied_probabilities"][2]
    assert pytest.approx(0.01694251) == result["z"]

    result = shin.calculate_implied_probabilities([2.6, 2.4, 4.3])
    assert pytest.approx(0.3729941) == result[0]
    assert pytest.approx(0.4047794) == result[1]
    assert pytest.approx(0.2222265) == result[2]

    result = shin.calculate_implied_probabilities(
        {"HOME": 2.6, "AWAY": 2.4, "DRAW": 4.3}
    )
    assert {
        "HOME": pytest.approx(0.3729941),
        "AWAY": pytest.approx(0.4047794),
        "DRAW": pytest.approx(0.2222265),
    } == result

    result = shin.calculate_implied_probabilities(
        {"HOME": 2.6, "AWAY": 2.4, "DRAW": 4.3}, full_output=True
    )
    assert {
        "HOME": pytest.approx(0.3729941),
        "AWAY": pytest.approx(0.4047794),
        "DRAW": pytest.approx(0.2222265),
    } == result["implied_probabilities"]
    assert pytest.approx(0.01694251) == result["z"]

    odds = [1.5, 2.74]
    inverse_odds = [1 / o for o in odds]
    sum_inverse_odds = sum(inverse_odds)
    result = shin.calculate_implied_probabilities(odds, full_output=True)

    assert result["iterations"] == 0
    assert result["delta"] == 0

    # With two outcomes, Shin is equivalent to the Additive Method described in Clarke et al. (2017)
    assert (
        pytest.approx(inverse_odds[0] - (sum_inverse_odds - 1) / 2)
        == result["implied_probabilities"][0]
    )
    assert (
        pytest.approx(inverse_odds[1] - (sum_inverse_odds - 1) / 2)
        == result["implied_probabilities"][1]
    )

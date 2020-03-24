import pytest

import shin


def test_calculate_implied_probabilities():
    with pytest.raises(ValueError):
        shin.calculate_implied_probabilities([0.9, 0.1])

    result = shin.calculate_implied_probabilities([2.6, 2.4, 4.3])

    assert pytest.approx(0.3729941) == result['implied_probabilities'][0]
    assert pytest.approx(0.4047794) == result['implied_probabilities'][1]
    assert pytest.approx(0.2222265) == result['implied_probabilities'][2]
    assert pytest.approx(0.01694251) == result['z']

    result = shin.calculate_implied_probabilities([])

    assert 0 == len(result['implied_probabilities'])

import pytest

import shin


def test_calculate_implied_probabilities_error_conditions() -> None:
    with pytest.raises(ValueError):
        shin.calculate_implied_probabilities([])

    with pytest.raises(ValueError):
        shin.calculate_implied_probabilities([1.98])

    with pytest.raises(ValueError):
        shin.calculate_implied_probabilities([0.9, 0.1])


@pytest.mark.parametrize("force_python_optimiser", [True, False])
def test_calculate_implied_probabilities_full_output(
    force_python_optimiser: bool,
) -> None:
    full_output = shin.calculate_implied_probabilities(
        [2.6, 2.4, 4.3], full_output=True, force_python_optimiser=force_python_optimiser
    )

    assert pytest.approx(0.3729941) == full_output.implied_probabilities[0]
    assert pytest.approx(0.4047794) == full_output.implied_probabilities[1]
    assert pytest.approx(0.2222265) == full_output.implied_probabilities[2]
    assert pytest.approx(0.01694251) == full_output.z


def test_calculate_implied_probabilities_sequence_input() -> None:
    result = shin.calculate_implied_probabilities([2.6, 2.4, 4.3])
    assert pytest.approx(0.3729941) == result[0]
    assert pytest.approx(0.4047794) == result[1]
    assert pytest.approx(0.2222265) == result[2]


def test_calculate_implied_probabilties_mapping_input() -> None:
    result = shin.calculate_implied_probabilities(
        {"HOME": 2.6, "AWAY": 2.4, "DRAW": 4.3}
    )
    assert {
        "HOME": pytest.approx(0.3729941),
        "AWAY": pytest.approx(0.4047794),
        "DRAW": pytest.approx(0.2222265),
    } == result


def test_calculate_implied_probabilities_full_output_mapping_input() -> None:
    result = shin.calculate_implied_probabilities(
        {"HOME": 2.6, "AWAY": 2.4, "DRAW": 4.3}, full_output=True
    )
    assert {
        "HOME": pytest.approx(0.3729941),
        "AWAY": pytest.approx(0.4047794),
        "DRAW": pytest.approx(0.2222265),
    } == result.implied_probabilities
    assert pytest.approx(0.01694251) == result.z


def test_calculate_implied_probabilities_two_outcomes() -> None:
    odds = [1.5, 2.74]
    inverse_odds = [1 / o for o in odds]
    sum_inverse_odds = sum(inverse_odds)
    result = shin.calculate_implied_probabilities(odds, full_output=True)

    assert result.iterations == 0
    assert result.delta == 0

    # With two outcomes, Shin is equivalent to the Additive Method described in Clarke et al. (2017)
    assert (
        pytest.approx(inverse_odds[0] - (sum_inverse_odds - 1) / 2)
        == result.implied_probabilities[0]
    )
    assert (
        pytest.approx(inverse_odds[1] - (sum_inverse_odds - 1) / 2)
        == result.implied_probabilities[1]
    )


def test_full_output_get_item_interface() -> None:
    full_output = shin.ShinOptimisationDetails(
        implied_probabilities=[0.3, 0.4, 0.3], iterations=10, delta=0.1, z=0.5
    )
    assert full_output["implied_probabilities"] == [0.3, 0.4, 0.3]
    assert full_output["iterations"] == 10
    assert full_output["delta"] == 0.1
    assert full_output["z"] == 0.5
    with pytest.raises(KeyError):
        full_output["foo"]  # type: ignore[call-overload]

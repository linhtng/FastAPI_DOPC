import pytest
from pydantic import ValidationError

from app.models.models import DeliverySpecs


@pytest.mark.parametrize(
    "test_ranges,expected_error, check_msg",
    [
        ([], "Distance ranges cannot be empty", True),
        (
            [
                {"min": 100, "max": 200, "a": 0, "b": 0},
                {"min": 200, "max": 0, "a": 0, "b": 0},
            ],
            "First distance range must start at min=0",
            True,
        ),
        (
            [
                {"min": 0, "max": 200, "a": 0, "b": 0},
                {"min": 200, "max": 300, "a": 0, "b": 0},
            ],
            "Last distance range must end with max=0",
            True,
        ),
        (
            [
                {"min": 0, "max": 200, "a": 0, "b": 0},
                {"min": 100, "max": 0, "a": 0, "b": 0},
            ],
            "Distance ranges must be sorted by min value",
            False,
        ),
        (
            [
                {"min": 0, "max": 200, "a": 0, "b": 0},
                {"min": 300, "max": 0, "a": 0, "b": 0},
            ],
            "Range gap found",
            True,
        ),
    ],
    ids=[
        "empty_ranges",
        "first_not_zero",
        "last_not_zero",
        "unsorted_ranges",
        "discontinuous_ranges",
    ],
)
def test_invalid_distance_ranges(test_ranges, expected_error, check_msg):
    with pytest.raises(ValidationError) as exc:
        DeliverySpecs(
            order_minimum_no_surcharge=1000, base_price=200, distance_ranges=test_ranges
        )
    # Verify exception was raised
    assert isinstance(exc.value, ValidationError)

    if check_msg and expected_error:
        assert expected_error in str(exc.value)


def test_valid_distance_ranges():
    valid_ranges = [
        {"min": 0, "max": 500, "a": 0, "b": 0},
        {"min": 500, "max": 1000, "a": 100, "b": 1},
        {"min": 1000, "max": 0, "a": 0, "b": 0},
    ]
    specs = DeliverySpecs(
        order_minimum_no_surcharge=1000, base_price=200, distance_ranges=valid_ranges
    )
    assert len(specs.distance_ranges) == 3

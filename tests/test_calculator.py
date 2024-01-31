from app.calculator import DeliveryCalculator
from app.models import DeliveryRequest
import pytest

def test_small_order_surcharge():
    # Arrange
    request = DeliveryRequest(cart_value=500, delivery_distance=2000, number_of_items=5, time="2022-12-31T15:30:00Z")
    calculator = DeliveryCalculator(request)

    # Act
    surcharge = calculator.small_order_surcharge()

    # Assert
    assert surcharge == 500, "The surcharge for a small order must be the difference between the minimum cart value and the actual cart value"


@pytest.mark.parametrize(
    "distance, expected_fee",
    [
        (1499, 300),  # 2€ base fee + 1€ for the additional 500 m => 3€
        (1500, 300),  # 2€ base fee + 1€ for the additional 500 m => 3€
        (1501, 400),  # 2€ base fee + 2€ for the additional 501 m => 4€
        (2000, 400),  # 2€ base fee + 2€ for the additional 1000 m => 4€
        (5000, 1000),  # 2€ base fee + 8€ for the additional 4000 m => 10€
        (10000, 2000),  # 2€ base fee + 18€ for the additional 9000 m => 20€
    ],
)
def test_distance_based_fee(distance, expected_fee):
    # Arrange
    request = DeliveryRequest(cart_value=1000, delivery_distance=distance, number_of_items=5, time="2022-12-31T15:30:00Z")
    calculator = DeliveryCalculator(request)

    # Act
    fee = calculator.distance_based_fee() + calculator.delivery_fee

    # Assert
    assert fee == expected_fee, f"The distance-based fee for {distance} meters should be {expected_fee} cents"

@pytest.mark.parametrize(
    "items, expected_surcharge",
    [
        (4, 0),  # no surcharge
        (5, 50),  # 50 cents is added
        (10, 300),  # 3€ surcharge (6 x 50 cents) is added
        (13, 570),  # 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
        (14, 620),  # 6,20€ surcharge is added ((10 * 50 cents) + 1,20€)
        (15, 670),  # 6,70€ surcharge is added ((11 * 50 cents) + 1,20€)
    ],
)
def test_item_surcharge(items, expected_surcharge):
    # Arrange
    request = DeliveryRequest(cart_value=1000, delivery_distance=2000, number_of_items=items, time="2022-12-31T15:30:00Z")
    calculator = DeliveryCalculator(request)

    # Act
    surcharge = calculator.item_surcharge()

    # Assert
    assert surcharge == expected_surcharge, f"The surcharge for {items} items should be {expected_surcharge} cents"


@pytest.mark.parametrize(
    "time, expected_multiplier",
    [
        ("2024-01-31T15:30:00Z", 1),  # no multiplier
        ("2024-1-26T14:59:59Z", 1),  # no multiplier
        ("2024-01-26T15:00:00Z", 1.2),  # 1.2x multiplier
        ("2024-01-26T18:59:59Z", 1.2),  # 1.2x multiplier
        ("2024-01-31T19:00:00Z", 1),  # no multiplier
    ],
)
def test_rush_hour_multiplier(time, expected_multiplier):
    # Arrange
    request = DeliveryRequest(cart_value=1000, delivery_distance=2000, number_of_items=5, time=time)
    calculator = DeliveryCalculator(request)

    # Act
    multiplier = calculator.rush_hour_multiplier()

    # Assert
    assert multiplier == expected_multiplier, f"The rush hour multiplier should be {expected_multiplier} at {time}"


@pytest.mark.parametrize(
    "cart_value, delivery_distance, number_of_items, time, expected_fee",
    [
        (2, 100000, 150, "2024-01-26T15:00:00Z", 1500 ),  # must be capped at 1500 cents
        (1, 2235, 4, "2024-01-26T14:00:00Z", 1499 ),  # 1499 cents
    ],
)
def test_cap_fee(cart_value, delivery_distance, number_of_items, time, expected_fee):
    # Arrange
    request = DeliveryRequest(cart_value=cart_value, delivery_distance=delivery_distance, number_of_items=number_of_items, time=time)
    calculator = DeliveryCalculator(request)

    # Act
    capped_fee = calculator.total_fee()

    # Assert
    assert capped_fee == expected_fee, "The delivery fee can never be more than 1500 cents, including possible surcharges."


@pytest.mark.parametrize(
    "cart_value, expected_fee",
    [
        (20000, 0),  # free shipping
        (20001, 0),  # free shipping
        (19999, 450),  # no free shipping
    ],
)
def test_total_fee_free_shipping(cart_value, expected_fee):
    # Arrange
    request = DeliveryRequest(cart_value=cart_value, delivery_distance=2000, number_of_items=5, time="2022-12-31T15:30:00Z")
    calculator = DeliveryCalculator(request)

    # Act
    total_fee = calculator.total_fee()

    # Assert
    assert total_fee == expected_fee, "The total fee should be 0 for cart value >= 20000 cents"



@pytest.mark.parametrize(
    "cart_value, delivery_distance, number_of_items, time, expected_fee",
    [
        (790, 2235, 4, "2024-01-15T13:00:00Z", 710 ),  # correct amount 710 cents
        (790, 2235, 5, "2024-01-15T13:00:00Z", 760 ),  # correct amount 760 cents
        (790, 2235, 13, "2024-01-15T13:00:00Z", 1280 ),  # correct amount 710 + 570 surcharge
        (790, 2235, 4, "2024-01-26T18:59:59Z", 852 ),  # correct amount 710 * 1.2x cents
    ],
)
def test_total_fee(cart_value, delivery_distance, number_of_items, time, expected_fee):
    # Arrange
    request = DeliveryRequest(cart_value=cart_value, delivery_distance=delivery_distance, number_of_items=number_of_items, time=time)
    calculator = DeliveryCalculator(request)

    # Act
    total_fee = calculator.total_fee()

    # Assert
    assert total_fee == expected_fee, f"For {cart_value} cents cart value, {delivery_distance} meters delivery distance, {number_of_items} items and {time} time, the total fee should be {expected_fee} cents"
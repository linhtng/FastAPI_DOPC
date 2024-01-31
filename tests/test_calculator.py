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
    assert surcharge == 500, "The surcharge for a small order should be the difference between the minimum cart value and the actual cart value"
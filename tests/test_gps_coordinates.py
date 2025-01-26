import pytest
from math import pi
from app.models.models import GPSCoordinates
from app.utils.constants import (
    MIN_LAT, MAX_LAT, MIN_LON, MAX_LON, 
    EXPECTED_USER_LATITUDE, 
    EXPECTED_USER_LONGITUDE
)

def test_given_min_longitude_then_accepts():
    # Arrange & Act
    coords = GPSCoordinates(longitude=MIN_LON, latitude=EXPECTED_USER_LATITUDE)
    # Assert
    assert coords.longitude == MIN_LON

def test_given_max_longitude_then_accepts():
    # Arrange & Act
    coords = GPSCoordinates(longitude=MAX_LON, latitude=EXPECTED_USER_LATITUDE)
    # Assert
    assert coords.longitude == MAX_LON

def test_given_below_min_longitude_then_raises_error():
    # Arrange
    invalid_lon = MIN_LON - 1
    valid_lat = EXPECTED_USER_LATITUDE
    # Act & Assert
    with pytest.raises(ValueError):
        GPSCoordinates(longitude=invalid_lon, latitude=valid_lat)

def test_given_min_latitude_then_accepts():
    # Arrange & Act
    coords = GPSCoordinates(longitude=EXPECTED_USER_LONGITUDE, latitude=MIN_LAT)
    # Assert
    assert coords.latitude == MIN_LAT

def test_given_max_latitude_then_accepts():
    # Arrange & Act
    coords = GPSCoordinates(longitude=EXPECTED_USER_LONGITUDE, latitude=MAX_LAT)
    # Assert
    assert coords.latitude == MAX_LAT

def test_given_above_max_latitude_then_raises_error():
    # Arrange
    valid_lon = EXPECTED_USER_LONGITUDE
    invalid_lat = MAX_LAT + 1
    # Act & Assert
    with pytest.raises(ValueError):
        GPSCoordinates(longitude=valid_lon, latitude=invalid_lat)

def test_given_invalid_longitude_then_raises_error():
    # Arrange
    invalid_lon = MAX_LON + 1
    valid_lat = EXPECTED_USER_LATITUDE
    
    # Act & Assert
    with pytest.raises(ValueError):
        GPSCoordinates(longitude=invalid_lon, latitude=valid_lat)

def test_given_invalid_latitude_then_raises_error():
    # Arrange
    valid_lon = EXPECTED_USER_LONGITUDE
    invalid_lat = MIN_LAT - 1
    
    # Act & Assert
    with pytest.raises(ValueError):
        GPSCoordinates(longitude=valid_lon, latitude=invalid_lat)


def test_from_coordinates_creates_instance():
    # Arrange
    coord_tuple = (EXPECTED_USER_LONGITUDE, EXPECTED_USER_LATITUDE)
    
    # Act
    coords = GPSCoordinates.from_coordinates(coord_tuple)
    
    # Assert
    assert coords.longitude == coord_tuple[0]
    assert coords.latitude == coord_tuple[1]

def test_to_radians_converts_correctly():
    # Arrange
    lon, lat = 180.0, 90.0
    coords = GPSCoordinates(longitude=lon, latitude=lat)
    
    # Act
    lat_rad, lon_rad = coords.to_radians()
    
    # Assert
    assert lat_rad == pi/2  # 90 degrees
    assert lon_rad == pi    # 180 degrees
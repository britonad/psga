import pytest

from app.models import Position, Ship


@pytest.fixture
def ship():
    """A dummy ship fixture."""

    ship = Ship(imo=9595321, name='MSC Preziosa')
    ship.save()

    return ship


@pytest.fixture
def position(ship):
    """A dummy position fixture."""

    position = Position(
        latitude='17.9850006103516',
        longitude='-63.1359672546387',
        ship=ship,
        timestamp='2019-01-15 09:43:13+00'
    )
    position.save()

    return position


@pytest.mark.django_db
def test_ships_endpoint(client, ship):
    # Given: a ship entry with data exists in the database.
    result = [{'imo': ship.imo, 'name': ship.name}]
    # When: a request is being made to the endpoint.
    response = client.get('/api/ships/')

    # Then: the endpoint returns the JSON data that corresponds to the result.
    assert response.json() == result


@pytest.mark.django_db
def test_ship_positions_endpoint(client, position):
    # Given: a position entry with data exists in the database.
    result = [
        {'latitude': position.latitude, 'longitude': position.longitude}
    ]
    # When: a request is being made to the endpoint.
    response = client.get('/api/positions/9595321/')

    # Then: the endpoint returns the JSON data that corresponds to the result.
    assert response.json() == result

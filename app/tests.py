from io import StringIO

import pytest
from django.core.management import call_command, CommandError
from rest_framework import status

from app.models import Position, Ship


def test_home_page(client):
    # Given: a template that should render geographical data provided.
    # When: a request hits the endpoint.
    response = client.get('/')

    # Then: it successfully renders to the end-user this template.
    assert response.status_code == status.HTTP_200_OK
    assert b'Python Assignment' in response.content


@pytest.mark.django_db
def test_import_geo_data():
    # Given: a CSV file containing 3 rows.
    # When: a command is invoked with a provided file name.
    stdout = StringIO()
    call_command('import_geo_data', file='fixtures/test.csv', stdout=stdout)

    # Then: it produces a success message to stdout and writes entries to a DB.
    assert 'The data has been imported successfully.' in stdout.getvalue()
    assert Ship.objects.count() == 3
    assert Position.objects.count() == 3
    assert (
            Position.objects.filter(ship__imo=Ship.objects.first().imo)
            .count() == 1
    )


@pytest.mark.django_db
def test_import_geo_data_with_exception():
    # Given: a non-existent CSV file.
    # When: a command is invoked with a non-existent provided file name.
    # Then: it raises a CommandError exception.
    with pytest.raises(CommandError):
        call_command('import_geo_data', file='non-existent.csv')

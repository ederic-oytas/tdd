"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
import pytest

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status


@pytest.fixture()
def client():
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_duplicate_a_counter(self, client):
        """It should return an error for duplicates"""
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_a_counter(self, client):
        result = client.post('/counters/fiz')
        assert result.status_code == status.HTTP_201_CREATED
        assert result.json['fiz'] == 0
        result = client.put('/counters/fiz')
        assert result.status_code == status.HTTP_200_OK
        assert result.json['fiz'] == 1

    def test_update_not_found(self, client):
        result = client.put('/counters/buz')
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_read_a_counter(self, client):
        result = client.post('/counters/raz')
        assert result.status_code == status.HTTP_201_CREATED
        assert result.json['raz'] == 0
        result = client.put('/counters/raz')
        assert result.status_code == status.HTTP_200_OK
        assert result.json['raz'] == 1
        result = client.get('/counters/raz')
        assert result.status_code == status.HTTP_200_OK
        assert result.json['raz'] == 1

    def test_read_not_found(self, client):
        result = client.get('/counters/jaz')
        assert result.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_a_counter(self, client):
        result = client.post('/counters/fun')
        assert result.status_code == status.HTTP_201_CREATED
        assert result.json['fun'] == 0
        result = client.get('/counters/fun')
        assert result.status_code == status.HTTP_200_OK
        assert result.json['fun'] == 0
        result = client.delete('/counters/fun')
        assert result.status_code == status.HTTP_204_NO_CONTENT
        result = client.get('/counters/fun')
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_not_found(self, client):
        result = client.delete('/counters/tun')
        assert result.status_code == status.HTTP_404_NOT_FOUND

import pytest

def test_index(client):
    response = client.get('/')
    assert b'City Walker API v1' in response.data

import pytest
import scraper.service as service
from unittest import mock
import requests


@mock.patch('scraper.service.getUserFromDB')
def test_get_user_from_db(mock_getUserFromDB):
    mock_getUserFromDB.return_value = 'Mocked Alice'
    username = service.getUserFromDB(1)

    assert username == 'Mocked Alice'


@mock.patch('requests.get')
def test_getUsers(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'id': 1, 'name': 'John Doe'}
    mock_get.return_value = mock_response
    data = service.getUsers()

    assert data == {'id': 1, 'name': 'John Doe'}


@pytest.mark.testmark
@mock.patch('requests.get')
def test_getUsers_error(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 400
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        service.getUsers()

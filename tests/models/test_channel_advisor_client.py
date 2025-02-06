from channel_advisor_api.models.channel_advisor_client import ChannelAdvisorClient
from unittest.mock import patch, MagicMock
import pytest
import base64
import json
from unittest.mock import call


@pytest.fixture
def requests_mock():
    with patch("channel_advisor_api.models.channel_advisor_client.requests") as mock:
        yield mock


@pytest.fixture
def authenticated_client():
    client = ChannelAdvisorClient()
    client.set_test_access_token("test_access_token")
    return client


@pytest.fixture
def expected_headers():
    return {"Authorization": "Bearer test_access_token", "Content-Type": "application/json"}


def test_client_access_token(requests_mock, mock_environ):
    requests_mock.post.return_value.json.return_value = {"access_token": "test_access_token"}
    client = ChannelAdvisorClient()
    assert client.access_token == "test_access_token"
    assert requests_mock.post.call_count == 1

    # Create the base64 encoded auth string
    auth_string = base64.b64encode(b"test_client_id:test_client_secret").decode()

    requests_mock.post.assert_called_with(
        "https://api.channeladvisor.com/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600,
        },
        headers={
            "Authorization": f"Basic {auth_string}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        },
    )


def test_client_access_token_cached(requests_mock):
    client = ChannelAdvisorClient()
    client.set_test_access_token("test_access_token")
    assert client.access_token == "test_access_token"
    assert requests_mock.post.call_count == 0


@patch.dict("os.environ", clear=True)
def test_client_access_token_missing_env(requests_mock):
    with pytest.raises(ValueError):
        ChannelAdvisorClient().access_token


def test_client_access_token_failed(requests_mock):
    requests_mock.post.return_value.ok = False
    with pytest.raises(ValueError):
        ChannelAdvisorClient().access_token


@pytest.mark.parametrize("http_method", ["GET", "POST", "PUT", "DELETE", "PATCH"])
def test_request_success(requests_mock, mock_environ, expected_headers, http_method):
    requests_mock.request.return_value.ok = True
    requests_mock.request.return_value.content = json.dumps({"data": "test_response"})

    client = ChannelAdvisorClient()
    client.set_test_access_token("test_access_token")
    response = client.request(http_method, "test/endpoint", params={"key": "value"}, data={"test": "data"})

    assert requests_mock.request.call_count == 1
    requests_mock.request.assert_called_with(
        http_method,
        "https://api.channeladvisor.com/v1/test/endpoint",
        data=json.dumps({"test": "data"}),
        params={"key": "value"},
        headers=expected_headers,
    )
    assert json.loads(response.content) == {"data": "test_response"}


def test_request_failed_response(requests_mock, mock_environ, authenticated_client):
    requests_mock.request.return_value.ok = False

    with pytest.raises(Exception):
        authenticated_client.request("GET", "/test/endpoint")


def test_request_401(requests_mock, mock_environ, authenticated_client):
    authorization_error_response = MagicMock()
    authorization_error_response.ok = False
    authorization_error_response.status_code = 401
    second_response = MagicMock()
    second_response.ok = True
    second_response.status_code = 200
    second_response.content = json.dumps({"data": "test_response"})

    requests_mock.request.side_effect = [authorization_error_response, second_response]
    response = authenticated_client.request("GET", "/test/endpoint")
    assert requests_mock.request.call_count == 2
    assert response.content == '{"data": "test_response"}'


def test_request_401_max_retries(requests_mock, mock_environ, authenticated_client):
    authorization_error_response = MagicMock()
    authorization_error_response.ok = False
    authorization_error_response.status_code = 401

    requests_mock.request.side_effect = [authorization_error_response] * 5
    with pytest.raises(Exception, match="Authorization Error: 401"):
        authenticated_client.request("GET", "/test/endpoint")
    assert requests_mock.request.call_count == 2


def test_request_404(requests_mock, mock_environ, authenticated_client):
    requests_mock.request.return_value.ok = False
    requests_mock.request.return_value.status_code = 404

    response = authenticated_client.request("GET", "/test/endpoint")
    assert requests_mock.request.call_count == 1
    assert response is None


@patch("time.sleep")
def test_request_429(mock_sleep, requests_mock, mock_environ, authenticated_client):
    # Create mock response objects
    first_response = MagicMock()
    first_response.ok = False
    first_response.status_code = 429

    second_response = MagicMock()
    second_response.ok = True
    second_response.status_code = 200
    second_response.content = json.dumps({"data": "test_response"})

    # Set up the sequence of responses
    requests_mock.request.side_effect = [first_response, second_response]

    response = authenticated_client.request("GET", "/test/endpoint")
    assert requests_mock.request.call_count == 2
    assert response.content == '{"data": "test_response"}'
    mock_sleep.assert_called_once()


@patch("time.sleep")
def test_request_429_max_retries(mock_sleep, requests_mock, mock_environ, authenticated_client):
    # Create 10 rate-limited responses
    rate_limited_response = MagicMock()
    rate_limited_response.ok = False
    rate_limited_response.status_code = 429

    # Set up the sequence of 10 failed responses
    requests_mock.request.side_effect = [rate_limited_response] * 10

    with pytest.raises(Exception, match="Rate Limit: 429"):
        authenticated_client.request("GET", "/test/endpoint")

    assert requests_mock.request.call_count == 5
    assert mock_sleep.call_count == 4


def test_request_other_error_status(requests_mock, authenticated_client):
    # Mock a 500 Internal Server Error
    error_response = MagicMock()
    error_response.ok = False
    error_response.status_code = 500
    error_response.text = "Internal Server Error"
    requests_mock.request.return_value = error_response

    with pytest.raises(Exception, match="Request GET .* failed. Status: 500"):
        authenticated_client.request("GET", "/test/endpoint")


def test_get_all_pages_single_page(requests_mock, authenticated_client, expected_headers):
    # Mock single page response
    response = MagicMock()
    response.ok = True
    response.content = json.dumps({"value": [{"id": 1}, {"id": 2}]})
    requests_mock.request.return_value = response

    results = authenticated_client.get_all_pages("test/endpoint")

    assert len(results) == 2
    assert results == [{"id": 1}, {"id": 2}]
    assert requests_mock.request.call_count == 1
    requests_mock.request.assert_called_with(
        "get", "https://api.channeladvisor.com/v1/test/endpoint", data=None, headers=expected_headers
    )


def test_get_all_pages_multiple_pages(requests_mock, authenticated_client, expected_headers):
    # Mock responses for multiple pages
    first_response = MagicMock()
    first_response.ok = True
    first_response.content = json.dumps({"value": [{"id": 1}, {"id": 2}], "@odata.nextLink": "next_link"})

    second_response = MagicMock()
    second_response.ok = True
    second_response.content = json.dumps({"value": [{"id": 3}, {"id": 4}]})

    requests_mock.request.side_effect = [first_response, second_response]

    results = authenticated_client.get_all_pages("test/endpoint")

    assert len(results) == 4
    assert results == [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}]
    assert requests_mock.request.call_count == 2

    # Verify calls were made with correct page numbers
    requests_mock.request.assert_has_calls(
        [
            call("get", "https://api.channeladvisor.com/v1/test/endpoint", data=None, headers=expected_headers),
            call("get", "https://api.channeladvisor.com/v1/next_link", data=None, headers=expected_headers),
        ]
    )


def test_get_all_pages_empty_response(requests_mock, authenticated_client):
    response = MagicMock()
    response.ok = True
    response.content = json.dumps({"value": [], "totalPages": 1})
    requests_mock.request.return_value = response

    results = authenticated_client.get_all_pages("GET", "/test/endpoint")

    assert len(results) == 0
    assert results == []
    assert requests_mock.request.call_count == 1


def test_get_all_pages_with_limit(requests_mock, authenticated_client):
    response = MagicMock()
    response.ok = True
    response.content = json.dumps({"value": [{"id": 1}], "totalPages": 1})
    requests_mock.request.return_value = response

    results = authenticated_client.get_all_pages("test/endpoint", limit=2)

    assert len(results) == 1
    assert results == [{"id": 1}]
    assert requests_mock.request.call_count == 1
    requests_mock.request.assert_called_with(
        "get",
        "https://api.channeladvisor.com/v1/test/endpoint?%24top=2",
        data=None,
        headers={"Authorization": "Bearer test_access_token", "Content-Type": "application/json"},
    )


def test_get_all_pages_with_none_response(requests_mock, authenticated_client):
    # This will force request to return None
    requests_mock.request.return_value.ok = False
    requests_mock.request.return_value.status_code = 404

    results = authenticated_client.get_all_pages("test/endpoint", limit=1)

    assert len(results) == 0
    assert requests_mock.request.call_count == 1


def test_get_all_pages_with_string_response(requests_mock, authenticated_client):
    response = MagicMock()
    response.ok = True
    response.content = json.dumps({"Value": "test_response"})
    requests_mock.request.return_value = response

    results = authenticated_client.get_all_pages("test/endpoint", limit=1)

    assert len(results) == 1
    assert results == ["test_response"]
    assert requests_mock.request.call_count == 1


def test_get_all_pages_with_unexpected_response(requests_mock, authenticated_client):
    response = MagicMock()
    response.ok = True
    response.content = json.dumps({"foo": "bar"})
    requests_mock.request.return_value = response

    results = authenticated_client.get_all_pages("test/endpoint", limit=1)

    assert len(results) == 0
    assert results == []
    assert requests_mock.request.call_count == 1

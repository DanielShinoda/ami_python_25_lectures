from unittest.mock import Mock, patch

import pytest
import requests

from src.get_weather import get_temperature, get_weather_description, get_weather_wttr

MOCK_PATH = "src.get_weather.requests.get"


@pytest.fixture
def mock_weather_data():
    return {
        "current_condition": [
            {
                "temp_C": "15",
                "temp_F": "59",
                "weatherDesc": [{"value": "Partly cloudy"}],
                "humidity": "65",
                "pressure": "1012",
            }
        ]
    }


def test_get_weather_wttr_success(mock_weather_data):
    with patch(MOCK_PATH) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_weather_data
        mock_get.return_value = mock_response

        result = get_weather_wttr("Paris")

        assert result == mock_weather_data
        mock_get.assert_called_once_with(
            "http://wttr.in/Paris", params={"format": "j1"}, timeout=10
        )


def test_get_temperature(mock_weather_data):
    with patch(MOCK_PATH) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_weather_data
        mock_get.return_value = mock_response

        temperature = get_temperature("Madrid")

        assert temperature == 15.0
        assert isinstance(temperature, float)


def test_get_weather_description(mock_weather_data):
    with patch(MOCK_PATH) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_weather_data
        mock_get.return_value = mock_response

        description = get_weather_description("Berlin")

        assert description == "Partly cloudy"


def test_get_weather_api_error():
    with patch(MOCK_PATH) as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        result = get_weather_wttr("Moscow")

        assert result is None


def test_get_weather_invalid_json():
    with patch(MOCK_PATH) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = get_weather_wttr("Tokyo")

        assert result is None


def test_get_temperature_no_data():
    mock_weather_data = {"error": "City not found"}

    with patch(MOCK_PATH) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_weather_data
        mock_get.return_value = mock_response

        temperature = get_temperature("InvalidCity")

        assert temperature is None

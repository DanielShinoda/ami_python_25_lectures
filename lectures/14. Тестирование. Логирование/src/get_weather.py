from typing import Dict, Optional

import requests


def get_weather_wttr(city: str, format: str = "j1") -> Optional[Dict]:
    try:
        url = f"http://wttr.in/{city}"
        params = {"format": format}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return None


def get_temperature(city: str) -> Optional[float]:
    weather_data = get_weather_wttr(city)

    if weather_data and "current_condition" in weather_data:
        current = weather_data["current_condition"][0]
        return float(current["temp_C"])
    return None


def get_weather_description(city: str) -> Optional[str]:
    weather_data = get_weather_wttr(city)

    if weather_data and "current_condition" in weather_data:
        current = weather_data["current_condition"][0]
        return current["weatherDesc"][0]["value"]
    return None

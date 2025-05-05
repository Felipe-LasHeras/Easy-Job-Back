
import requests

def get_weather_data(city_name, api_key):
    """
    Obtiene datos climáticos para una ciudad específica utilizando OpenWeatherMap API.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric',
        'lang': 'es'
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos climáticos: {e}")
        return None

def get_occupation_code(description):
    """
    Obtiene el código de ocupación utilizando la API de codificación automática del INE.
    """
    url = "https://rapps.ine.cl:9292/predict"
    payload = {
        "text": description,
        "classifier": "ciuo"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener código de ocupación: {e}")
        return None

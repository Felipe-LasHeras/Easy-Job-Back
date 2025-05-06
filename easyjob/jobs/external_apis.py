import requests
from django.conf import settings

class ExternalAPIManager:

    @staticmethod
    def get_weather_data(city='Santiago'):
        try:
            api_key = settings.OPENWEATHERMAP_API_KEY
            if not api_key:
                return {'error': 'Falta la clave de API de OpenWeatherMap'}

            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es'
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200 or 'main' not in data:
                return {'error': f'Error en la respuesta del clima: {data.get("message", "desconocido")}'}

            return {
                'ciudad': city,
                'temperatura': data['main']['temp'],
                'descripcion': data['weather'][0]['description'],
                'humedad': data['main']['humidity'],
                'viento': data['wind']['speed']
            }
        except Exception as e:
            return {'error': f'Error al obtener clima: {str(e)}'}

    @staticmethod
    def get_exchange_rates(base='CLP'):
        try:
            api_key = settings.EXCHANGE_API_KEY
            if not api_key:
                return {'error': 'Falta la clave de API de ExchangeRate'}

            url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}'
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200 or 'conversion_rates' not in data:
                return {'error': f'Error en la respuesta de tasas de cambio: {data.get("error-type", "desconocido")}'}

            return {
                'base': base,
                'USD': data['conversion_rates']['USD'],
                'EUR': data['conversion_rates']['EUR']
            }
        except Exception as e:
            return {'error': f'Error al obtener tasas de cambio: {str(e)}'}

    @staticmethod
    def get_news():
        try:
            api_key = settings.NEWS_API_KEY
            if not api_key:
                return [{'titulo': 'Falta la clave de API de NewsAPI', 'url': '#'}]

            url = f'https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={api_key}'
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200 or 'articles' not in data:
                return [{'titulo': f'Error en la respuesta de noticias: {data.get("message", "desconocido")}', 'url': '#'}]

            articles = data.get('articles', [])[:3]
            return [{'titulo': a['title'], 'url': a['url']} for a in articles]
        except Exception as e:
            return [{'titulo': f'Error al obtener noticias: {str(e)}', 'url': '#'}]

    @staticmethod
    def get_random_facts():
        try:
            url = 'https://randomuser.me/api/?results=3'
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200 or 'results' not in data:
                return [{'nombre': 'Error', 'email': 'Respuesta inválida', 'pais': 'N/A'}]

            return [{
                'nombre': f"{user['name']['first']} {user['name']['last']}",
                'email': user['email'],
                'pais': user['location']['country']
            } for user in data['results']]
        except Exception as e:
            return [{'nombre': 'Error', 'email': str(e), 'pais': 'N/A'}]

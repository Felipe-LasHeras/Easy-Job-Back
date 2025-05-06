import requests

class ExternalAPIManager:
    WEATHER_API_KEY = '28fcf1158ed377a137b851435aa43c18'
    EXCHANGE_API_KEY = 'c09f49da25dd57e64dbcc523'
    
    @staticmethod
    def get_weather_data(city='Santiago'):
        """Obtiene el clima actual de una ciudad desde OpenWeatherMap"""
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={ExternalAPIManager.WEATHER_API_KEY}&units=metric&lang=es'
            response = requests.get(url)
            data = response.json()
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
        """Obtiene tasas de cambio desde ExchangeRate API"""
        try:
            url = f'https://v6.exchangerate-api.com/v6/{ExternalAPIManager.EXCHANGE_API_KEY}/latest/{base}'
            response = requests.get(url)
            data = response.json()
            return {
                'base': base,
                'USD': data['conversion_rates']['USD'],
                'EUR': data['conversion_rates']['EUR']
            }
        except Exception as e:
            return {'error': f'Error al obtener tasas de cambio: {str(e)}'}

    @staticmethod
    def get_news():
        """Obtiene noticias tecnológicas desde una API pública"""
        try:
            url = 'https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=YOUR_NEWSAPI_KEY'
            response = requests.get(url)
            data = response.json()
            articles = data.get('articles', [])[:3]
            return [{'titulo': a['title'], 'url': a['url']} for a in articles]
        except Exception as e:
            return [{'titulo': f'Error al obtener noticias: {str(e)}', 'url': '#'}]

    @staticmethod
    def get_random_facts():
        """Obtiene hechos curiosos desde RandomUser API"""
        try:
            url = 'https://randomuser.me/api/?results=3'
            response = requests.get(url)
            data = response.json()
            return [{
                'nombre': f"{user['name']['first']} {user['name']['last']}",
                'email': user['email'],
                'pais': user['location']['country']
            } for user in data['results']]
        except Exception as e:
            return [{'nombre': 'Error', 'email': str(e), 'pais': 'N/A'}]
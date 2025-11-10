from django.shortcuts import render
import requests, os
from datetime import datetime,timedelta
import pytz


def index(request):
    weather_data = {}
    city_image = None
    city = request.GET.get('city')
    message = None

    if city:
        weather_api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('OPENWEATHER_API_KEY')}&units=metric"
        # image_api = f"https://api.unsplash.com/search/photos?query={city}&client_id={os.getenv('UNSPLASH_ACCESS_KEY')}&orientation=landscape"

        weather_response = requests.get(weather_api).json()
        # image_response = requests.get(image_api).json()

        if weather_response.get('cod') == 200:
            description = weather_response['weather'][0]['description'].lower()

            if "rain" in description:
                message = "Grab an umbrella! ☔"
            elif "clear" in description:
                message = "Perfect day to go outside! ☀️"
            elif "cloud" in description:
                message = "A bit cloudy, but still nice! ☁️"
            elif "snow" in description:
                message = "Stay warm and enjoy the snow! ❄️"
            elif "storm" in description or "thunder" in description:
                message = "Stay indoors! ⚡"
            else:
                message = "Have a great day! 🌈"


            timezone_offset = weather_response['timezone']  # seconds from UTC
            local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
            local_time_str = local_time.strftime('%I:%M %p')

            sunrise_timestamp = weather_response['sys']['sunrise'] + timezone_offset
            sunset_timestamp = weather_response['sys']['sunset'] + timezone_offset

            sunrise_time = datetime.utcfromtimestamp(sunrise_timestamp).strftime('%I:%M %p')
            sunset_time = datetime.utcfromtimestamp(sunset_timestamp).strftime('%I:%M %p')

            weather_data = {
                'city': city.title(),
                'temperature': weather_response['main']['temp'],
                'humidity': weather_response['main']['humidity'],
                'wind': weather_response['wind']['speed'],
                'description': weather_response['weather'][0]['description'].title(),
                'icon': weather_response['weather'][0]['icon'],
                'local_time': local_time_str,
                'sunrise': sunrise_time,
                'sunset': sunset_time,
            }
            # if image_response['results']:
                # city_image = image_response['results'][0]['urls']['regular']

    return render(request, 'forecast.html', {'weather': weather_data,'message':message})

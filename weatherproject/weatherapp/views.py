from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    # Set the default city to 'Kathmandu'
    city = request.POST.get('city', 'kathmandu')
    
    # OpenWeather API URL
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=30852d42af97ee038278563e0696b565'
    PARAMS = {'units': 'metric'}
    
    # Google Custom Search API parameters
    API_KEY = 'AIzaSyAwaDvVqXCtmUap5Dle-0cezzhyzstF660'
    SEARCH_ENGINE_ID = 'd684f7bc2bc324b78'
    
    # Build query for city image search
    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
    
    # Fetch city image URL
    image_url = None
    try:
        image_data = requests.get(city_url).json()
        search_items = image_data.get("items", [])
        if search_items:
            image_url = search_items[0].get('link', None)
        else:
            image_url = "default_image_url_here"  # Set a default image URL if no results
    except requests.RequestException:
        image_url = "default_image_url_here"  # Fallback to a default image on request error
    
    # Fetch weather data
    try:
        weather_data = requests.get(weather_url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()
        exception_occurred = False
    except (requests.RequestException, KeyError):
        # Default weather data if the request fails or data is missing
        exception_occurred = True
        messages.error(request, 'Entered data is not available in the API')
        description = 'clear sky'
        icon = '01d'
        temp = 25
        day = datetime.date.today()

    return render(
        request,
        'weatherapp/index.html',
        {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': exception_occurred,
            'image_url': image_url
        }
    )
